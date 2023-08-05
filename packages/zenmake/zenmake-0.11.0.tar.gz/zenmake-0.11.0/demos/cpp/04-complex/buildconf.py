
from buildconf_tools import *

cliopts = {
    #'color': 'no',
    'jobs' : { 'build' : 4 },
    #'progress' : {'any': False, 'build': True },
    'verbose-build' : 1,
}

general = {
    'monitor-files' : 'buildconf_tools.py',
    'build-work-dir-name' : 'wrk',
}

tasks = {
    'shlib' : {
        'features' : 'cxxshlib',
        'source'   : 'shlib/**/*.cpp',
        'includes' : 'include',
        'defines'  : 'ABC=1 DOIT MY_LONG_STRING="some long string"',
        'export'   : 'includes defines',
        'install-path' : False,
        'configure'  : [
            {
                'do' : 'parallel', 'actions' : [
                    { 'do' : 'check-headers', 'names' : 'cstdio iostream', 'id' : 'first' },
                    { 'do' : 'check-headers', 'names' : 'stdlib.h', 'after' : 'first' },
                    { 'do' : 'check-headers', 'names' : 'stdlibasd.h', 'mandatory' : False },
                    { 'do' : 'check-libs', 'names' : 'boost_random', 'mandatory' : not iswin32 },
                ],
                'tryall' : True,
            },
        ],
    },
    'stlib' : {
        'features' : 'cxxstlib',
        'source'   : 'stlib/**/*.cpp',
    },
    'shlibmain' : {
        'features' : 'cxxshlib',
        'source'   : 'shlibmain/**/*.cpp',
        'use'      : 'shlib stlib',
        'install-path' : '$(prefix)/lbr',
    },
    'main' : {
        'features' : 'cxxprogram',
        'source'   : 'prog/**/*.cpp',
        'use'      : 'shlibmain',
        'target'   : '@bld', # to check 'build-work-dir-name'
    },
}

buildtypes = {
    'debug-gcc' : {
        'toolchain' : 'g++',
        'cxxflags' : '-O0 -g',
    },
    'release-gcc' : {
        'toolchain' : 'g++',
        'cxxflags' : '-O2',
    },
    'debug-clang' : {
        'toolchain' : 'clang++',
        'cxxflags' : '-O0 -g',
    },
    'release-clang' : {
        'toolchain' : 'clang++',
        'cxxflags' : '-O2',
    },
    'debug-msvc' : {
        'toolchain' : 'msvc',
        'cxxflags' : '/Od',
    },
    'release-msvc' : {
        'toolchain' : 'msvc',
        'cxxflags' : '/O2',
    },
    'default' : {
        'linux': 'debug-gcc',
        'darwin': 'debug-clang',
        'windows': 'debug-msvc',
    },
}

toolchains = {
    'g++': {
        'LINKFLAGS' : '-Wl,--as-needed',
        'CXXFLAGS' : '-fPIC -Wall',
    },
    'clang++': {
        'CXXFLAGS' : '-fPIC',
    },
    'msvc': {
        'CXXFLAGS' : '/EHsc',
    },
}
