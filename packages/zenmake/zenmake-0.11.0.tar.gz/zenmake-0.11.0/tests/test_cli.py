# coding=utf-8
#

# pylint: disable = wildcard-import, unused-wildcard-import, unused-import
# pylint: disable = missing-docstring, invalid-name, wrong-import-order
# pylint: disable = no-member, attribute-defined-outside-init

"""
 Copyright (c) 2019, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

import sys
import os
from copy import deepcopy
import pytest
import tests.common as cmn
from zm.constants import APPNAME, CAP_APPNAME
from zm import cli, installdirvars

joinpath = os.path.join

INSTALL_DIRVAR_CLI_DEFAULTS = { k:None for k in installdirvars.VAR_NAMES }

@pytest.mark.usefixtures("unsetEnviron")
class TestCmds(object):

    @pytest.fixture(autouse = True)
    def setup(self):
        self.defaults = { 'buildtype': 'somedebug' }
        self.parser = cli.CmdLineParser('test', self.defaults)

    def _parseHelpArgs(self, args, capsys):
        # CLI prints help and does exit
        with pytest.raises(SystemExit) as cm:
            self.parser.parse(args)
        captured = capsys.readouterr()
        return cm.value.code, captured.out, captured.err

    def _testMainHelpMsg(self, args, capsys):
        ecode, out, err = self._parseHelpArgs(args, capsys)

        assert not err
        assert ecode == 0
        assert CAP_APPNAME in out
        assert 'based on the Waf build system' in out
        assert self.parser.parsed is not None
        assert self.parser.parsed.name == 'help'
        assert self.parser.parsed.args == {'topic': 'overview'}
        assert self.parser.parsed.wafline == []

    def _assertAllsForCmd(self, cmdname, checks, baseExpectedArgs):

        expectedArgs = None
        for check in checks:
            expectedArgs = deepcopy(baseExpectedArgs)
            expectedArgs.update(check['expectedArgsUpdate'])

            def assertAll(cmd, parsercmd):
                assert cmd is not None
                assert parsercmd is not None
                assert parsercmd == cmd
                assert cmd.name == cmdname
                assert cmd.args == expectedArgs
                # pylint: disable = cell-var-from-loop
                if 'wafArgs' in check:
                    assert sorted(check['wafArgs']) == sorted(parsercmd.wafline)

            # parser with explicit args
            cmd = self.parser.parse(check['args'])
            assertAll(cmd, self.parser.parsed)

            # parser with args from sys.argv
            oldargv = sys.argv
            sys.argv = [APPNAME] + check['args']
            cmd = self.parser.parse()
            sys.argv = oldargv
            assertAll(cmd, self.parser.parsed)

    def testEmpty(self, capsys):
        self._testMainHelpMsg([], capsys)

    def testHelp(self, capsys):
        self._testMainHelpMsg(['help'], capsys)

    def testHelpWrongTopic(self, capsys):
        args = ['help', 'qwerty']
        ecode, out, err = self._parseHelpArgs(args, capsys)
        assert not out
        assert 'Unknown command/topic' in err
        assert ecode != 0

    def testHelpForCmds(self, capsys):
        for cmd in cli.config.commands:
            args = ['help', cmd.name]
            ecode, out, err = self._parseHelpArgs(args, capsys)
            assert ecode == 0
            assert not err
            if cmd.name == 'help':
                assert 'show help' in out
            else:
                assert cmd.description.capitalize() in out

    def testCmdBuild(self):

        baseExpectedArgs = {
            'buildtype' : self.defaults['buildtype'],
            'jobs' : None,
            'configure': False,
            'color': 'auto',
            'clean': False,
            'progress': False,
            'cleanall': False,
            'distclean': False,
            'tasks': [],
            'verbose': 0,
            'verboseConfigure' : None,
            'verboseBuild' : None,
            'withTests': 'no',
            'runTests': 'none',
            'buildroot' : None,
            'forceExternalDeps' : False,
            'cacheCfgActionResults' : False,
        }
        baseExpectedArgs.update(INSTALL_DIRVAR_CLI_DEFAULTS)

        CMDNAME = 'build'
        CMNOPTS = ['--color=auto']

        checks = [
            dict(
                args = [CMDNAME],
                expectedArgsUpdate = {},
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '-b', 'release'],
                expectedArgsUpdate = {'buildtype': 'release'},
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--jobs', '22'],
                expectedArgsUpdate = {'jobs': 22},
                wafArgs = [CMDNAME, '--jobs=22'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--verbose'],
                expectedArgsUpdate = {'verbose': 1},
                wafArgs = [CMDNAME, '-v'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '-vvv'],
                expectedArgsUpdate = {'verbose': 3},
                wafArgs = [CMDNAME, '-vvv'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--configure'],
                expectedArgsUpdate = {'configure': True},
                wafArgs = ['configure', CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--clean'],
                expectedArgsUpdate = {'clean': True},
                wafArgs = ['clean', CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--clean-all'],
                expectedArgsUpdate = {'cleanall': True},
                wafArgs = ['cleanall', CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--distclean'],
                expectedArgsUpdate = {'distclean': True},
                wafArgs = ['distclean', CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--with-tests', 'yes'],
                expectedArgsUpdate = {'withTests': 'yes'},
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--run-tests', 'all'],
                expectedArgsUpdate = {'runTests': 'all'},
                wafArgs = [CMDNAME, 'test'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--run-tests', 'on-changes'],
                expectedArgsUpdate = {'runTests': 'on-changes'},
                wafArgs = [CMDNAME, 'test'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--progress'],
                expectedArgsUpdate = {'progress': True},
                wafArgs = [CMDNAME, '--progress'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--color', 'no'],
                expectedArgsUpdate = {'color': 'no'},
                wafArgs = [CMDNAME, '--color=no'] + CMNOPTS[1:],
            ),
            dict(
                args = [CMDNAME, 'sometask'],
                expectedArgsUpdate = {'tasks': ['sometask']},
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, 'sometask', 'anothertask'],
                expectedArgsUpdate = {'tasks': ['sometask', 'anothertask']},
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--buildroot', 'somedir'],
                expectedArgsUpdate = {'buildroot' : 'somedir'},
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
        ]

        self._assertAllsForCmd(CMDNAME, checks, baseExpectedArgs)

    def testCmdTest(self):

        baseExpectedArgs = {
            'buildtype' : self.defaults['buildtype'],
            'jobs' : None,
            'configure': False,
            'color': 'auto',
            'clean': False,
            'progress': False,
            'cleanall': False,
            'distclean': False,
            'tasks': [],
            'verbose': 0,
            'verboseConfigure' : None,
            'verboseBuild' : None,
            'withTests': 'yes',
            'runTests': 'all',
            'buildroot' : None,
            'forceExternalDeps' : False,
            'cacheCfgActionResults' : False,
        }
        baseExpectedArgs.update(INSTALL_DIRVAR_CLI_DEFAULTS)

        CMDNAME = 'test'
        CMNOPTS = ['--color=auto']

        checks = [
            dict(
                args = [CMDNAME],
                expectedArgsUpdate = {},
                wafArgs = ['build', CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '-b', 'release'],
                expectedArgsUpdate = {'buildtype': 'release'},
                wafArgs = ['build', CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--jobs', '22'],
                expectedArgsUpdate = {'jobs': 22},
                wafArgs = ['build', CMDNAME, '--jobs=22'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--verbose'],
                expectedArgsUpdate = {'verbose': 1},
                wafArgs = ['build', CMDNAME, '-v'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '-vvv'],
                expectedArgsUpdate = {'verbose': 3},
                wafArgs = ['build', CMDNAME, '-vvv'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--configure'],
                expectedArgsUpdate = {'configure': True},
                wafArgs = ['configure', 'build', CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--clean'],
                expectedArgsUpdate = {'clean': True},
                wafArgs = ['clean', 'build', CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--clean-all'],
                expectedArgsUpdate = {'cleanall': True},
                wafArgs = ['cleanall', 'build', CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--distclean'],
                expectedArgsUpdate = {'distclean': True},
                wafArgs = ['distclean', 'build', CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--with-tests', 'no'],
                expectedArgsUpdate = {'withTests': 'no'},
                wafArgs = ['build', CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--run-tests', 'none'],
                expectedArgsUpdate = {'runTests': 'none'},
                wafArgs = ['build', CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--run-tests', 'on-changes'],
                expectedArgsUpdate = {'runTests': 'on-changes'},
                wafArgs = ['build', CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--progress'],
                expectedArgsUpdate = {'progress': True},
                wafArgs = ['build', CMDNAME, '--progress'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--color', 'no'],
                expectedArgsUpdate = {'color': 'no'},
                wafArgs = ['build', CMDNAME, '--color=no'] + CMNOPTS[1:],
            ),
            dict(
                args = [CMDNAME, 'sometask'],
                expectedArgsUpdate = {'tasks': ['sometask']},
                wafArgs = ['build', CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, 'sometask', 'anothertask'],
                expectedArgsUpdate = {'tasks': ['sometask', 'anothertask']},
                wafArgs = ['build', CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--buildroot', os.getcwd()],
                expectedArgsUpdate = {'buildroot' : os.getcwd()},
                wafArgs = ['build', CMDNAME] + CMNOPTS,
            ),
        ]

        self._assertAllsForCmd(CMDNAME, checks, baseExpectedArgs)

    def testCmdConfigure(self):

        baseExpectedArgs = {
            'buildtype' : self.defaults['buildtype'],
            'color': 'auto',
            'cleanall': False,
            'distclean': False,
            'verbose': 0,
            'verboseConfigure' : None,
            'withTests': 'no',
            'buildroot' : None,
            'forceExternalDeps' : False,
            'cacheCfgActionResults' : False,
            'force' : False,
        }
        baseExpectedArgs.update(INSTALL_DIRVAR_CLI_DEFAULTS)

        CMDNAME = 'configure'
        CMNOPTS = ['--color=auto']

        checks = [
            dict(
                args = [CMDNAME],
                expectedArgsUpdate = {},
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '-b', 'release'],
                expectedArgsUpdate = {'buildtype': 'release'},
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--clean-all'],
                expectedArgsUpdate = {'cleanall': True},
                wafArgs = ['cleanall', CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--distclean'],
                expectedArgsUpdate = {'distclean': True},
                wafArgs = ['distclean', CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--verbose'],
                expectedArgsUpdate = {'verbose': 1},
                wafArgs = [CMDNAME, '-v'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '-vvv'],
                expectedArgsUpdate = {'verbose': 3},
                wafArgs = [CMDNAME, '-vvv'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--color', 'no'],
                expectedArgsUpdate = {'color': 'no'},
                wafArgs = [CMDNAME, '--color=no'] + CMNOPTS[1:],
            ),
            dict(
                args = [CMDNAME, '--buildroot', os.getcwd()],
                expectedArgsUpdate = {'buildroot' : os.getcwd()},
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
        ]

        self._assertAllsForCmd(CMDNAME, checks, baseExpectedArgs)

    def testCmdClean(self):

        baseExpectedArgs = {
            'buildtype' : self.defaults['buildtype'],
            'color': 'auto',
            'verbose': 0,
            'buildroot' : None,
            'forceExternalDeps' : False,
        }

        CMDNAME = 'clean'
        CMNOPTS = ['--color=auto',]

        checks = [
            dict(
                args = [CMDNAME],
                expectedArgsUpdate = {},
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '-b', 'release'],
                expectedArgsUpdate = {'buildtype': 'release'},
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--verbose'],
                expectedArgsUpdate = {'verbose': 1},
                wafArgs = [CMDNAME, '-v'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '-vvv'],
                expectedArgsUpdate = {'verbose': 3},
                wafArgs = [CMDNAME, '-vvv'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--color', 'no'],
                expectedArgsUpdate = {'color': 'no'},
                wafArgs = [CMDNAME, '--color=no'],
            ),
            dict(
                args = [CMDNAME, '--buildroot', os.getcwd()],
                expectedArgsUpdate = {'buildroot' : os.getcwd()},
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
        ]

        self._assertAllsForCmd(CMDNAME, checks, baseExpectedArgs)

    def testCmdDistclean(self):

        baseExpectedArgs = {
            'color': 'auto',
            'verbose': 0,
            'buildroot' : None,
        }

        CMDNAME = 'distclean'
        CMNOPTS = ['--color=auto',]

        checks = [
            dict(
                args = [CMDNAME],
                expectedArgsUpdate = {},
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--verbose'],
                expectedArgsUpdate = {'verbose': 1},
                wafArgs = [CMDNAME, '-v'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '-vvv'],
                expectedArgsUpdate = {'verbose': 3},
                wafArgs = [CMDNAME, '-vvv'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--color', 'no'],
                expectedArgsUpdate = {'color': 'no'},
                wafArgs = [CMDNAME, '--color=no'],
            ),
            dict(
                args = [CMDNAME, '--buildroot', os.getcwd()],
                expectedArgsUpdate = {'buildroot' : os.getcwd()},
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
        ]

        self._assertAllsForCmd(CMDNAME, checks, baseExpectedArgs)

    def testCmdZipApp(self):

        baseExpectedArgs = {
            'destdir' : '.',
            'color': 'auto',
            'verbose': 0,
        }

        CMDNAME = 'zipapp'
        checks = [
            dict(
                args = [CMDNAME],
                expectedArgsUpdate = { 'destdir' : '.' },
            ),
            dict(
                args = [CMDNAME, '--destdir', 'somedir'],
                expectedArgsUpdate = {'destdir' : 'somedir' },
            ),
            dict(
                args = [CMDNAME, '--verbose'],
                expectedArgsUpdate = {'verbose': 1, 'destdir' : '.'},
            ),
            dict(
                args = [CMDNAME, '--color', 'no'],
                expectedArgsUpdate = {'color': 'no', 'destdir' : '.'},
            ),
        ]

        self._assertAllsForCmd(CMDNAME, checks, baseExpectedArgs)

    def checkCmdInstall(self, cmd):

        baseExpectedArgs = {
            'buildtype' : self.defaults['buildtype'],
            'jobs' : None,
            'color': 'auto',
            'configure': False,
            'clean': False,
            'progress': False,
            'cleanall': False,
            'distclean': False,
            'verbose': 0,
            'verboseConfigure' : None,
            'verboseBuild' : None,
            'destdir' : '',
            'buildroot' : None,
            'forceExternalDeps' : False,
            'cacheCfgActionResults' : False,
        }
        baseExpectedArgs.update(INSTALL_DIRVAR_CLI_DEFAULTS)

        if cmd == 'uninstall':
            for name in ('configure', 'jobs', 'clean', 'cleanall', 'distclean'):
                baseExpectedArgs.pop(name)

        CMDNAME = cmd
        CMNOPTS = ['--color=auto']

        checks = [
            dict(
                args = [CMDNAME],
                expectedArgsUpdate = {},
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--destdir', 'somedir'],
                expectedArgsUpdate = {'destdir' : 'somedir' },
                wafArgs = [CMDNAME, '--destdir=' + 'somedir'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--prefix', '/usr/loc'],
                expectedArgsUpdate = {'prefix' : '/usr/loc' },
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--bindir', 'somedir'],
                expectedArgsUpdate = {'bindir' : 'somedir' },
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--libdir', 'somedir'],
                expectedArgsUpdate = {'libdir' : 'somedir' },
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--verbose'],
                expectedArgsUpdate = {'verbose': 1},
                wafArgs = [CMDNAME, '-v'] + CMNOPTS,
            ),
            dict(
                args = [CMDNAME, '--color', 'no'],
                expectedArgsUpdate = {'color': 'no'},
                wafArgs = [CMDNAME, '--color=no'] + CMNOPTS[1:],
            ),
            dict(
                args = [CMDNAME, '--buildroot', os.getcwd()],
                expectedArgsUpdate = {'buildroot' : os.getcwd()},
                wafArgs = [CMDNAME] + CMNOPTS,
            ),
        ]

        self._assertAllsForCmd(CMDNAME, checks, baseExpectedArgs)

    def testCmdInstall(self):
        self.checkCmdInstall('install')

    def testCmdUninstall(self):
        self.checkCmdInstall('uninstall')

    def testCmdVersion(self):

        baseExpectedArgs = {
            'verbose': 0,
        }

        CMDNAME = 'version'
        checks = [
            dict(
                args = [CMDNAME],
                expectedArgsUpdate = {},
                wafArgs = [CMDNAME],
            ),
            dict(
                args = [CMDNAME, '--verbose'],
                expectedArgsUpdate = {'verbose': 1},
                wafArgs = [CMDNAME, '-v'],
            ),
        ]

        self._assertAllsForCmd(CMDNAME, checks, baseExpectedArgs)

    def testCmdSysInfo(self):

        baseExpectedArgs = {
            'verbose': 0,
        }

        CMDNAME = 'sysinfo'
        checks = [
            dict(
                args = [CMDNAME],
                expectedArgsUpdate = {},
                wafArgs = [CMDNAME],
            ),
            dict(
                args = [CMDNAME, '--verbose'],
                expectedArgsUpdate = {'verbose': 1},
                wafArgs = [CMDNAME, '-v'],
            ),
        ]

        self._assertAllsForCmd(CMDNAME, checks, baseExpectedArgs)

def parse(cfgdefaults, args):
    return cli.CmdLineParser('test', cfgdefaults).parse(args).args

@pytest.mark.usefixtures("unsetEnviron")
class TestDefaults(object):

    def testBuildtype(self):

        cfgdefaults = {}
        assert parse(cfgdefaults, ['install']).buildtype is None
        cfgdefaults = { 'buildtype': 'somedebug' }
        assert parse(cfgdefaults, ['install']).buildtype == 'somedebug'
        assert parse(cfgdefaults, ['install', '--buildtype=my']).buildtype == 'my'

    def testDestdir(self, monkeypatch):

        cfgdefaults = {}
        assert parse(cfgdefaults, ['install']).destdir == ''
        assert parse(cfgdefaults, ['zipapp']).destdir == '.'

        cfgdefaults = { 'destdir': 'dd' }
        assert parse(cfgdefaults, ['install']).destdir == 'dd'
        assert parse(cfgdefaults, ['zipapp']).destdir == 'dd'
        assert parse(cfgdefaults, ['install', '--destdir=aa']).destdir == 'aa'
        assert parse(cfgdefaults, ['zipapp', '--destdir=aa']).destdir == 'aa'
        cfgdefaults = { 'destdir': { 'install' : 'cc', 'any' : 'ss' } }
        assert parse(cfgdefaults, ['install']).destdir == 'cc'
        assert parse(cfgdefaults, ['zipapp']).destdir == 'ss'
        assert parse(cfgdefaults, ['install', '--destdir=aa']).destdir == 'aa'
        assert parse(cfgdefaults, ['zipapp', '--destdir=aa']).destdir == 'aa'

        monkeypatch.setenv('DESTDIR', 'dst')
        cfgdefaults = {}
        assert parse(cfgdefaults, ['install']).destdir == 'dst'
        assert parse(cfgdefaults, ['zipapp']).destdir == 'dst'
        cfgdefaults = { 'destdir': 'dd' }
        assert parse(cfgdefaults, ['install']).destdir == 'dst'
        assert parse(cfgdefaults, ['zipapp']).destdir == 'dst'
        assert parse(cfgdefaults, ['install', '--destdir=aa']).destdir == 'aa'
        assert parse(cfgdefaults, ['zipapp', '--destdir=aa']).destdir == 'aa'
        cfgdefaults = { 'destdir': { 'install' : 'cc', 'any' : 'ss' } }
        assert parse(cfgdefaults, ['install']).destdir == 'dst'
        assert parse(cfgdefaults, ['zipapp']).destdir == 'dst'
        assert parse(cfgdefaults, ['install', '--destdir=aa']).destdir == 'aa'
        assert parse(cfgdefaults, ['zipapp', '--destdir=aa']).destdir == 'aa'

    def testPrefix(self, monkeypatch):

        cfgdefaults = {}
        assert parse(cfgdefaults, ['install']).prefix is None

        cfgdefaults = { 'prefix': 'dd' }
        assert parse(cfgdefaults, ['install']).prefix == 'dd'
        assert parse(cfgdefaults, ['install', '--prefix=aa']).prefix == 'aa'

        monkeypatch.setenv('PREFIX', '/usr/ll')
        cfgdefaults = {}
        assert parse(cfgdefaults, ['install']).prefix == '/usr/ll'
        cfgdefaults = { 'prefix': 'ccc' }
        assert parse(cfgdefaults, ['install']).prefix == '/usr/ll'
        assert parse(cfgdefaults, ['install', '--prefix=aa']).prefix == 'aa'
