import os
import sys


PKG_BUILDER = "fpm"
if os.name == "nt":
    PKG_BUILDER = "msi"

CLI_CONFIG = {
    "config": {"options": ["-c"], "subcommands": ["_global_"]},
    "name": {"options": ["-n"], "subcommands": ["_global_"]},
    "directory": {
        "options": ["-D", "--dir"],
        "subcommands": ["_global_"],
    },
    "run": {"options": ["-R"], "subcommands": ["_global_"]},
    "requirements": {"options": ["-r"], "subcommands": ["_global_"]},
    "exclude": {
        "options": ["-e"],
        "subcommands": ["build", "pyinstaller"],
        "nargs": "*",
    },
    "venv_uninstall": {"subcommands": ["build", "pyinstaller"], "nargs": "*"},
    "system_site": {
        "options": ["-S"],
        "action": "store_true",
        "subcommands": ["build", "pyinstaller"],
    },
    "pyinstaller_version": {
        "subcommands": ["build", "pyinstaller"],
    },
    "pyinstaller_runtime_tmpdir": {
        "options": ["--pyinstaller-runtime-tmpdir"],
        "subcommands": ["build", "pyinstaller"],
    },
    "pyinstaller_args": {
        "subcommands": ["build", "pyinstaller"],
        "nargs": "*",
    },
    "onedir": {"action": "store_true", "subcommands": ["build", "pyinstaller"]},
    "pyenv": {"subcommands": ["build", "pyinstaller"]},
    "no_clean": {"action": "store_true", "subcommands": ["_global_"]},
    "locale_utf8": {
        "options": ["--locale-utf8"],
        "action": "store_true",
        "subcommands": ["build", "pyinstaller"],
    },
    "dependencies": {
        "nargs": "*",
        "subcommands": ["build", "pyinstaller"],
    },
    "omit": {"subcommands": ["build", "pyinstaller"]},
    "release": {"subcommands": ["build", "pyinstaller"]},
    "pkg_builder": {"subcommands": ["build", "pyinstaller"]},
    "pkg_tgt": {"subcommands": ["build", "pyinstaller"]},
    "srcdir": {"subcommands": ["build", "pyinstaller"]},
    "system_copy_in": {"nargs": "*", "subcommands": ["build", "pyinstaller"]},
    "tgt_version": {"subcommands": ["build", "pyinstaller"]},
    "venv_plugin": {"subcommands": ["build", "pyinstaller"]},
    "python_bin": {"subcommands": ["build", "pyinstaller"]},
    "dry_run": {"subcommands": ["build", "pyinstaller"], "action": "store_true"},
    "timeout": {"subcommands": ["_global_"], "type": int},
    "pip_version": {"subcommands": ["build", "pyinstaller"]},
    "use_static_requirements": {
        "options": ["--use-static-requirements"],
        "action": "store_true",
        "subcommands": ["build", "pyinstaller"],
    },
}

CONFIG = {
    "config": {
        "default": "",
        "help": (
            "Load extra options from a configuration file, this is useful when the "
            "project needs to use more advanced features like compiling c binaries "
            "into the environment."
        ),
    },
    "dry_run": {
        "default": False,
        "help": "Run the program without actually doing any subprocess calls",
    },
    "name": {
        "default": None,
        "help": "The name of the project to build",
    },
    "directory": {
        "default": os.getcwd(),
        "help": (
            "The path to the directory to build from. This denotes the root of the "
            "python project source tree to work from. This directory should have the "
            "setup.py and the paths referenced in configurations will assume that "
            "this is the root path they are working from."
        ),
    },
    "run": {
        "default": "run.py",
        "help": "The location of the project run.py file",
    },
    "requirements": {
        "default": "requirements.txt",
        "help": "The name of the requirements.txt file to use",
    },
    "exclude": {
        "default": None,
        "help": (
            "A list of exclude files or python modules, these python packages will be "
            "ignored by pyinstaller"
        ),
    },
    "venv_uninstall": {
        "default": [],
        "help": ("List of modules to remove from the virtual environment"),
    },
    "system_site": {
        "default": False,
        "help": (
            "Include the system site-packages when building. This is needed for builds "
            "from custom installs of Python"
        ),
    },
    "pyinstaller_version": {
        "default": "5.3",
        "help": (
            "The version of Pyinstaller to install.  If 'dev' is specified it will be "
            "installed from git, if 'local:/absolute/file/system/path' is specified it "
            "will be installed from the specified file system path"
        ),
    },
    "pyinstaller_runtime_tmpdir": {
        "default": None,
        "help": "Pyinstaller runtime tmpdir",
    },
    "pyinstaller_args": {
        "default": None,
        "help": (
            "Args to pass straight through to pyinstaller. I.E. tiamat build "
            "--pyinstaller-args='--key=1234 -v'"
        ),
    },
    "datas": {"default": None, "help": "Pyinstaller datas mapping."},
    "onedir": {
        "default": False,
        "help": (
            "Instead of producing a single binary produce a directory with all "
            "components"
        ),
    },
    "pyenv": {
        "default": ".".join(str(x) for x in sys.version_info[:3]),
        "help": (
            "Set the python version to build with, if not present the system python "
            "will be used. Only use CPython versions, to see available versions run "
            '`pyenv install --list | grep "3\\.[6789]"`'
        ),
    },
    "no_clean": {
        "default": False,
        "help": (
            "Don't run the clean up sequence, this will leave the venv, spec file and "
            "other artifacts. Only use this for debugging."
        ),
    },
    "locale_utf8": {
        "default": False,
        "help": (
            "Use the UTF-8 locale with PyInstaller, as in PEP538 and PEP540. This "
            "enables UTF-8 on systems which only provide C or POSIX locales."
        ),
    },
    "build": {
        "default": False,
        "help": (
            "Enter in commands to build a non-python binary into the deployed binary. "
            "The build options are set on a named project basis. This allows for "
            "multiple shared binaries to be embedded into the final build."
        ),
    },
    "dependencies": {
        "default": {},
        "help": "comma separated list of dependencies needed for the build",
    },
    "release": {
        "default": {},
        "help": "Release string i.e. '1.el7'. this is the fpm --iteration option.",
    },
    "pkg": {"default": {}, "help": "Options for building packages"},
    "pkg_builder": {
        "default": PKG_BUILDER,
        "help": "Select what package builder plugin to use.",
    },
    "pkg_tgt": {
        "default": None,
        "help": "Specify the os/distribution target to build the package against.",
    },
    "srcdir": {
        "default": None,
        "help": (
            "Instead of reading in a requirements.txt file, install all of the python "
            "package sources and/or wheels found in the specific directory"
        ),
    },
    "system_copy_in": {
        "default": None,
        "help": (
            "A list of directories to copy into the build venv that are not otherwise "
            "detected"
        ),
    },
    "tgt_version": {
        "default": None,
        "help": "Target package version",
    },
    "venv_plugin": {
        "default": "builtin",
        "help": "The python virtual environment plugin to use",
    },
    "python_bin": {
        "default": None,
        "type": str,
        "help": "The path to the python binary to use for system calls",
    },
    "omit": {
        "default": None,
        "help": "File globs to omit so that un-needed files can be removed",
    },
    "timeout": {
        "default": 300,
        "type": int,
        "help": ("Amount of time in seconds before considering a command has failed"),
    },
    "pip_version": {
        "default": "latest",
        "help": (
            "The version of pip for tiamat to utilize from pypi.  If 'latest' is "
            "specified it will utilize the latest release from pypi, otherwise specify"
            "the desired version, for example: '20.2.4'"
        ),
    },
    "use_static_requirements": {
        "os": "USE_STATIC_REQUIREMENTS",
        "default": True,
        "help": ("Use static requirements to build packages with, for example: Salt"),
    },
}
SUBCOMMANDS = {
    "pyinstaller": {
        "desc": "Build a dedicated project into an artifact using pyinstaller",
        "help": "Build a dedicated project into an artifact using pyinstaller",
    },
    "build": {
        "desc": "Build a dedicated project into an artifact using pyinstaller",
        "help": "Build a dedicated project into an artifact using pyinstaller",
    },
    "clean": {
        "desc": "Remove the build and dist directories",
        "help": "Remove the build and dist directories",
    },
    "install": {
        "desc": "Download a project from pypi, then build and install it locally",
        "help": "Download a project from pypi, then build and install it locally",
    },
}

# If tiamat is running from a binary, add a subcommand to read it's contents
if getattr(sys, "frozen", False):
    SUBCOMMANDS["freeze"] = {
        "desc": "List the python packages that are bundled in the app",
        "help": "List the python packages that are bundled in the app",
    }

DYNE = {
    "tiamat": ["tiamat"],
    "virtualenv": ["virtualenv"],
    "builder": ["builder"],
    "package": ["package"],
    "tool": ["tool"],
}
