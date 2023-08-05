# coding=utf-8
#

"""
 Copyright (c) 2019 Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

import os
import sys
import time
import platform

# NOTICE:This module must import modules with original Waf context classes
# before declaring their alter implementions.
# Otherwise classes in this module can be ignored. In normal case of
# using of the Waf such classes are created in the 'wscript' because this
# file is loaded always after all Waf context classes.

from waflib import Errors as waferror, Context as WafContext
from waflib.ConfigSet import ConfigSet
from waflib.Configure import ConfigurationContext as WafConfContext, conf
from waflib.Configure import find_program as wafFindProgram
from zm.constants import ZENMAKE_CONF_CACHE_PREFIX, WAF_CACHE_DIRNAME, WAF_CONFIG_LOG
from zm.constants import TASK_TARGET_KINDS, PLATFORM
from zm.pyutils import maptype
from zm.autodict import AutoDict
from zm.pathutils import PathsParam
from zm import utils, log, toolchains, error, db, version, cli, edeps, environmon
from zm.buildconf.select import handleOneTaskParamSelect, handleTaskParamSelects
from zm.buildconf.scheme import EXPORTING_TASK_PARAMS
from zm.features import TASK_TARGET_FEATURES_TO_LANG, TASK_LANG_FEATURES, \
    TOOLCHAIN_VARS, BUILDCONF_PREPARE_TASKPARAMS, ToolchainVars, getLoadedFeatures
from zm.waf import assist, context, config_actions as configActions

joinpath   = os.path.join
normpath   = os.path.normpath
relpath    = os.path.relpath
pathexists = os.path.exists
isabspath  = os.path.isabs
isfile     = os.path.isfile
getfsize   = os.path.getsize

toList       = utils.toList
toListSimple = utils.toListSimple

CONFLOG_HEADER_TEMPLATE = '''# Project %(prj)s configured on %(now)s by
# ZenMake %(zmver)s, based on Waf %(wafver)s (abi %(wafabi)s)
# python %(pyver)s on %(systype)s
# using %(args)s
#'''

def _genToolAutoName(lang):
    return 'auto-%s' % lang.replace('xx', '++')

TOOL_AUTO_NAMES = { _genToolAutoName(x) for x in ToolchainVars.allLangs() }
_DONT_STORE_TASK_PARAMS = ('$bconf', )
_EXPORT_PATH_PARAMS = frozenset(['includes', 'libpath', 'stlibpath'])
_DROP_FROM_COLLECTED_ENVVARS = set([
    'WAF_PRINT_FAILURE_LOG', 'WAF_CMD_FORMAT', 'WAF_LOG_FORMAT',
    'WAF_HOUR_FORMAT', 'NOSYNC', 'WAFLOCK', 'NOCOLOR', 'CLICOLOR',
    'CLICOLOR_FORCE', 'NO_LOCK_IN_RUN', 'NO_LOCK_IN_OUT', 'NO_LOCK_IN_TOP',
    'JOBS', 'NUMBER_OF_PROCESSORS', 'WAF_NO_PREFORK',
    'TERM', 'COLUMNS'
])

_cache = {}

class ConfigurationContext(WafConfContext):
    """ Context for command 'configure' """

    # pylint: disable = no-member,attribute-defined-outside-init
    # pylint: disable = too-many-instance-attributes

    def __init__(self, *args, **kwargs):

        self._fixSysEnvVars()
        super().__init__(*args, **kwargs)

        environmon.assignMonitoringTo(self, 'environ')

        self._loadedTools = {}
        self._toolchainEnvs = {}
        self._toolchainSettings = {}
        self._confCache = None
        self.allTasks = None
        self.allOrderedTasks = None
        self.monitFiles = []
        self.zmMetaConfAttrs = {}

    def _fixSysEnvVars(self):
        flagVars = ToolchainVars.allSysFlagVars()
        environ = os.environ
        for var in flagVars:
            val = environ.get(var)
            if val is not None:
                environ[var] = val.replace('"', '').replace("'", '')

    def _adjustTaskExportParams(self, taskParams):

        startdir = taskParams['$bconf'].startdir

        exportList = taskParams.pop('export', [])
        exportsMeta = []

        for param in EXPORTING_TASK_PARAMS:
            exportName = 'export-%s' % param
            exportVal = taskParams.pop(exportName, bool(param in exportList))

            if param == 'config-results':
                # it is handled in another place
                taskParams[exportName] = exportVal
                continue

            # gather meta for export
            if isinstance(exportVal, bool):
                exportVal = taskParams.get(param) if exportVal else None

            if not exportVal:
                continue

            withPaths = param in _EXPORT_PATH_PARAMS
            if withPaths and not isinstance(exportVal, PathsParam):
                exportVal = PathsParam(exportVal, startdir)

            exportsMeta.append((param, exportVal))

        return exportsMeta

    def _handleTaskExportParams(self, taskParams):

        exportsMeta = taskParams.pop('$exports-meta', [])
        nextDeps = taskParams.get('$ruse', [])
        if not nextDeps:
            return

        exportsMeta[0:0] = self._adjustTaskExportParams(taskParams)
        if not exportsMeta:
            return

        for name in nextDeps:
            depTaskParams = self.allTasks.get(name)
            if not depTaskParams:
                continue

            # apply gathered exports to depTaskParams
            for param, exportVal in exportsMeta:
                if param in _EXPORT_PATH_PARAMS:
                    paramVal = depTaskParams.get(param)
                    if paramVal is None:
                        depTaskParams[param] = PathsParam.makeFrom(exportVal)
                    else:
                        paramVal.insertFrom(0, exportVal)
                elif isinstance(exportVal, maptype):
                    paramVal = exportVal.copy()
                    paramVal.update(depTaskParams.get(param, {}))
                    depTaskParams[param] = paramVal
                else:
                    depTaskParams.setdefault(param, [])
                    depTaskParams[param][0:0] = exportVal

            # save exports for child tasks
            depTaskParams['$exports-meta'] = list(exportsMeta)

    def _gatherMonitoredEnvVars(self):

        names = set()
        names.update(environmon.monitoredVars())
        names -= _DROP_FROM_COLLECTED_ENVVARS

        for bconf in self.bconfManager.configs:
            names.update(bconf.usedEnvVars)

        names.update(assist.getPermanentMonitEnvVarNames())
        return tuple(names)

    def _handleMonitLibs(self, taskParams):

        for libsparam in ('libs', 'stlibs'):
            monitparam = 'monit' + libsparam
            monitLibs = taskParams.get(monitparam)
            if monitLibs is None:
                continue

            monitLibs = toList(monitLibs)
            libs = toList(taskParams.get(libsparam, []))
            if isinstance(monitLibs, bool):
                monitLibs = set(libs) if monitLibs else None
            else:
                monitLibs = set(monitLibs)
                monitLibs.intersection_update(libs)

            if not monitLibs:
                taskParams.pop(monitparam, None)
            else:
                taskParams[monitparam] = sorted(monitLibs)

    def _calcObjectsIndex(self, bconf, taskParams):

        # In this way indexes for object files aren't changed from build to build
        # while in Waf way they can be changed.

        cache = self.getConfCache()
        if 'object-idx' not in cache:
            cache['object-idx'] = {}

        indexes = cache['object-idx']
        key = '%s%s%s' % (bconf.path, os.pathsep, taskParams['name'])
        lastIdx = indexes.get('last-idx', 0)

        idx = taskParams.get('objfile-index')
        if idx is not None:
            if idx > lastIdx:
                indexes['last-idx'] = idx
            indexes[key] = idx
        else:
            idx = indexes.get(key)
            if idx is None:
                indexes['last-idx'] = idx = lastIdx + 1
                indexes[key] = idx
        return idx

    def _checkTaskDepsInUse(self):

        envPrefixes = ('LIB', 'STLIB', 'FRAMEWORK', 'INCLUDES')

        def check(dep, bconf, taskParams, allTasks):

            # check in local deps
            if dep in allTasks:
                return

            # check in configured external libs/frameworks
            env = self.all_envs[taskParams['$task.variant']]
            uselib = dep.upper()
            envNames = ('%s_%s' % (x, uselib) for x in envPrefixes)
            if any(x in env for x in envNames):
                return

            # problem found
            taskName = taskParams['name']
            msg = 'Task %r: dependency %r not found.' % (taskName, dep)
            raise error.ZenMakeConfError(msg, confpath = bconf.path)

        allTasks = self.allTasks
        for bconf in self.bconfManager.configs:
            for taskParams in bconf.tasks.values():
                for dep in taskParams.get('use', []):
                    check(dep, bconf, taskParams, allTasks)

    def _finishToolConfig(self, toolenv):

        # Waf skips all or some of these variables for toolchains like fortran, D, etc.
        # And therefore 'vnum' feature doesn't work for some toolchains.
        # This code fixes this problem.
        if not toolenv.DEST_OS:
            toolenv.DEST_OS = utils.getDefaultDestOS()
        if not toolenv.DEST_BINFMT:
            toolenv.DEST_BINFMT = utils.getDestBinFormatByOS(toolenv.DEST_OS)

    def _loadTool(self, tool, **kwargs):

        tooldirs = kwargs.get('tooldirs', None)
        withSysPath = kwargs.get('withSysPath', True)
        toolId = kwargs.get('id', '')

        loadedTool = self._loadedTools.setdefault(tool, {})
        toolInfo = loadedTool.get(toolId)
        if toolInfo:
            # don't load again
            return toolInfo

        module = None
        try:
            module = context.loadTool(tool, tooldirs, withSysPath)
        except ImportError as ex:
            paths = getattr(ex, 'toolsSysPath', sys.path)
            msg = 'Could not load the tool %r' % tool
            msg += ' from %r\n%s' % (paths, ex)
            self.fatal(msg)

        func = getattr(module, 'configure', None)
        if func and callable(func):
            # Here is false-positive of pylint
            # See https://github.com/PyCQA/pylint/issues/1493
            # pylint: disable = not-callable
            func(self)

            self._finishToolConfig(self.env)

        if not loadedTool: # avoid duplicates for loading on build stage
            self.tools.append({'tool' : tool, 'tooldir' : tooldirs, 'funs' : None})

        toolenv = self.env
        loadedTool[toolId] = (module, toolenv)

        return module, toolenv

    def _checkToolchainNames(self, bconf):

        validToolchainNames = self.getStandardToolchainNames()

        # Each bconf has own customToolchains
        validToolchainNames |= bconf.customToolchains.keys()

        for taskName, taskParams in bconf.tasks.items():
            names = taskParams['toolchain']
            for name in names:
                if name not in validToolchainNames:
                    msg = 'Toolchain %r for the task %r is not valid.' % (name, taskName)
                    msg += ' Valid toolchains: %r' % list(validToolchainNames)
                    raise error.ZenMakeConfError(msg, confpath = bconf.path)

    def _loadDetectedToolchain(self, lang, toolId):
        """
        Load auto detected toolchain by its lang
        """

        lang = lang.replace('++', 'xx')
        displayedLang = lang.replace('xx', '++').upper()

        self.msg('Autodetecting toolchain', '%s language' % displayedLang)

        cfgVar = ToolchainVars.cfgVarToSetToolchain(lang)

        toolname = None
        toolenv = self.env
        for toolname in toolchains.getNames(lang):
            self.env.stash()
            try:
                # try to load
                toolenv = self.loadTool(toolname, id = toolId)
            except waferror.ConfigurationError:
                self.env.revert()
            else:
                if toolenv[cfgVar]:
                    self.env.commit()
                    break
                self.env.revert()
        else:
            self.fatal('could not configure a %s toolchain!' % displayedLang)

        return toolname, toolenv

    def getStandardToolchainNames(self):
        """
        Return set of valid names of known toolchains without custom ones
        """

        langs = set(getLoadedFeatures()).intersection(ToolchainVars.allLangs())
        validNames = {'auto-' + lang.replace('xx', '++') for lang in langs}
        validNames.update(toolchains.getAllNames(platform = PLATFORM))
        return validNames

    def loadCaches(self):
        """
        Load cache files needed for 'configure'
        """

        cachePath = joinpath(self.cachedir.abspath(), ZENMAKE_CONF_CACHE_PREFIX)
        try:
            cache = db.loadFrom(cachePath)
        except EnvironmentError:
            cache = {}

        # protect from format changes
        zmversion = cache.get('zmversion', '')
        if zmversion != version.current():
            cache = { 'zmversion' : version.current() }

        self._confCache = cache

    def saveCaches(self):
        """
        Save cache files needed for 'configure' and for 'build'
        """

        bconfManager = self.bconfManager
        rootbconf    = bconfManager.root
        bconfPaths   = rootbconf.confPaths
        cachedir     = bconfPaths.zmcachedir
        rootdir      = rootbconf.rootdir
        relBTypeDir  = os.path.relpath(rootbconf.selectedBuildTypeDir, rootdir)

        # common conf cache
        if self._confCache is not None:
            cachePath = joinpath(cachedir, ZENMAKE_CONF_CACHE_PREFIX)
            db.saveTo(cachePath, self._confCache)

        # Waf always loads all *_cache.py files in directory 'c4che' during
        # build step. So it loads all stored variants even though they
        # aren't needed. And therefore it's better to save variants in
        # different files and load only needed ones.

        tasks = self.allTasks

        targetsData = {}
        envs = {}
        notStored = {}
        for taskParams in tasks.values():
            taskVariant = taskParams['$task.variant']

            # It's necessary to delete variant from conf.all_envs. Otherwise
            # Waf stores it in 'c4che'.
            env = self.all_envs.pop(taskVariant)
            envs[taskVariant] = utils.configSetToDict(env)

            # prepare some targets info
            taskName = taskParams['name']
            targetsData[taskName] = {
                'type' : taskParams['$tkind'],
                'name' : os.path.basename(taskParams['target']),
                'fname' : os.path.basename(taskParams['$real.target']),
                'dest-os' : env.DEST_OS,
                'dest-binfmt' : env.DEST_BINFMT,
            }
            if 'ver-num' in taskParams:
                targetsData[taskName]['ver-num'] = taskParams['ver-num']

            # don't store some params
            notStored[taskName] = [ (x, taskParams.pop(x, None)) \
                                        for x in _DONT_STORE_TASK_PARAMS ]

        buildtype = rootbconf.selectedBuildType

        tasksData = {
            'tasks'     : tasks,
            'taskenvs'  : envs,
            'buildtype' : buildtype,
            'depconfs'  : self.zmdepconfs,
            'ordered-tasknames' : [x['name'] for x in self.allOrderedTasks],
        }

        cachePath = assist.makeTasksCachePath(cachedir, buildtype)
        db.saveTo(cachePath, tasksData)

        # restore not stored params
        for taskParams in tasks.values():
            notStoredParams = notStored[taskParams['name']]
            for name, value in notStoredParams:
                taskParams[name] = value

        # save targets info to use as external dependency in other projects
        allDepTargets = [] if not self.zmdepconfs else self.zmdepconfs['$all-dep-targets']
        targetsData = {
            'rootdir' : rootdir,
            'btypedir' : relBTypeDir,
            'targets' : targetsData,
            'deptargets' : allDepTargets,
        }

        dbTargetsPath = assist.makeTargetsCachePath(cachedir, buildtype)
        dbfile = db.PyDBFile(dbTargetsPath)
        dbfile.save(targetsData)

    def getConfCache(self):
        """
        Get conf cache
        """
        return self._confCache

    # override
    def prepare_env(self, env):
        """
        Insert *PREFIX*, *BINDIR*, *LIBDIR* and other values into ``env``
        """

        rootbconf = self.bconfManager.root
        rootbconf.installDirVars.setAllTo(env)

    # override
    def post_recurse(self, node):
        # Avoid some actions from WafConfContext.post_recurse.
        # It's mostly for performance.
        # WafContext.Context.post_recurse(self, node)

        # this method must not be used
        raise NotImplementedError

    # override
    def store(self):

        self.saveCaches()
        super().store()

    def setDirectEnv(self, name, env):
        """ Set env without deriving and other actions """

        self.variant = name
        self.all_envs[name] = env

    def _cfgCompilerVarName(self, lang):
        """
        For selected language return WAF ConfigSet variable name to set/get
        compiler name in the form COMPILER_CXX, COMPILER_CC, etc.
        """

        return TOOLCHAIN_VARS[lang].get('cfgenv-compiler',
            'COMPILER_%s' % ToolchainVars.cfgVarToSetToolchain(lang))

    def loadTool(self, tool, **kwargs):
        """
        Load tool/toolchain from Waf or another places
        Version of loadTool for configure context.
        """

        startMsg = 'Checking for %r' % tool

        quiet = kwargs.get('quiet', False)
        if quiet:
            self.in_msg += 1

        toolEnv = None
        try:
            try:
                self.startMsg(startMsg)
                toolInfo = self._loadTool(tool, **kwargs)
            except waferror.ConfigurationError as ex:
                self.endMsg(False)
                if 'CXX=g++48' in ex.msg:
                    msg = 'Could not find gcc/g++ (only Clang)'
                    raise waferror.ConfigurationError(msg)
                raise
            else:
                endMsg = True
                toolEnv = toolInfo[1]
                for lang in toolchains.getLangs(tool):
                    var = ToolchainVars.cfgVarToSetToolchain(lang)
                    if toolEnv[var]:
                        # The COMPILER_%LANG% vars are almost useless because
                        # of existing vars like CXX, CC, etc. But in some rare
                        # places Waf checks and uses these vars.
                        varName = self._cfgCompilerVarName(lang)
                        toolEnv[varName] = tool

                        endMsg = toolEnv.get_flat(var)
                        break
                self.endMsg(endMsg)
        finally:
            if quiet:
                self.in_msg -= 1

        return toolEnv

    def _getToolchainSysEnvVals(self, sysEnvToolVars, actualToolchains):

        sysEnvToolVals = []
        for var, val in sysEnvToolVars.items():
            lang = ToolchainVars.langBySysVarToSetToolchain(var)
            if not lang:
                continue
            if val in actualToolchains:
                # This val is a name of a toolchain, not a path to it, so it is
                # necessery to remove this var from environ otherwise
                # ctx.find_program will not try to find this toolchain

                # DON'T remove var from os.environ: it breaks saving of env vars
                # in ZenMake metafile (writeZenMakeMetaFile) and the autoconf
                # feature doesn't work correctly
                self.environ.pop(var, None)
            else:
                # Value from OS env is not a name of a toolchain
                # (it can be path to toolchain) and
                # therefore it should be set auto-* for toolchain name
                # ZenMake detects actual name later.
                val = _genToolAutoName(lang)
            sysEnvToolVals.append((lang, val))

        return sysEnvToolVals

    def handleToolchains(self, bconf):
        """
        Handle all toolchains from current build tasks.
        Returns unique names of all toolchains.
        """

        customToolchains = bconf.customToolchains
        toolchainVars = ToolchainVars.allSysVarsToSetToolchain()
        flagVars = ToolchainVars.allSysFlagVars()

        actualToolchains = set(toolchains.getAllNames(withAuto = True))
        # customToolchains can contain unknown custom names
        actualToolchains.update(customToolchains.keys())

        # OS env vars
        osenv = os.environ
        sysEnvToolVars = \
            { var:osenv[var] for var in toolchainVars if var in osenv }
        sysEnvFlagVars = \
            { var:osenv[var].split() for var in flagVars if var in osenv}

        sysEnvToolVals = self._getToolchainSysEnvVals(
                                    sysEnvToolVars, actualToolchains)

        toolchainSettings = self._toolchainSettings[bconf.path] = AutoDict()
        toolchainSettings.update(customToolchains)

        for toolchain in tuple(actualToolchains):
            if toolchain in customToolchains and toolchain in TOOL_AUTO_NAMES:
                msg = "%r is not valid name" % toolchain
                msg += " in the variable 'toolchains'"
                raise error.ZenMakeConfError(msg, confpath = bconf.path)

            settings = toolchainSettings[toolchain]

            # OS env vars
            settings.vars.update(sysEnvToolVars)
            settings.vars.update(sysEnvFlagVars)
            settings.kind = toolchain if not settings.kind else settings.kind

        toolchainNames = set()

        for taskParams in bconf.tasks.values():

            features = toListSimple(taskParams.get('features', []))
            _toolchains = []

            # handle env vars to set toolchain
            for lang, val in sysEnvToolVals:
                if lang in features:
                    _toolchains.append(val)

            # try to get from the task
            if not _toolchains:
                _toolchains = toList(taskParams.get('toolchain', []))

            if not _toolchains:
                # try to use auto-*
                _toolchains = set()
                for feature in features:
                    lang = TASK_TARGET_FEATURES_TO_LANG.get(feature)
                    if not lang and feature in TASK_LANG_FEATURES:
                        lang = feature
                    if lang:
                        _toolchains.add(_genToolAutoName(lang))
                _toolchains = list(_toolchains)

            toolchainNames.update(_toolchains)

            # store result in task
            taskParams['toolchain'] = _toolchains

        toolchainNames = tuple(toolchainNames)
        return toolchainNames

    def loadToolchains(self, bconf):
        """
        Load all selected toolchains
        """

        toolchainNames = self.handleToolchains(bconf)
        self._checkToolchainNames(bconf)

        toolchainsEnvs = self._toolchainEnvs
        oldEnvName = self.variant
        toolchainSettings = self._toolchainSettings[bconf.path]
        detectedToolNames = {}
        emptyEnv = ConfigSet()

        def loadToolchain(toolchain):

            if toolchain in toolchainsEnvs:
                #don't load again
                return

            self.setenv(toolchain, env = emptyEnv)

            toolId = ''
            toolSettings = toolchainSettings[toolchain]

            for var, val in toolSettings.vars.items():
                lang = ToolchainVars.langBySysVarToSetToolchain(var)
                if not lang:
                    # it's not toolchain var
                    continue
                if val and pathexists(val[0]):
                    self.env[var] = val
                toolId += '%s=%r ' % (var, val)

            allowedNames = toolchains.getAllNames(withAuto = True)
            if toolSettings.kind not in allowedNames:
                msg = "toolchains.%s" % toolchain
                msg += " must have field 'kind' with one of the values: "
                msg += str(allowedNames)[1:-1]
                raise error.ZenMakeConfError(msg, confpath = bconf.path)

            # toolchain   - name of a system or custom toolchain
            # toolForLoad - name of module for toolchain
            toolForLoad = toolSettings.kind

            if toolForLoad in TOOL_AUTO_NAMES:
                lang = toolForLoad[5:]
                detectedToolname, toolenv = self._loadDetectedToolchain(lang, toolId)
                detectedToolNames[toolForLoad] = detectedToolname
                if toolchain in TOOL_AUTO_NAMES:
                    toolchainsEnvs[toolchain] = toolenv # to avoid reloading
                    toolchain = detectedToolname
            else:
                toolenv = self.loadTool(toolForLoad, id = toolId)

            toolchainsEnvs[toolchain] = self.env = toolenv

        for name in toolchainNames:
            loadToolchain(name)

        if detectedToolNames:
            # replace all auto-* in build tasks with detected toolchains
            for taskParams in bconf.tasks.values():
                taskParams['toolchain'] = \
                    [detectedToolNames.get(t, t) for t in taskParams['toolchain']]

        # switch to old env due to calls of 'loadToolchain'
        self.variant = oldEnvName

        return toolchainsEnvs

    def getToolchainEnvs(self):
        """
        Get envs for all loaded toolchains
        """

        return self._toolchainEnvs

    def getToolchainSettings(self, bconfpath):
        """
        Get toolchain settings for loaded toolchains in specific bconf
        """

        return self._toolchainSettings[bconfpath]

    def addExtraMonitFiles(self, bconf):
        """
        Add extra file paths to monitor for autoconfig feature
        """

        files = bconf.general.get('monitor-files')
        if not files:
            return
        for path in files.abspaths():
            if not os.path.isfile(path):
                msg = "Error in the file %r:\n" % bconf.path
                msg += "File path %r " % path
                msg += "from the general.monitor-files doesn't exist"
                self.fatal(msg)
            self.monitFiles.append(path)

    def mergeTasks(self):
        """
        Merge all tasks from all buildconf files.
        It makes self.allTasks as a dict with all tasks.
        """

        tasks = {}
        for bconf in self.bconfManager.configs:
            newtasks = bconf.tasks
            for taskParams in newtasks.values():
                assert taskParams.get('$bconf', bconf) == bconf
                taskParams['$bconf'] = bconf
                sameNameTask = tasks.get(taskParams['name'])
                if sameNameTask is not None:
                    msg = "There are two tasks with the same name %r" % taskParams['name']
                    msg += " in buildconf files:"
                    msg += "\n  %s" % sameNameTask['$bconf'].path
                    msg += "\n  %s" % bconf.path
                    raise error.ZenMakeConfError(msg)

            tasks.update(newtasks)

        self.allTasks = tasks

    def runConfigActions(self):
        """
        Run supported configuration actions: checks/others
        """
        configActions.runActions(self)

    def configureTaskParams(self):
        """
        Handle some known task params that can be handled at configure stage.
        """

        for taskParams in self.allOrderedTasks:
            bconf = taskParams['$bconf']

            assist.handleTaskIncludesParam(taskParams, bconf.startdir)
            assist.handleTaskLibPathParams(taskParams)

            self._handleMonitLibs(taskParams)

            #counter for the object file extension
            taskParams['objfile-index'] = self._calcObjectsIndex(bconf, taskParams)

            # should be called after handling of 'casual' params
            self._handleTaskExportParams(taskParams)

    def _prepareBConfParams(self, bconf):

        def prepareTaskParams(hooks, taskparams):

            for hookInfo in hooks:
                paramName = hookInfo[0]
                handler   = hookInfo[1]
                param = taskparams.get(paramName)
                if param is not None:
                    taskparams[paramName] = handler(bconf, param)

                paramName += '.select'
                param = taskparams.get(paramName, {})
                for condition in param:
                    param[condition] = handler(bconf, param[condition])

        for taskParams in bconf.tasks.values():
            prepareTaskParams(BUILDCONF_PREPARE_TASKPARAMS, taskParams)

    def _prepareBConfs(self):

        configs = self.bconfManager.configs
        for bconf in configs:
            self._prepareBConfParams(bconf)

    def _setupTaskTarget(self, taskParams, taskEnv, btypeDir):

        features = taskParams['features']
        targetKind = lang = None
        for feature in features:
            lang = TASK_TARGET_FEATURES_TO_LANG.get(feature)
            if lang is not None:
                targetKind = feature[len(lang):]
                break
        taskParams['$tlang'] = lang
        taskParams['$tkind'] = targetKind

        patterns = {}
        if lang:
            for kind in TASK_TARGET_KINDS:
                key = '%s%s_PATTERN' % (lang, kind)
                pattern = taskEnv[key]
                if pattern:
                    patterns[kind] = pattern
        taskParams['$tpatterns'] = patterns

        taskName = taskParams['name']

        normalizeTarget = taskParams.get('normalize-target-name', False)
        target = taskParams.get('target', taskName)
        if target:
            if normalizeTarget:
                target = utils.normalizeForFileName(target, spaceAsDash = True)
            targetPath = joinpath(btypeDir, target)
            taskParams['target'] = targetPath

            env = self.all_envs[taskParams['$task.variant']]
            pattern = patterns.get(targetKind)
            realTarget = assist.makeTargetRealName(targetPath, targetKind, pattern,
                                                   env, taskParams.get('ver-num'))
        else:
            realTarget = taskParams['target'] = ''

        taskParams['$real.target'] = realTarget
        taskParams['$runnable'] = targetKind == 'program'

    def _preconfigureTasks(self):

        rootbconf = self.bconfManager.root
        buildtype = rootbconf.selectedBuildType
        btypeDir = rootbconf.selectedBuildTypeDir
        defaultLibVersion = rootbconf.defaultLibVersion

        rootEnv = self.all_envs['']
        emptyEnv = ConfigSet()
        toolchainEnvs = self.getToolchainEnvs()
        allTasks = self.allTasks

        for taskParams in self.allOrderedTasks:

            taskName = taskParams['name']

            # make variant name for each task: 'buildtype.taskname'
            taskVariant = assist.makeTaskVariantName(buildtype, taskName)
            # store it
            taskParams['$task.variant'] = taskVariant

            assert taskVariant not in self.all_envs

            # set up env with toolchain for task
            _toolchains = taskParams['toolchain']
            if _toolchains:
                baseEnv = toolchainEnvs[_toolchains[0]]
                if len(_toolchains) > 1:
                    # make copy of env to avoid using 'update' on original
                    # toolchain env
                    baseEnv = utils.copyEnv(baseEnv)
                for toolname in _toolchains[1:]:
                    baseEnv.update(toolchainEnvs[toolname])
            else:
                needToolchain = set(taskParams['features']) & TASK_LANG_FEATURES
                if needToolchain:
                    msg = "No toolchain for task %r found." % taskName
                    msg += " Is buildconf correct?"
                    self.fatal(msg)
                else:
                    baseEnv = emptyEnv

            # Create env for task
            # Do deepcopy instead of baseEnv.derive() because an access to
            # isolated env will be faster
            taskEnv = utils.deepcopyEnv(baseEnv)

            # make task env complete
            taskEnv.parent = rootEnv

            # conf.setenv with unknown name or non-empty env makes deriving or
            # creates the new object and it is not really needed here
            self.setDirectEnv(taskVariant, taskEnv)

            if defaultLibVersion and 'ver-num' not in taskParams:
                taskParams['ver-num'] = defaultLibVersion

            taskParams.setdefault('$ruse', [])
            for name in taskParams.get('use', []):
                depTaskParams = allTasks.get(name)
                if depTaskParams:
                    depTaskParams['$ruse'].append(taskName)

            self._setupTaskTarget(taskParams, taskEnv, btypeDir)

    def _preconfigureRootEnv(self):

        rootbconf = self.bconfManager.root
        rootEnv = self.all_envs['']
        rootEnv['$builtin-vars'] = rootbconf.builtInVars

    def preconfigure(self):
        """
        Preconfigure. It's called by 'execute' before the actual 'configure'.
        """

        self._preconfigureRootEnv()

        configs = self.bconfManager.configs
        for bconf in configs:

            # set context path
            self.path = self.getPathNode(bconf.confdir)

            tasks = bconf.tasks

            # it's necessary to handle 'toolchain.select' before loading of toolchains
            for taskParams in tasks.values():
                handleOneTaskParamSelect(bconf, taskParams, 'toolchain')

            # load all toolchains envs
            self.loadToolchains(bconf)

            # Other '*.select' params must be handled after loading of toolchains
            handleTaskParamSelects(bconf)

            # remove disabled tasks after processing '*.select' params
            disabledTasks = [x['name'] for x in tasks.values() if not x.get('enabled', True)]
            for name in disabledTasks:
                tasks.pop(name)

        self.mergeTasks()

        if not self.allTasks:
            msg = "There are no actual tasks to run. Nothing to do."
            raise error.ZenMakeConfError(msg)

        # ordering must be after handling of 'use.select'
        self.allOrderedTasks = assist.orderTasksByLocalDeps(self.allTasks)

        toolchainEnvs = self.getToolchainEnvs()

        # Remove toolchain envs from self.all_envs
        # to avoid potential name conflicts and to free mem
        for toolchain in toolchainEnvs:
            self.all_envs.pop(toolchain, None)

        self._preconfigureTasks()

        # switch current env to the root env
        self.setenv('')

    # override
    def execute(self):

        environmon.doMonitoring = True

        self._prepareBConfs()

        bconf = self.bconfManager.root
        bconfPaths = bconf.confPaths

        # See details here: https://gitlab.com/ita1024/waf/issues/1563
        # It's not needed anymore
        #self.env.NO_LOCK_IN_RUN = True
        #self.env.NO_LOCK_IN_TOP = True

        self.init_dirs()

        self.cachedir = self.bldnode.make_node(WAF_CACHE_DIRNAME)
        self.cachedir.mkdir()

        if bconfPaths.zmcachedir != self.cachedir.abspath():
            try:
                os.makedirs(bconfPaths.zmcachedir)
            except OSError:
                pass

        path = joinpath(self.bldnode.abspath(), WAF_CONFIG_LOG)
        self.logger = log.makeLogger(path, 'cfg')

        projectDesc = "%s (ver: %s)" % (bconf.projectName, bconf.projectVersion)
        pyDesc = "%s (%s)" % (platform.python_version(), platform.python_implementation())

        cliArgs = [sys.argv[0]] + cli.selected.orig
        confHeaderParams = {
            'now'     : time.ctime(),
            'zmver'   : version.current(),
            'wafver'  : WafContext.WAFVERSION,
            'wafabi'  : WafContext.ABI,
            'pyver'   : pyDesc,
            'systype' : sys.platform,
            'args'    : " ".join(cliArgs),
            'prj'     : projectDesc,
        }

        self.to_log(CONFLOG_HEADER_TEMPLATE % confHeaderParams)
        self.msg('Setting top to', self.srcnode.abspath())
        self.msg('Setting out to', self.bldnode.abspath())

        if id(self.srcnode) == id(self.bldnode):
            log.warn('Setting startdir == buildout')
        elif id(self.path) != id(self.srcnode):
            if self.srcnode.is_child_of(self.path):
                log.warn('Are you certain that you do not want to set top="." ?')

        self.loadCaches()
        self.preconfigure()

        # prepare external dep rules to run
        edeps.preconfigureExternalDeps(self)

        # run external dep 'configure' rules and gather needed info after them
        edeps.produceExternalDeps(self)
        edeps.finishExternalDepsConfig(self)

        # finally run rest configuration including conf tests
        WafContext.Context.execute(self)

        # It is better to check deps in 'use' after conf checks
        self._checkTaskDepsInUse()

        if self.zmdepconfs:
            # insert libs/stlibs into params 'libs'/'stlibs' after conf actions
            # to avoid problems with some cont tests (check-libs)
            edeps.applyExternalDepLibsToTasks(self.allOrderedTasks)

        # store necessary info
        self.store()

        environmon.doMonitoring = False

        instanceCache = self.zmcache
        if not instanceCache.get('confpaths-added-to-monit', False):
            self.monitFiles.extend([x.path for x in self.bconfManager.configs])
            instanceCache['confpaths-added-to-monit'] = True

        WafContext.top_dir = self.srcnode.abspath()
        WafContext.out_dir = self.bldnode.abspath()

        self.zmMetaConfAttrs.update({
            'last-python-ver': '.'.join(str(x) for x in sys.version_info[:3]),
            'last-dbformat': db.getformat(),
        })
        zmMetaFilePath = bconfPaths.zmmetafile

        zmmeta = AutoDict(
            monitfiles = self.monitFiles,
            attrs = self.zmMetaConfAttrs,
            buildtype = bconf.selectedBuildType,
            cliargs = cli.selected.args,
            envvars = self._gatherMonitoredEnvVars(),
        )

        assist.writeZenMakeMetaFile(zmMetaFilePath, zmmeta, self.zmMetaConf())

@conf
def find_program(self, filename, **kwargs):
    """
    It's replacement for waflib.Configure.find_program to provide some
    additional abilities.
    """
    # pylint: disable = invalid-name

    filename = utils.toListSimple(filename)

    # simple caching
    useCache = all(x not in kwargs for x in ('environ', 'exts', 'value'))
    if useCache:
        cache = _cache.setdefault('find-program', {})
        pathList = kwargs.get('path_list')
        pathList = tuple(pathList) if pathList else None
        filenameKey = (tuple(filename), kwargs.get('interpreter'), pathList)
        result = cache.get(filenameKey)
        if result is not None:
            kwargs['value'] = result
            kwargs['endmsg-postfix'] = ' (cached)'

    result = wafFindProgram(self, filename, **kwargs)

    if useCache:
        cache[filenameKey] = result
    return result

@conf
def find_binary(_, filenames, exts, paths):
    """
    It's replacement for waflib.Configure.find_binary to fix some problems.
    """
    # pylint: disable = invalid-name

    expanduser = os.path.expanduser

    for name in filenames:
        for ext in exts:
            exeName = name + ext
            if isabspath(exeName):
                # zero-byte files cannot be used
                if isfile(exeName) and getfsize(exeName):
                    return exeName
            else:
                for path in paths:
                    fullpath = expanduser(joinpath(path, exeName))
                    # zero-byte files cannot be used
                    if isfile(fullpath) and getfsize(fullpath):
                        return fullpath
    return None
