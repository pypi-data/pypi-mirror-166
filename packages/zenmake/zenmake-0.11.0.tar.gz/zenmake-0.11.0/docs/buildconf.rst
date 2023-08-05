.. include:: global.rst.inc
.. highlight:: python
.. _buildconf:

Build config
============

ZenMake uses build configuration file with name ``buildconf.py`` or
``buildconf.yaml``/``buildconf.yml``. First variant is a regular python file and second one is
an YAML file. ZenMake doesn't use both files in one directory at the same time.
If both files exist in one directory then only ``buildconf.py`` will be used.
Common name ``buildconf`` is used in this manual.

The format for both config files is the same. YAML variant is a little more
readable but in python variant you can add a custom python code if you wish.

Simplified scheme of buildconf is:

.. parsed-literal::

    startdir_ = path
    buildroot_ = path
    realbuildroot_ = path
    project_ = { ... }
    :ref:`buildconf-general` = { ... }
    cliopts_ = { ... }
    conditions_ = { ... }
    tasks_ = { name: :ref:`task parameters<buildconf-taskparams>` }
    buildtypes_ = { name: :ref:`task parameters<buildconf-taskparams>` }
    toolchains_ = { name: parameters }
    byfilter_ = [ { for: {...}, set: :ref:`task parameters<buildconf-taskparams>` }, ... ]
    :ref:`buildconf-subdirs` = []
    edeps_ = { ... }

Also see :ref:`syntactic sugar<buildconf-syntactic-sugar>`.

.. _buildconf-dict-def:

Where symbols '{}' mean an associative array/dictionary and symbols '[]'
mean a list. In python notation '{}' is known as dictionary. In some other
languages it's called an associative array including YAML (Of course YAML is not
programming language but it's markup language). For shortness it's called
a ``dict`` here.

Not all variables are required in the scheme above but buildconf cannot be
empty. All variables have reserved names and they all are described here.
Other names in buildconf are just ignored by ZenMake
(excluding :ref:`substitution variables<buildconf-substitutions>`) if present and it means
they can be used for some custom purposes.

.. note::

    **About paths in general.**

    You can use native paths but it's recommended to use wherever possible
    POSIX paths (Symbol ``/`` is used as a separator in a path).
    With POSIX paths you will ensure the same paths on
    different platforms/operating systems. POSIX paths will be
    converted into native paths automatically, but not vice versa.
    For example, path 'my/path' will be converted into 'my\\path' on Windows.
    Also it's recommended to use relative paths wherever possible.

.. warning::

    ``Windows only``: do NOT use short filename notation (8.3 filename) for
    paths in buildconf files. It can cause unexpected errors.

Below is the detailed description of each buildconf variable.

.. _buildconf-startdir:

startdir
""""""""
    A start path for all paths in a buildconf.
    It is ``.`` by default. The path can be absolute or relative to directory
    where current buildconf file is located. It means that by default all other
    relative paths in the current buildconf file are considered as the paths
    relative to directory with the current buildconf file.
    But you can change this by setting a different value to this variable.

.. _buildconf-buildroot:

buildroot
"""""""""
    A path to the root of a project build directory. By default it is
    directory 'build' in the directory with the top-level buildconf file of
    the project. Path can be absolute or relative to the startdir_.
    It is important to be able to remove the build
    directory safely, so it should never be given as ``.`` or ``..``.

    .. note::
      If you change value of ``buildroot`` with already using/existing
      build directory then ZenMake will not touch previous build directory.
      You can remove previous build directory manually or run
      command ``distclean`` before changing of ``buildroot``.
      ZenMake cannot do it because it stores all
      meta information in current build directory and if you change this
      directory it will lose all such an information.

      This can be changed in the future by storing extra information in some
      other place like user home directory but now it is.

.. _buildconf-realbuildroot:

realbuildroot
"""""""""""""
    A path to the real root of a project build directory and by default it is
    equal to value of ``buildroot``. It is optional parameter and if
    ``realbuildroot`` has different value from ``buildroot`` then
    ``buildroot`` will be symlink to ``realbuildroot``. Using ``realbuildroot``
    makes sense mostly on linux where '/tmp' is usually on tmpfs filesystem
    nowadays and it can used to make building in memory. Such a way can improve
    speed of building. Note that on Windows OS the process of ZenMake needs to be
    started with enabled "Create symbolic links" privilege and usual user
    doesn't have a such privilege.
    Path can be absolute or relative to the startdir_.
    It is important to be able to remove the build directory safely,
    so it should never be given as ``.`` or ``..``.

.. _buildconf-project:

project
"""""""
    A `dict <buildconf-dict-def_>`_ with some parameters for the project.
    Supported values:

    :name: The name of the project. It's name of the top-level startdir_
           directory by default.
    :version: The version of the project. It's empty by default.
              It's used as default value for
              :ref:`ver-num<buildconf-taskparams-ver-num>` field if not empty.

.. _buildconf-general:

general
""""""""
    A `dict <buildconf-dict-def_>`_ array with some general features.
    Supported values:

    :autoconfig: Execute the command ``configure`` automatically in
                 the command ``build`` if it's necessary.
                 It's ``True`` by default. Usually you don't need to change
                 this value.

    :monitor-files: Set extra file paths to check changes in them. You can use
                    additional files with your buildconf file(s). For example
                    it can be extra python module with some tools. But in this
                    case ZenMake doesn't know about such files when it checks
                    buildconf file(s) for changes to detect if it must call
                    command ``configure`` for feature ``autoconfig``. You
                    can add such files to this variable and ZenMake will check
                    them for changes as it does so for regular buildconf file(s).

                    If paths contain spaces and all these paths are listed
                    in one string then each such a path must be in quotes.

    :hash-algo: Set hash algorithm to use in ZenMake. It can be ``sha1`` or
                ``md5``. By default ZenMake uses sha1 algorithm to control
                changes of config/built files and for some other things.
                Sha1 has much less collisions than md5
                and that's why it's used by default. Modern CPUs often has support
                for this algorithm and sha1 show better or almost the same
                performance than md5 in this cases. But in some cases md5 can be
                faster and you can set here this variant. However, don't expect big
                difference in performance of ZenMake. Also, if a rare
                "FIPS compliant" build of Python is used it's always sha1 anyway.

    :db-format: Set format for internal ZenMake db/cache files.
                Use one of possible values: ``py``, ``pickle``, ``msgpack``.

                The value ``py`` means text file with python syntax. It is not fastest
                format but it is human readable one.

                The value ``pickle`` means python pickle binary format. It has
                good performance and python always supports this format.

                The value ``msgpack`` means msgpack binary
                format by using python module ``msgpack``. Using of this format can
                decrease ZenMake overhead in building of some big projects because
                it has the best performance among all supported formats.
                If the package ``msgpack`` doesn't exist in the current system then
                the ``pickle`` value will be used.
                Note: ZenMake doesn't try to install package ``msgpack``.
                This package must be installed in some other way.

                The default value is ``pickle``.

    :provide-edep-targets: Provide target files of
                :ref:`external dependencies<dependencies-external>`
                in the :ref:`buildroot<buildconf-buildroot>` directory.
                It is useful to run built files from the build directory without
                the need to use such a thing as LD_LIBRARY_PATH for each dependency.
                Only existing and used target files are provided.
                Static libraries are also ignored because they are not needed
                to run built files.
                On Windows ZenMake copies these files while on other OS
                (Linux, MacOS, etc) it makes symlinks.

                It's ``False`` by default.

    :build-work-dir-name: Set a name of work directory which is used mostly for
            object files during compilation. This directory seperates
            resulting target files from other files in a buildtype directory to
            avoid file/directory conflicts. Usually you don't need to set this
            parameter until some target name has conflict with default value of
            this parameter.

            The default value is ``@bld``.

.. _buildconf-cliopts:

cliopts
""""""""
    A `dict <buildconf-dict-def_>`_ array with default values for command
    line options. It can be any existing command line option that ZenMake has.
    If you want to set an option for selected commands then you can set it in
    the format of a `dict <buildconf-dict-def_>`_ where key is a name of
    specific command or special value 'any' which means any command.
    If some command doesn't have selected option then it will be ignored.

    Example in YAML format:

    .. code-block:: yaml

        cliopts:
          verbose: 1
          jobs : { build : 4 }
          progress :
            any: false
            build: true

    .. note::
        Selected command here is a command that is used on command line.
        It means if you set an option for the ``build`` command and zenmake calls
        the ``configure`` command before this command by itself then this option will
        be applied for both ``configure`` and ``build`` commands. In other words
        it is like you are running this command with this option on command line.

.. _buildconf-conditions:

conditions
"""""""""""
    A `dict <buildconf-dict-def_>`_ with conditions for
    :ref:`selectable parameters<buildconf-select>`.

.. _buildconf-tasks:

tasks
"""""
    A `dict <buildconf-dict-def_>`_ with build tasks. Each task has own
    unique name and :ref:`parameters<buildconf-taskparams>`. Name of task can
    be used as dependency id for other build tasks. Also this name is used as a
    base for resulting target file name if parameter ``target`` is not set in
    :ref:`task parameters<buildconf-taskparams>`.
    In this variable you can set up build parameters particularly for each build task.
    Example in YAML format:

    .. code-block:: yaml

        tasks:
          mylib :
            # some task parameters
          myexe :
            # some task parameters
            use : mylib

    .. note::
        Parameters in this variable can be overridden by parameters in
        buildtypes_ and/or byfilter_.

    .. note::
        Name of a task cannot contain symbol ``:``. You can use
        parameter ``target`` if you want to have this symbol in
        resulting target file names.

.. _buildconf-buildtypes:

buildtypes
""""""""""
    A `dict <buildconf-dict-def_>`_ with build types like ``debug``, ``release``,
    ``debug-gcc`` and so on. Here is also a special value with name ``default``
    that is used to set default build type if nothing is specified. Names of
    these build types are just names, they can be any name but not ``default``.
    Also you should remember that these names are used as
    directory names. So don't use
    incorrect symbols if you don't want a problem with it.

    This variable can be empty or absent. In this case current buildtype is
    always just an empty string.

    Possible parameters for each build type are described in
    :ref:`task parameters<buildconf-taskparams>`.

    Special value ``default`` must be a string with the name of one of the
    build types or a `dict <buildconf-dict-def_>`_ where keys are supported name
    of the host operating system and values are strings with the names of one of the
    build types. Special key '_' or 'no-match' can be used in the ``default`` to
    define a value that will be used if the name of the current host operating system
    is not found among the keys in the ``default``.

    Valid host operating system names: ``linux``, ``windows``, ``darwin``, ``freebsd``,
    ``openbsd``, ``sunos``, ``cygwin``, ``msys``, ``riscos``, ``atheos``,
    ``os2``, ``os2emx``, ``hp-ux``, ``hpux``, ``aix``, ``irix``.

    .. note::
        Only ``linux``, ``windows`` and ``darwin`` are tested.

    Examples in YAML format:

    .. code-block:: yaml

        buildtypes:
          debug        : { toolchain: auto-c++ }
          debug-gcc    : { toolchain: g++, cxxflags: -fPIC -O0 -g }
          release-gcc  : { toolchain: g++, cxxflags: -fPIC -O2 }
          debug-clang  : { toolchain: clang++, cxxflags: -fPIC -O0 -g }
          release-clang: { toolchain: clang++, cxxflags: -fPIC -O2 }
          debug-msvc   : { toolchain: msvc, cxxflags: /Od /EHsc }
          release-msvc : { toolchain: msvc, cxxflags: /O2 /EHsc }
          default: debug

        buildtypes:
          debug:
            toolchain.select:
              default: g++
              darwin: clang++
              windows: msvc
            cxxflags.select:
              default : -O0 -g
              msvc    : /Od /EHsc
          release:
            toolchain.select:
              default: g++
              darwin: clang++
              windows: msvc
            cxxflags.select:
              default : -O2
              msvc    : /O2 /EHsc
          default: debug

        buildtypes:
          debug-gcc    : { cxxflags: -O0 -g }
          release-gcc  : { cxxflags: -O2 }
          debug-clang  : { cxxflags: -O0 -g }
          release-clang: { cxxflags: -O2 }
          debug-msvc   : { cxxflags: /Od /EHsc }
          release-msvc : { cxxflags: /O2 /EHsc }
          default:
            _: debug-gcc
            linux: debug-gcc
            darwin: debug-clang
            windows: debug-msvc

    .. note::
        Parameters in this variable override corresponding parameters in tasks_ and
        can be overridden by parameters in byfilter_.

.. _buildconf-toolchains:

toolchains
""""""""""
    A `dict <buildconf-dict-def_>`_ with custom toolchain setups. It's useful
    for simple cross builds for example, or for custom settings for existing
    toolchains. Each value has unique name and parameters. Parameters are also
    dict with names of environment variables and
    special name ``kind`` that is used to specify the type of
    toolchain/compiler. Environment variables are usually such variables as
    ``CC``, ``CXX``, ``AR``, etc that are used to specify
    name or path to existing toolchain/compiler. Path can be absolute or
    relative to the startdir_. Also such variables as ``CFLAGS``,
    ``CXXFLAGS``, etc can be set here.

    Names of toolchains from this parameter can be used as a value for the
    ``toolchain`` in :ref:`task parameters<buildconf-taskparams>`.

    Example in YAML format:

    .. code-block:: yaml

        toolchains:
          custom-g++:
            kind : auto-c++
            CXX  : custom-toolchain/gccemu/g++
            AR   : custom-toolchain/gccemu/ar
          custom-clang++:
            kind : clang++
            CXX  : custom-toolchain/clangemu/clang++
            AR   : custom-toolchain/clangemu/llvm-ar
          g++:
            LINKFLAGS : -Wl,--as-needed

.. _buildconf-byfilter:

byfilter
""""""""
    This variable describes extra/alternative way to set up build tasks.
    It's a list of `dicts <buildconf-dict-def_>`_ with attributes
    ``set`` and ``for``, ``not-for`` and/or ``if``.
    Attributes ``for``/``not-for``/``if`` describe conditions for parameters
    in attribute ``set``, that is, a filter to set some build task parameters.
    The attribute ``for`` is like a ``if a`` and the attribute
    ``not-for`` is like a ``if not b`` where ``a`` and ``b`` are some conditions.
    And they are like a ``if a and if not b`` when both of them exist in the
    same item. The attribute ``not-for`` has higher priority in the case of the
    same condition in the both of them.

    Since v0.11 ZenMake supports ``if`` attribute where you can set a string with
    python like expression.

    The ``for``/``not-for`` are dicts and ``if`` is an expression.
    In ``for``/``not-for``/``if`` you can use such variables as dict keys in
    ``for``/``not-for`` and as keywords within an expression:

    :task:      Build task name or list of build task names.
                It can be existing task(s) from tasks_ or new (only in ``for``).
    :buildtype: Build type or list of build types.
                It can be existing build type(s) from buildtypes_ or new (only in ``for``).
    :platform:  Name of a host platform/operating system or list of them.
                Valid values are the same as for ``default`` in buildtypes_.

    The ``if`` is a real python expression with some builtin functions.
    You can use standard python operators as '(', ')', 'and', 'or', 'not', '==',
    '!=' and 'in'. ZenMake supports a little set of extensions as well:

    ===========================  ==========================================================
    Name                         Description
    ===========================  ==========================================================
    true                         The same as python 'True'.
    false                        The same as python 'False'.
    startswith(str, prefix)      Returns true if 'str' starts with the specified 'prefix'.
    endswith(str, prefix)        Returns true if 'str' ends with the specified 'suffix'.
    ===========================  ==========================================================

    The attribute ``set`` has value of the :ref:`task parameters<buildconf-taskparams>`.

    Other features:

    - If some key parameter is not specified in ``for``/``not-for``/``if`` it means that
      this is for all possible values of this kind of condition. For example
      if it has no ``task`` it means 'for all existing tasks'.
      Special word ``all`` (without any other parameters) can be used to indicate
      that current item must be applied to all build tasks.
      Empty dict (i.e. ``{}``) in ``for``/``not-for`` can be used for the same reason as well.
    - Variable 'byfilter' overrides all matched values defined in
      tasks_ and buildtypes_.
    - Items in ``set`` with the same names and the same conditions in
      ``for``/``not-for``/``if`` override items defined before.
    - If ``for``/``not-for`` and ``if`` are used for the same ``set`` then
      result will be the intersection of resulting sets from ``for``/``not-for`` and ``if``.
    - When ``set`` is empty or not defined it does nothing.

    .. note::
      ZenMake applies every item in the ``byfilter`` in the order as they were written.

    It's possible to use ``byfilter`` without tasks_ and buildtypes_.

    Example in YAML format:

    .. code-block:: yaml

        GCC_BASE_CXXFLAGS: -std=c++11 -fPIC

        buildtypes:
        debug-gcc    : { cxxflags: $GCC_BASE_CXXFLAGS -O0 -g }
        release-gcc  : { cxxflags: $GCC_BASE_CXXFLAGS -O2 }
        debug-clang  : { cxxflags: $GCC_BASE_CXXFLAGS -O0 -g }
        release-clang: { cxxflags: $GCC_BASE_CXXFLAGS -O2 }
        debug-msvc   : { cxxflags: /Od /EHsc }
        release-msvc : { cxxflags: /O2 /EHsc }
        default:
          _: debug-gcc
          linux: debug-gcc
          darwin: debug-clang
          windows: debug-msvc

        byfilter:
          - for: all
            set: { includes: '.', rpath : '.', }

          - for: { task: shlib shlibmain }
            set: { features: cxxshlib }

          - for: { buildtype: debug-gcc release-gcc, platform: linux }
            set:
              toolchain: g++
              linkflags: -Wl,--as-needed

          - for: { buildtype: release-gcc }
            not-for : { platform : windows }
            set: { cxxflags: -fPIC -O3 }

          - for: { buildtype: [debug-clang, release-clang], platform: linux darwin }
            set: { toolchain: clang++ }

          - if: endswith(buildtype, '-gcc') and platform == 'linux'
            set:
              toolchain: g++
              linkflags: -Wl,--as-needed

          - if: buildtype == 'release-gcc' and platform == 'linux'
            set:
              cxxflags: $GCC_BASE_CXXFLAGS -O3

          - if: endswith(buildtype, '-clang') and platform in ('linux', 'darwin')
            set:
              toolchain: clang++

          - if: endswith(buildtype, '-msvc') and platform == 'windows'
            set:
              toolchain: msvc

    .. note::
        Parameters in this variable override corresponding parameters in tasks_
        and in buildtypes_.

.. _buildconf-subdirs:

subdirs
"""""""
    This variable controls including buildconf files from other sub directories
    of the project.

    - If it is list of paths then ZenMake will try to use this list as paths
      to sub directories with the buildconf files and will use all found ones.
      Paths can be absolute or relative to the :ref:`startdir<buildconf-startdir>`.
    - If it is an empty list or just absent at all
      then ZenMake will not try to use any
      sub directories of the project to find buildconf files.

    Example in Python format:

    .. code-block:: python

        subdirs = [
            'libs/core',
            'libs/engine',
            'main',
        ]

    Example in YAML format:

    .. code-block:: yaml

        subdirs:
            - libs/core
            - libs/engine
            - main

    See some details :ref:`here<dependencies-subdirs>`.

.. _buildconf-edeps:

edeps
""""""""""""
    A `dict <buildconf-dict-def_>`_ with configurations of external non-system
    dependencies. Each such a dependency has own unique name which can be used in
    task parameter :ref:`use<buildconf-taskparams-use>`.

    See full description of parameters :ref:`here<buildconf-edep-params>`.
    Description of external dependencies is :ref:`here<dependencies-external>`.

.. note::

    More examples of buildconf files can be found in repository
    `here <repo_demo_projects_>`_.
