# coding=utf-8
#

"""
 Copyright (c) 2019, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

import sys
import os
from os import path
if sys.hexversion < 0x3050000:
    raise ImportError('Python >= 3.5 is required')

#pylint: disable=wrong-import-position
from zm import environmon
environmon.assignMonitoringTo(os, 'environ')

from zm.constants import CWD
from zm import utils, cli
from zm.pathutils import unfoldPath

joinpath = path.join

_indyCmd = {
    'zipapp'  : 'zm.zipapp',
    'version' : 'zm.version',
    'sysinfo' : 'zm.sysinfo',
}

def handleCLI(args, noBuildConf, options, cwd):
    """
    Handle CLI and return command object and waf cmd line
    """

    defaults = options if options else {}
    cmd = cli.parseAll(args, noBuildConf, defaults)
    cli.selected = cmd

    # Adjust some paths
    for param in ('buildroot', 'destdir'):
        val = cmd.args.get(param)
        if val:
            cmd.args[param] = unfoldPath(val, cwd)

    return cmd

def runIndyCmd(cmd):
    """
    Run independent command that doesn't use buildconf and Waf.
    """

    if cmd.name not in _indyCmd:
        raise NotImplementedError('Unknown command')

    moduleName = _indyCmd[cmd.name]
    module = utils.loadPyModule(moduleName, withImport = True)
    return module.Command().run(cmd.args)

def findTopLevelBuildConfDir(startdir):
    """
    Try to find top level dir with a buildconf file.
    Return None if file was not found.
    """

    from zm.buildconf.loader import findConfFile

    curdir = startdir
    found = None
    while curdir:
        if findConfFile(curdir):
            found = curdir

        nextdir = path.dirname(curdir)
        if nextdir == curdir:
            break
        curdir = nextdir

    return found

def loadTesting():
    """
    Check if it's testing mode and load testing mode if it's necessary
    """

    # Special flag for ZenMake testing
    testing = os.environ.get('ZENMAKE_TESTING_MODE', '')
    try:
        # value from os.environ is a string but it may be a digit
        if testing:
            testing = int(testing)
    except ValueError:
        pass

    if testing:
        # pylint: disable = unused-import
        import zm.testing

def run():
    """
    Prepare and run ZenMake and Waf with ZenMake stuff
    """

    # process buildconf and CLI
    from zm import log, error
    from zm.buildconf.processing import ConfManager as BuildConfManager

    noBuildConf = True
    cwd = CWD
    cmd = None

    try:

        # pylint: disable = unused-import
        # force loading *feature*_init modules before CLI
        from zm import features
        # pylint: enable = unused-import

        loadTesting()

        # We cannot to know if buildconf is changed while buildroot is unknown.
        # This information is stored in the file that is located in buildroot.
        # But buildroot can be set on the command line and we must to parse CLI
        # before processing of buildconf.

        bconfDir = findTopLevelBuildConfDir(cwd)
        noBuildConf = bconfDir is None
        cmd = handleCLI(sys.argv, noBuildConf, None, cwd)

        error.verbose = cmd.args.verbose

        if cmd.name in _indyCmd:
            return runIndyCmd(cmd)

        # Init color mode for logs. It's necessary because such an initialization
        # in waf.options.OptionsContext.init_logs happens too late.
        log.enableColorsByCli(cmd.args.color)

        if noBuildConf:
            log.error('Config buildconf.py/.yaml not found. Check one '
                      'exists in the project directory.')
            return 1

        def cliOptsHandler(defaults):
            return handleCLI(sys.argv, noBuildConf, defaults, cwd)

        bconfManager = BuildConfManager(bconfDir, clivars = cmd.args,
                                        clihandler = cliOptsHandler)
        bconf = bconfManager.root
        cmd = cli.selected

        from zm import db
        utils.setDefaultHashAlgo(bconf.general['hash-algo'])
        db.useformat(bconf.general['db-format'])

    except error.ZenMakeError as ex:
        verbose = 0
        if cmd:
            verbose = cmd.args.verbose
        if verbose > 1:
            log.pprint('RED', ex.fullmsg)
        log.error(ex.msg)
        sys.exit(1)
    except KeyboardInterrupt:
        log.pprint('RED', 'Interrupted')
        sys.exit(68)

    # start waf ecosystem
    from zm.waf import launcher
    launcher.run(cmd, bconfManager)

    return 0
