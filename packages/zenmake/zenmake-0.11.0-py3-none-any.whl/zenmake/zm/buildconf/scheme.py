# coding=utf-8
#

"""
 Copyright (c) 2019, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

from copy import deepcopy
import re

from zm.constants import KNOWN_PLATFORMS, TASK_TARGET_KINDS
from zm.pyutils import stringtype
from zm.utils import toList
from zm.error import ZenMakeConfValueError
from zm.cli import config as cliConfig
from zm.buildconf.types import PATHS_SCHEME, ANYSTR_KEY
from zm.buildconf.sugar import genSugarSchemes
from zm.features import ConfValidation

_RE_VER_NUM = re.compile(r"^(0|[1-9]\d*)(\.(0|[1-9]\d*)){0,2}?$")
_RE_CONDNAME = re.compile(r"^[\w\d+-_]+$", re.ASCII)

def _checkVerNum(_, value, fullkey):

    if value and not _RE_VER_NUM.match(value):
        msg = "Value %r is invalid version number" % value
        msg += " for the param %r." % fullkey
        raise ZenMakeConfValueError(msg)

def _checkCondName(_, value, fullkey):

    if not value:
        msg = "Value  cannot be empty"
        msg += " for the param %r." % fullkey
        raise ZenMakeConfValueError(msg)

    if value == 'default':
        msg = "The 'default' value is not allowed"
        msg += " for the param %r." % fullkey
        raise ZenMakeConfValueError(msg)

    if not _RE_CONDNAME.match(value):
        msg = "Value %r is invalid" % value
        msg += " for the param %r." % fullkey
        raise ZenMakeConfValueError(msg)

def _checkBuildtypeName(conf, value, fullkey):

    allowed = []
    try:
        allowed.extend(conf['buildtypes'].keys())
    except AttributeError:
        pass

    allowed = set(allowed)
    if 'default' in allowed:
        allowed.remove('default')

    if allowed:
        if value not in allowed:
            msg = "Value %r is invalid" % value
            msg += " for the param %r." % fullkey
            msg = '%s\nAllowed values: %s' %(msg, str(list(allowed))[1:-1])
            raise ZenMakeConfValueError(msg)
    else:
        if value:
            msg = "Value %r is invalid" % value
            msg += " for the param %r." % fullkey
            msg += '\nIt must be empty string.'
            raise ZenMakeConfValueError(msg)

def _genSameSchemeDict(keys, scheme):
    return { k:scheme for k in keys }

def _genConfActionsScheme(confnode, fullkey):

    # pylint: disable = unused-argument

    # conf actions are in a list where each item has own scheme according 'do'
    scheme = {
        'type': 'list',
        'vars-type' : ('dict', 'func'),
        'dict-vars' : _genConfActionsDictVarsScheme
    }

    return scheme

_actionToVars = {
    'call-pyfunc' : {
        'func': { 'type': 'func' },
    },
    'find-program' : {
        'names' : { 'type': ('str', 'list-of-strs') },
        'paths' : { 'type': ('str', 'list-of-strs'),
                    'traits': ['list-of-paths', 'abs'] },
        'var':    { 'type': 'str' },
    },
    'find-file' : {
        'names' : { 'type': ('str', 'list-of-strs') },
        'paths' : { 'type': ('str', 'list-of-strs'),
                    'traits': ['list-of-paths', 'abs'] },
        'var':    { 'type': 'str' },
    },
    'check-headers' : {
        'names' :   { 'type': ('str', 'list-of-strs') },
        'defname' : { 'type': 'str' },
        'defines' : { 'type': ('str', 'list-of-strs') },
    },
    'check-libs' : {
        'names' :      { 'type': ('str', 'list-of-strs') },
        'fromtask' :   { 'type': 'bool' },
        'autodefine' : { 'type': 'bool' },
        'defines' :    { 'type': ('str', 'list-of-strs') },
    },
    'check-code' : {
        'label' :   { 'type': 'str' },
        'text' :    { 'type': 'str' },
        'file' :    { 'type': 'str' },
        'defname' : { 'type': 'str' },
        'defines' : { 'type': ('str', 'list-of-strs') },
        'execute' : { 'type': 'bool' },
    },
    'pkgconfig' : {
        'toolname' : { 'type': 'str' },
        'toolpaths' : { 'type': ('str', 'list-of-strs'),
                        'traits': ['list-of-paths', 'abs'] },
        'packages' : { 'type': 'str' },
        'cflags' : { 'type': 'bool' },
        'libs' : { 'type': 'bool' },
        'static' : { 'type': 'bool' },
        'defnames' : {
            'type' : ('bool', 'vars-in-dict'),
            'keys-kind' : 'anystr',
            'vars-type' : 'dict',
            'vars' : {
                'have' : { 'type': ('bool', 'str') },
                'version' : { 'type': ('bool', 'str') },
            },
        },
        'def-pkg-vars' : {
            'type': 'dict',
            'vars' : { ANYSTR_KEY : { 'type': 'str' } },
        },
        'tool-atleast-version' : { 'type': 'str' },
        'pkg-version' : { 'type': 'bool' },
    },
    'toolconfig' : {
        'msg' : { 'type': 'str' },
        'toolname' : { 'type': 'str' },
        'toolpaths' : {
            'type': ('str', 'list-of-strs'),
            'traits' : ['list-of-paths', 'abs']
        },
        'args' : { 'type': ('str', 'list-of-strs') },
        'parse-as' : {
            'type': 'str',
            'allowed': ('none', 'entire', 'flags-libs'),
        },
        'static' : { 'type': 'bool' },
        'defname' : { 'type': 'str' },
        'var':    { 'type': 'str' },
    },
    'write-config-header' : {
        'file' : { 'type': 'str' },
        'guard': { 'type': 'str' },
        'remove-defines' : { 'type': 'bool' },
    },
    'parallel' : {
        'tryall' : { 'type': 'bool' },
        'actions' : _genConfActionsScheme,
    },
}

def _genConfActionsDictVarsScheme(confnode, fullkey):

    # common params for any conf action
    schemeDictVars = {
        'do' :       {
            'type': 'str',
            'allowed' : set(_actionToVars.keys()),
        },
        'mandatory' : { 'type': 'bool' },
    }

    keyParts = fullkey.split('.')
    if keyParts[-2] == 'actions':
        # add specific params for parallel conf actions
        schemeDictVars.update({
            'id' :     { 'type': 'str' },
            'before' : { 'type': 'str' },
            'after' :  { 'type': 'str' },
        })

    action = confnode.get('do', '')
    if isinstance(action, stringtype):
        # add params specific for this action
        schemeDictVars.update(_actionToVars.get(action, {}))
    return schemeDictVars

def _genInstallFilesScheme(confnode, fullkey):

    # pylint: disable = unused-argument

    scheme = {
        'type' : 'list',
        'vars-type' : ('dict', ),
        'dict-vars' : _genInstallFilesDictVarsScheme
    }

    return scheme

_installTypeSpecVars = {
    'copy' : {
        'src'   : PATHS_SCHEME,
        'dst'   : { 'type': 'str', 'traits': ['one-path', 'abs'] },
        'chmod' : { 'type' : ('int', 'str'), },
        'user'  : { 'type': 'str' },
        'group' : { 'type': 'str' },
        'follow-symlinks' : { 'type': 'bool', },
    },
    'copy-as' : {
        'src'   : { 'type': 'str', 'traits': ['one-path', 'abs'] },
        'dst'   : { 'type': 'str', 'traits': ['one-path', 'abs'] },
        'chmod' : { 'type' : ('int', 'str'), },
        'user'  : { 'type': 'str' },
        'group' : { 'type': 'str' },
        'follow-symlink' : { 'type': 'bool', },
    },
    'symlink' : {
        'src' : { 'type': 'str', 'traits': ['one-path', 'abs'] },
        'symlink' : { 'type': 'str', 'traits': ['one-path', 'abs'] },
        'user'  : { 'type': 'str' },
        'group' : { 'type': 'str' },
        'relative' : { 'type': 'bool', },
    },
}

def _genInstallFilesDictVarsScheme(confnode, fullkey):

    # common params
    schemeDictVars = {
        'do' :       {
            'type': 'str',
            'allowed' : ('copy', 'copy-as', 'symlink'),
        },
    }

    action = confnode.get('do')
    if not action:
        action = 'symlink' if 'symlink' in confnode else 'copy'
    confnode['do'] = action

    if 'src' not in confnode:
        msg = "There is no 'src' in the param %r." % fullkey
        raise ZenMakeConfValueError(msg)

    dstParamName = 'symlink' if action == 'symlink' else 'dst'
    if dstParamName not in confnode:
        msg = "There is no %r in the param %r." % (dstParamName, fullkey)
        raise ZenMakeConfValueError(msg)

    schemeDictVars.update(_installTypeSpecVars[action])

    return schemeDictVars

def _genCliOptionsVarsScheme(confnode, fullkey):

    # pylint: disable = unused-argument

    cmdNames = [ x.name for x in cliConfig.commands ]
    optNames = []
    for options in (cliConfig.options, cliConfig.installoptions):
        optNames.extend([ x.names[-1].replace('-', '', 2) for x in options ])

    optionsOptDictTypeScheme = _genSameSchemeDict(
        cmdNames + ['any'],
        { 'type' : ('bool', 'int', 'str'), }
    )

    scheme = _genSameSchemeDict(
        optNames,
        {
            'type' : ('bool', 'int', 'str', 'dict'),
            'allow-unknown-keys' : False,
            'dict-vars' : optionsOptDictTypeScheme,
        }
    )

    return scheme

_DEP_RULE_SCHEME = {
    'type': ('str', 'dict',),
    'dict-vars' : {
        'trigger' : {
            'type': 'dict',
            'vars' : {
                'always' : { 'type': 'bool' },
                'no-targets' : { 'type': 'bool' },
                'paths-exist' : PATHS_SCHEME,
                'paths-dont-exist' : PATHS_SCHEME,
                'func' : { 'type': 'func', 'traits': ['func'] },
                'env' : {
                    'type': 'dict',
                    'vars' : { ANYSTR_KEY : { 'type': 'str' } },
                },
            },
        },
        'cmd' : { 'type': 'str' },
        'cwd' : { 'type': 'str', 'traits': ['one-path'] },
        'env' : {
            'type': 'dict',
            'vars' : { ANYSTR_KEY : { 'type': 'str' } },
        },
        'timeout' : { 'type': 'int' },
        'shell' : { 'type': 'bool' },
        'zm-commands' : { 'type': ('str', 'list-of-strs') },
    },
}

_ALLOWED_DEP_TARGET_TYPES = frozenset(list(TASK_TARGET_KINDS) + ['file'])

taskscheme = {
    'target' :          { 'type': 'str' },
    'features' :        { 'type': ('str', 'list-of-strs') },
    'use' :             { 'type': ('str', 'list-of-strs') },
    'source' :          PATHS_SCHEME,
    'toolchain' :       { 'type': ('str', 'list-of-strs') },
    'libs' :            { 'type': ('str', 'list-of-strs') },
    'libpath':          { 'type': ('str', 'list-of-strs'), 'traits': ['list-of-paths'] },
    'monitlibs':        { 'type': ('bool', 'str', 'list-of-strs') },
    'stlibs' :          { 'type': ('str', 'list-of-strs') },
    'stlibpath':        { 'type': ('str', 'list-of-strs'), 'traits': ['list-of-paths'] },
    'monitstlibs':      { 'type': ('bool', 'str', 'list-of-strs') },
    'rpath' :           { 'type': ('str', 'list-of-strs') },
    'ver-num' :         { 'type': 'str', 'allowed' : _checkVerNum },
    'includes':         { 'type': ('str', 'list-of-strs'), 'traits': ['list-of-paths'] },
    'linkflags' :       { 'type': ('str', 'list-of-strs') },
    'ldflags' :         { 'type': ('str', 'list-of-strs') },
    'defines' :         { 'type': ('str', 'list-of-strs') },
    'install-path' :    { 'type': ('bool', 'str'), 'traits': ['one-path', 'abs'] },
    'install-files' :   _genInstallFilesScheme,
    'configure' :       _genConfActionsScheme,
    'group-dependent-tasks' : { 'type': 'bool' },
    'normalize-target-name' : { 'type': 'bool' },
    'enabled'       : { 'type': 'bool' },
    'objfile-index' : { 'type': 'int' },
}

############ EXTEND TASK PARAMS

def _checkExportParams(_, value, fullkey):

    for val in toList(value):
        if val not in EXPORTING_TASK_PARAMS_S:
            msg = "Value %r is invalid" % val
            msg += " for the param %r." % fullkey
            raise ZenMakeConfValueError(msg)

def _addExportParamsToScheme(tscheme, exportingParams):

    tscheme['export'] = {
        'type': ('str', 'list-of-strs'),
        'allowed': _checkExportParams,
    }

    for param in exportingParams:
        if param == 'config-results':
            paramScheme = { 'type': 'bool' }
        else:
            paramScheme = deepcopy(tscheme[param])
            _type = paramScheme['type']
            if not isinstance(_type, (tuple, list)):
                _type = (_type,)
            else:
                _type = tuple(_type)
            paramScheme['type'] = ('bool', ) + _type
        tscheme['export-%s' % param] = paramScheme

def _addSelectToParams(scheme, paramNames = None):
    """
    Add '.select' variant to param from scheme
    """

    if paramNames is None:
        paramNames = tuple(scheme.keys())

    for name in paramNames:
        origScheme = scheme[name]
        scheme['%s.select' % name] = {
            'type' : 'dict',
            'vars' : {
                'default' : origScheme,
                ANYSTR_KEY : origScheme,
            },
        }

def _applyExportAndSelectedTaskParams():

    featuresTaskSchemes = ConfValidation.getTaskSchemeSpecs()

    #---------- base params

    # It's necessary to save current list of keys before updating with values from features
    # to avoid mixing with unwanted values from features
    selectableParams = [x for x in taskscheme if x != 'features']

    taskscheme.update(featuresTaskSchemes['base'])

    #---------- export params
    exportingParams = [
        'includes', 'defines', 'config-results',
        'libpath', 'stlibpath', 'linkflags', 'ldflags',
    ]
    selectableParams.extend(['export-%s' % x for x in exportingParams])

    # Apply values from features
    exportingParams.extend(featuresTaskSchemes['export'])
    _addExportParamsToScheme(taskscheme, exportingParams)

    #---------- *.select params
    selectableParams.extend(featuresTaskSchemes['select'])
    _addSelectToParams(taskscheme, selectableParams)

    return tuple(exportingParams)

EXPORTING_TASK_PARAMS = _applyExportAndSelectedTaskParams()
EXPORTING_TASK_PARAMS_S = frozenset(EXPORTING_TASK_PARAMS)

###################################

confscheme = {
    # traits are not used for 'startdir', 'buildroot'/'realbuildroot'
    'startdir' : { 'type': 'str' },
    'buildroot' : { 'type': 'str' },
    'realbuildroot' : { 'type': 'str' },

    'general' : {
        'type' : 'dict',
        'vars' : {
            'autoconfig' : { 'type': 'bool' },
            'monitor-files' : {
                'type': ('str', 'list-of-strs'),
                'traits': ['list-of-paths'],
            },
            'hash-algo' : { 'type': 'str', 'allowed' : ('sha1', 'md5') },
            'db-format' : {
                'type': 'str',
                'allowed': ('py', 'pickle', 'msgpack'),
            },
            'provide-edep-targets' : { 'type': 'bool' },
            'build-work-dir-name' : { 'type': 'str' },
        },
    },
    'cliopts' : {
        'type' : 'dict',
        'vars' : _genCliOptionsVarsScheme,
    },
    'subdirs' : {
        'type': 'list-of-strs', 'traits': ['list-of-paths', 'abs']
    },
    'project' : {
        'type' : 'dict',
        'vars' : {
            'name' : { 'type': 'str' },
            'version' : { 'type': 'str' },
        },
    },
    'conditions' : {
        'type' : 'dict',
        'allowed-keys' : _checkCondName,
        'vars' : {
            ANYSTR_KEY : {
                'type' : 'dict',
                'dict-vars' : {
                    'platform' :  { 'type': ('str', 'list-of-strs') },
                    'host-os'  :  { 'type': ('str', 'list-of-strs') },
                    'distro'   :  { 'type': ('str', 'list-of-strs') },
                    'cpu-arch' :  { 'type': ('str', 'list-of-strs') },
                    'toolchain' : { 'type': ('str', 'list-of-strs') },
                    'task' :      { 'type': ('str', 'list-of-strs') },
                    'buildtype' : { 'type': ('str', 'list-of-strs') },
                    'env' :       { 'type': 'dict' },
                },
            },
        },
    },
    'edeps' : {
        'type' : 'vars-in-dict',
        'keys-kind' : 'anystr',
        'vars-type' : 'dict',
        'vars' : {
            'rootdir' :  { 'type': 'str', 'traits': ['one-path'] },
            'export-includes' : {
                'type': ('str', 'list-of-strs'),
                'traits': ['list-of-paths']
            },
            'targets' :  {
                'type': 'dict',
                'vars' : {
                    ANYSTR_KEY: {
                        'type': 'dict',
                        'vars': {
                            'dir'  : {'type' : 'str', 'traits' : ['one-path'] },
                            'type' : {'type' : 'str', 'allowed' : _ALLOWED_DEP_TARGET_TYPES },
                            'name' : {'type' : 'str' },
                            'ver-num' : { 'type': 'str', 'allowed' : _checkVerNum },
                            'fname' : {'type' : 'str' },
                            #'fallback' : {'type' : 'str' },
                        },
                    },
                },
            },
            'rules'   :  {
                'type': 'dict',
                'vars': {
                    'configure' : _DEP_RULE_SCHEME,
                    'build' : _DEP_RULE_SCHEME,
                    'test' : _DEP_RULE_SCHEME,
                    'clean' : _DEP_RULE_SCHEME,
                    'install' : _DEP_RULE_SCHEME,
                    'uninstall' : _DEP_RULE_SCHEME,
                }
            },
            'buildtypes-map' : {
                'type': 'dict',
                'vars' : {
                    ANYSTR_KEY : { 'type' : 'str' },
                },
            },
        },
    },
    'tasks' : {
        'type' : 'dict',
        'vars' : {
            ANYSTR_KEY : {
                'type' : 'dict',
                'vars' : taskscheme,
            },
        },
    },
    'buildtypes' : {
        'type' : 'dict',
        'vars' : {
            ANYSTR_KEY : {
                'type' : 'dict',
                'vars' : taskscheme,
            },
            'default' : {
                'type': ('dict', 'str'),
                'dict-vars' : {
                    k: { 'type': 'str' } for k in KNOWN_PLATFORMS + ('_', 'no-match')
                },
                'str-allowed': _checkBuildtypeName,
            },
        },
    },
    'toolchains' : {
        'type' : 'dict',
        'vars' : {
            ANYSTR_KEY : {
                'type' : 'dict',
                'vars' : {
                    'kind' : { 'type': 'str' },
                    ANYSTR_KEY : { 'type' : 'str' },
                },
            },
        },
    },
    'byfilter' : {
        'type' : 'list',
        'vars-type' : 'dict',
        'dict-allow-unknown-keys' : False,
        'dict-vars' : {
            'for' : {
                'type': ('dict', 'str'),
                'dict-vars' : {
                    'task' : { 'type': ('str', 'list-of-strs') },
                    'buildtype' : { 'type': ('str', 'list-of-strs') },
                    'platform' : { 'type': ('str', 'list-of-strs') },
                },
                'str-allowed': ('all',),
            },
            'not-for' : {
                'type': 'dict',
                'vars' : {
                    'task' : { 'type': ('str', 'list-of-strs') },
                    'buildtype' : { 'type': ('str', 'list-of-strs') },
                    'platform' : { 'type': ('str', 'list-of-strs') },
                },
            },
            'if' : {
                'type': ('str', 'bool'),
            },
            'set' : {
                'type' : 'dict',
                'vars' : taskscheme,
            },
        },
    },
}

KNOWN_TASK_PARAM_NAMES = frozenset(taskscheme.keys())
KNOWN_CONF_PARAM_NAMES = frozenset(confscheme.keys())
KNOWN_CONDITION_PARAM_NAMES = \
    frozenset(confscheme['conditions']['vars'][ANYSTR_KEY]['dict-vars'].keys())
KNOWN_CONF_ACTIONS = frozenset(_actionToVars.keys())

# Syntactic sugar constructions are not 'real' parameters because they
# are converted into other buildconf constructions
genSugarSchemes(confscheme)

KNOWN_CONF_SUGAR_NAMES = frozenset(confscheme.keys()) - KNOWN_CONF_PARAM_NAMES
