# coding=utf-8
#

# pylint: disable = wildcard-import, unused-wildcard-import, unused-import
# pylint: disable = missing-docstring, invalid-name

"""
 Copyright (c) 2019, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

import os
import sys
import pytest

from zm.autodict import AutoDict
from zm.constants import APPNAME, CWD
from zm import cli
from zm import starter
import tests.common as cmn

joinpath = os.path.join

def testHandleCLI(capsys):

    oldCliSelected = cli.selected
    cwd = CWD

    noBuildConf = True
    args = [APPNAME]
    options = {}

    with pytest.raises(SystemExit):
        starter.handleCLI(args, noBuildConf, options, cwd)
    # clean output
    capsys.readouterr()

    with pytest.raises(SystemExit):
        starter.handleCLI(args, noBuildConf, None, cwd)
    # clean output
    capsys.readouterr()

    #############
    args = [APPNAME, 'build']
    options = {}
    cmd = starter.handleCLI(args, noBuildConf, options, cwd)
    assert cmd == cli.selected
    assert cmd.name == 'build'
    assert cmd.wafline[0] == 'build'
    assert cmd.args.verbose == 0
    assert cmd.args.jobs is None
    assert not cmd.args.progress

    options = {
        'verbose': 1,
        'jobs' : { 'build' : 4 },
        'progress' : {'any': False, 'build': True },
    }
    cmd = starter.handleCLI(args, noBuildConf, options, cwd)
    assert cmd == cli.selected
    assert cmd.name == 'build'
    assert cmd.wafline[0] == 'build'
    assert cmd.args.verbose == 1
    assert cmd.args.jobs == 4
    assert cmd.args.progress
    cmd = starter.handleCLI(args, noBuildConf, None, cwd)
    assert cmd == cli.selected
    assert cmd.name == 'build'
    assert cmd.wafline[0] == 'build'
    assert cmd.args.verbose == 0
    assert cmd.args.jobs is None
    assert not cmd.args.progress

    args = [APPNAME, 'test']
    cmd = starter.handleCLI(args, noBuildConf, options, cwd)
    assert cmd == cli.selected
    assert cmd.name == 'test'
    assert cmd.wafline[0] == 'build'
    assert cmd.args.verbose == 1
    assert cmd.args.jobs is None
    assert not cmd.args.progress

    # don't affect other tests
    cli.selected = oldCliSelected

def testFindTopLevelBuildConfDir(tmpdir):

    startdir = str(tmpdir.realpath())
    assert starter.findTopLevelBuildConfDir(startdir) is None

    dir1 = tmpdir.mkdir("dir1")
    dir2 = dir1.mkdir("dir2")
    dir3 = dir2.mkdir("dir3")
    dir4 = dir3.mkdir("dir4")

    assert starter.findTopLevelBuildConfDir(str(dir4)) is None

    buildconf = joinpath(str(dir4), 'buildconf.py')
    with open(buildconf, 'w+') as file:
        file.write("buildconf")
    assert starter.findTopLevelBuildConfDir(str(dir4)) == str(dir4)
    assert starter.findTopLevelBuildConfDir(str(dir3)) is None

    buildconf = joinpath(str(dir3), 'buildconf.yaml')
    with open(buildconf, 'w+') as file:
        file.write("buildconf")
    assert starter.findTopLevelBuildConfDir(str(dir4)) == str(dir3)
    assert starter.findTopLevelBuildConfDir(str(dir3)) == str(dir3)
    assert starter.findTopLevelBuildConfDir(str(dir2)) is None

    buildconf = joinpath(str(dir1), 'buildconf.yml')
    with open(buildconf, 'w+') as file:
        file.write("buildconf")
    assert starter.findTopLevelBuildConfDir(str(dir4)) == str(dir1)
    assert starter.findTopLevelBuildConfDir(str(dir3)) == str(dir1)
    assert starter.findTopLevelBuildConfDir(str(dir2)) == str(dir1)
    assert starter.findTopLevelBuildConfDir(str(dir1)) == str(dir1)
