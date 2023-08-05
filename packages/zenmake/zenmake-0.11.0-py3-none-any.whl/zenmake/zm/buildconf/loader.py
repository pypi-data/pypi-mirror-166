# coding=utf-8
#

"""
 Copyright (c) 2019, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

__all__ = [
    'applyDefaults',
    'load',
]

import os
import sys

from zm.constants import BUILDCONF_FILENAMES, DEFAULT_BUILDROOTNAME
from zm.utils import loadPyModule

isfile = os.path.isfile
joinpath = os.path.join

def applyDefaults(buildconf, isTopLevel, projectDir):
    """
    Set default values to some params in buildconf if they don't exist
    """

    params = None

    # Param 'startdir' is set in another place

    # buildroot
    if isTopLevel:
        if not hasattr(buildconf, 'buildroot'):
            setattr(buildconf, 'buildroot', DEFAULT_BUILDROOTNAME)

    # Param 'realbuildroot' must not be set here

    # general features
    if not hasattr(buildconf, 'general'):
        setattr(buildconf, 'general', {})
    if isTopLevel:
        params = buildconf.general
        params['autoconfig'] = params.get('autoconfig', True)
        params['hash-algo'] = params.get('hash-algo', 'sha1')
        params['db-format'] = params.get('db-format', 'pickle')

    # dict params
    dictParams = (
        'cliopts', 'conditions', 'edeps', 'toolchains',
        'buildtypes', 'tasks',
    )
    for param in dictParams:
        if not hasattr(buildconf, param):
            setattr(buildconf, param, {})

    # usedirs
    if not hasattr(buildconf, 'subdirs'):
        setattr(buildconf, 'subdirs', [])

    # project
    if not hasattr(buildconf, 'project'):
        setattr(buildconf, 'project', {})
    if isTopLevel:
        params = buildconf.project
        params['name'] = params.get('name', None)
        if params['name'] is None:
            params['name'] = os.path.basename(projectDir)
        params['version'] = params.get('version', '')

    # byfilter
    if not hasattr(buildconf, 'byfilter'):
        setattr(buildconf, 'byfilter', [])

def findConfFile(dpath, fname = None):
    """
    Try to find buildconf file.
    Returns filename if found or None
    """
    if fname:
        if isfile(joinpath(dpath, fname)):
            return fname
        return None

    for name in BUILDCONF_FILENAMES:
        if isfile(joinpath(dpath, name)):
            return name
    return None

def load(dirpath = None, filename = None):
    """
    Load buildconf.
    Param 'dirpath' is optional param that is used as directory
    with buildconf file.
    """

    if not dirpath:
        # try to find config file
        for path in sys.path:
            _filename = findConfFile(path, filename)
            if _filename:
                dirpath = path
                filename = _filename
                break
        else:
            filename = None
    else:
        filename = findConfFile(dirpath, filename)

    found = None
    if filename:
        found = 'py' if filename.endswith('.py') else 'yaml'

    if found == 'py':
        # Avoid writing .pyc files
        sys.dont_write_bytecode = True
        module = loadPyModule(filename[:-3], dirpath = dirpath, withImport = False)
        sys.dont_write_bytecode = False # pragma: no cover
    elif found == 'yaml':
        from zm.buildconf import yaml
        module = yaml.load(joinpath(dirpath, filename))
    else:
        module = loadPyModule('zm.buildconf.fakeconf')

    return module
