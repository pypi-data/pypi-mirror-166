.. include:: global.rst.inc
.. highlight:: console
.. _commands:

Commands
=====================

Here are some descriptions of general commands. You can get the list of the all
commands with a short description by ``zenmake help`` or ``zenmake --help``.
To get help on selected command you
can use ``zenmake help <selected command>`` or
``zenmake <selected command> --help``. Some commands have short aliases.
For example you can use ``bld`` instead of ``build`` and ``dc``
instead of ``distclean``.

configure
    Configure the project. In most cases you don't need to call this command
    directly. The ``build`` command calls this command by itself if necessary.
    This command processes most of values from :ref:`buildconf<buildconf>`
    of a project. Any change in :ref:`buildconf<buildconf>` leads to call
    of this command. You can change this behaviour with parameter ``autoconfig``
    in buildconf :ref:`general features<buildconf-general>`.

build
    Build the project in the current directory. It's the main command. To see all
    possible parameters use ``zenmake help build`` or
    ``zenmake build --help``. For example you can use ``-v`` to see more info
    about building process or ``-p`` to use progress bar instead of text logging.
    By default it calls the ``configure`` command by itself if necessary.

test
    Build (if necessery) and run tests in the current directory. If the project
    has no tests it's almost the same as running the ``build`` command.
    The ``test`` command builds and runs tests by default while
    the ``build`` command doesn't.

run
    Build the project (if necessery) and run one executable target from the
    build directory.
    You can specify build task/target to run if the project has more than
    one executable targets or omit it if the project has only one
    executable target. To provide command line args directly to your program
    you can put them after '--' in command line after all args for ZenMake.
    This command is for fast checking of the built project.

clean
    Remove build files for selected ``buildtype`` of the project.
    It doesn't touch other build files.

cleanall
    Remove the build directory of the project with everything in it.

install
    Install the build targets in some destination directory using installation
    prefix. It builds targets by itself if necessary.
    You can control paths with :ref:`environment variables<envvars>`
    or command line parameters (see ``zenmake help install``).
    It looks like classic ``make install`` in common.

uninstall
    Remove the build targets installed with the ``install`` command.
