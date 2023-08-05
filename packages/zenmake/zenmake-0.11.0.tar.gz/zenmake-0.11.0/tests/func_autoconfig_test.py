# coding=utf-8
#

# pylint: disable = wildcard-import, unused-wildcard-import
# pylint: disable = missing-docstring, invalid-name
# pylint: disable = unused-argument, no-member, attribute-defined-outside-init
# pylint: disable = too-many-lines, too-many-branches, too-many-statements

"""
 Copyright (c) 2020, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

import os
import io
import shutil

import pytest
from zm import pyutils, version

import tests.common as cmn
from tests.func_utils import *

@pytest.mark.usefixtures("unsetEnviron")
class TestAutoconfig(object):

    @pytest.fixture(params = getZmExecutables())
    def allZmExe(self, request):
        self.zmExe = zmExes[request.param]

    @pytest.fixture(params = [joinpath('c', '01-trivial')])
    def project(self, request, tmpdir):

        setupTest(self, request, tmpdir)

        self.testdir = os.path.abspath(joinpath(self.cwd, os.pardir))

    @pytest.fixture(params = cmn.getMonitoredEnvVarNames()[::3])
    def toolEnvVar(self, request):
        self.toolEnvVar = request.param

    def testEnvVars(self, allZmExe, project, toolEnvVar):

        env = { 'ZENMAKE_TESTING_MODE' : '1' }

        # first run
        cmdLine = ['build']
        returncode, stdout, _ = runZm(self, cmdLine, env)
        assert returncode == 0

        # then it should be checked

        # Such a way breaks building but here is testing of reacting, not building.
        env[self.toolEnvVar] = cmn.randomstr()
        _, stdout, _ = runZm(self, cmdLine, env)
        assert "Setting top to" in stdout
        assert "Setting out to" in stdout

    def testConfChanged(self, allZmExe, project):

        # first run
        cmdLine = ['build']
        returncode, stdout, _ = runZm(self, cmdLine)
        assert returncode == 0

        # then it should be checked

        buildConfFile = joinpath(self.cwd, 'buildconf.py')
        buildConfFile2 = joinpath(self.cwd, 'buildconf.yaml')
        assert isfile(buildConfFile) or isfile(buildConfFile2)

        yamlFormat = not isfile(buildConfFile) and isfile(buildConfFile2)
        if yamlFormat:
            buildConfFile = buildConfFile2

        with open(buildConfFile, 'r') as file:
            lines = file.readlines()
        if yamlFormat:
            lines.append("somevar : 'qq'\n")
        else:
            lines.append("somevar = 'qq'\n")
        with open(buildConfFile, 'w') as file:
            file.writelines(lines)

        returncode, stdout, _ = runZm(self, cmdLine)
        assert returncode == 0
        assert "Setting top to" in stdout
        assert "Setting out to" in stdout

        returncode, stdout, _ = runZm(self, cmdLine)
        assert returncode == 0
        assert "Setting top to" not in stdout
        assert "Setting out to" not in stdout

    def testVerChanged(self, project):

        zmdir = joinpath(self.testdir, 'zenmake')
        shutil.copytree(cmn.ZENMAKE_DIR, zmdir)

        self.zmExe = [PYTHON_EXE, zmdir]

        # first run
        cmdLine = ['build']
        returncode, stdout, _ = runZm(self, cmdLine)
        assert returncode == 0

        # then it should be checked
        parsed = version.parseVersion(version.current())
        gr = parsed.groups()
        changedVer = '.'.join(gr[:3]) + '-' + cmn.randomstr(10)

        filePath = joinpath(zmdir, version.VERSION_FILE_NAME)
        with io.open(filePath, 'wt') as file:
            file.write(pyutils.texttype(changedVer))

        returncode, stdout, _ = runZm(self, cmdLine)
        assert returncode == 0
        assert "Setting top to" in stdout
        assert "Setting out to" in stdout

        returncode, stdout, _ = runZm(self, cmdLine)
        assert returncode == 0
        assert "Setting top to" not in stdout
        assert "Setting out to" not in stdout
