import os
import pathlib
import shutil
import tempfile


def new(
    hub,
    *,
    name: str = None,
    requirements: str,
    system_site: bool = False,
    exclude: list[str] = None,
    directory: str,
    pyinstaller_version: str = "4.10",
    pyinstaller_runtime_tmpdir: str = None,
    pkg: str = None,
    onedir: bool = False,
    pyenv: str = "system",
    run: str = "run.py",
    locale_utf8: bool = False,
    dependencies: str = None,
    release: str = None,
    pkg_tgt: str = None,
    pkg_builder: str = None,
    srcdir: str = None,
    system_copy_in: list[str] = None,
    tgt_version: str = None,
    python_bin: str = None,
    omit: list[str] = None,
    venv_plugin: str = None,
    pyinstaller_args: list[str] = None,
    timeout: int = 300,
    pip_version: str = "latest",
    venv_uninstall: list[str] = None,
    use_static_requirements: bool = True,
    datas: set = None,
    build: bool = None,
    **opt,
) -> dict[str, any]:
    """
    Collect all the arguments needed for a build

    :param hub: The redistributed pop central hub.
    :param name: The name of the project to build.
    :param requirements: The name of the requirements.txt file to use.
    :param system_site: Include the system site-packages when building.
    :param exclude: A list of exclude files or python modules, these python packages
        will be ignored by pyinstaller
    :param directory: The path to the directory to build from.
        This denotes the root of the python project source tree to work from.
        This directory should have the setup.py and the paths referenced in
        configurations will assume that this is the root path they are working from.
    :param pyinstaller_version: The version of pyinstaller to use for packaging
    :param pyinstaller_runtime_tmpdir: Pyinstaller runtime tmpdir.
    :param datas: PyInstaller datas mapping
    :param build: Enter in commands to build a non-python binary into the
        deployed binary.
        The build options are set on a named project basis. This allows for multiple
        shared binaries to be embedded into the final build:

    .. code-block:: yaml

        build:
          libsodium:
            make:
              - wget libsodium
              - tar xvf libsodium*
              - cd libsodium
              - ./configure
              - make
            src: libsodium/libsodium.so
            dest: lib64/

    :param pkg: Options for building packages.
    :param onedir: Instead of producing a single binary produce a directory with
        all components.
    :param pyenv: The python version to build with.
    :param run: The location of the project run.py file.
    :param locale_utf8: Use the UTF-8 locale with PyInstaller, as in PEP538 and PEP540.
    :param dependencies: Comma separated list of dependencies needed for the build.
    :param release: Release string i.e. '1.el7'.
    :param pkg_tgt: The os/distribution target to build the package against.
    :param pkg_builder: The package builder plugin to use.
    :param srcdir: Install all of the python package sources and/or wheels found in
        this directory.
    :param system_copy_in: A list of directories to copy into the build venv that are
        not otherwise detected.
    :param tgt_version: Target package version.
    :param python_bin: The python binary to use for system calls
    :param omit: Omit files by glob
    :param pyinstaller_args: Args to pass straight through to pyinstaller
    :param venv_plugin: The virtualenvironment plugin to use
    :param timeout: The amount of time (seconds) before a command is considered to
        have failed
    :param pip_version: The version of pip to use while packaging
    :param venv_uninstall: A list of packages to remove from the final virtual environment
    :param use_static_requirements: Use static requirements to build packages with
        for example: Salt

    """
    if opt:
        hub.log.debug(
            f"OPTs that are unused by the pyinstaller plugin: {', '.join(opt.keys())}"
        )

    # Get the name of the binary from the target path if it is not supplied as an opt
    if name == "." or name is None:
        name = os.path.basename(os.path.abspath("."))

    # Create a temporary directory for the virtualenv
    venv_dir = tempfile.mkdtemp()

    # Determine if this is running on windows
    is_win = os.name == "nt"

    # Find the location of the python binary if it wasn't explicitly supplied
    if python_bin is None:
        if is_win:
            python_bin = os.path.join(venv_dir, "Scripts", "python")
        else:
            python_bin = os.path.join(venv_dir, "bin", "python3")

    # Determine the path to the entrypoint script for this build
    if is_win:
        s_path = os.path.join(venv_dir, "Scripts", name)
    elif locale_utf8:
        s_path = "env PYTHONUTF8=1 LANG=POSIX " + os.path.join(venv_dir, "bin", name)
    else:
        s_path = os.path.join(venv_dir, "bin", name)

    # Transform None types into collections
    if datas is None:
        datas = set()

    if exclude is None:
        exclude = []

    if pyinstaller_args is None:
        pyinstaller_args = []

    # Put together the pyinstaller command
    cmd = [python_bin, "-B", "-O", "-m", "PyInstaller"]

    # Determine the python modules that should be excluded
    excluded = set()
    for ex in exclude:
        if os.path.isfile(ex):
            with open(ex) as exf:
                for line in exf:
                    line = line.strip()
                    if line:
                        excluded.add(line)
        else:
            excluded.add(ex)

    # Get the absolute path of the directory to build from
    dir_ = os.path.abspath(directory)

    # Get the path to the requirements file of the project in the build directory
    requirements = os.path.join(directory, requirements)

    # Make a requirements file
    req = hub.tool.pyinstaller.requirements.compile(
        directory=dir_, requirements=requirements
    )

    # Get the target version
    if tgt_version:
        version = tgt_version
    else:
        version = hub.tiamat.data.version(directory=dir_, name=name)

    build = dict(
        name=name,
        build=build,
        pkg=pkg,
        pkg_tgt=pkg_tgt,
        pkg_builder=pkg_builder,
        dependencies=dependencies,
        release=release,
        binaries=[],
        is_win=is_win,
        exclude=excluded,
        requirements=requirements,
        sys_site=system_site,
        dir=dir_,
        srcdir=srcdir,
        pyinstaller_version=pyinstaller_version,
        pyinstaller_runtime_tmpdir=pyinstaller_runtime_tmpdir,
        system_copy_in=system_copy_in,
        run=os.path.join(directory, run),
        spec=os.path.join(directory, f"{name}.spec"),
        pybin=python_bin,
        s_path=s_path,
        venv_dir=venv_dir,
        vroot=os.path.join(venv_dir, "lib"),
        onedir=onedir,
        all_paths=set(),
        imports=set(),
        datas=datas,
        cmd=cmd,
        pyenv=pyenv,
        pypi_args=[
            s_path,
            "--log-level=INFO",
            "--noconfirm",
            "--onedir" if onedir else "--onefile",
            "--clean",
        ]
        + list(pyinstaller_args),
        venv_uninstall=venv_uninstall,
        locale_utf8=locale_utf8,
        omit=omit,
        venv_plugin=venv_plugin,
        timeout=timeout,
        pip_version=pip_version,
        use_static_requirements=use_static_requirements,
        req=req,
        version=version,
    )
    return build


def run(hub, build_name: str):
    """
    Run pyinstaller and perform the build
    """
    # Initialize a new virtual environment for the build to occur in
    hub.virtualenv.init.create(build_name)
    hub.virtualenv.init.scan(build_name)
    hub.virtualenv.init.mk_adds(build_name)

    # Run the commands listed in the 'make' portion of the build config
    hub.tiamat.make.apply(build_name)

    # Call
    hub.tool.pyinstaller.spec.mk_spec(build_name)
    hub.tool.pyinstaller.runner.call(build_name)


def clean(hub, build_name: str):
    """
    Clean up virtual environments and intermediate files after a build
    """
    opts = hub.tiamat.BUILDS[build_name]
    try:
        shutil.rmtree(opts.venv_dir)
    except OSError:
        pathlib.Path(opts.venv_dir).unlink()
    os.remove(opts.spec)
    os.remove(opts.req)
    try:
        # try to remove pyinstaller warn-*** file
        os.remove(os.path.join(opts.dir, "build", opts.name, f"warn-{opts.name}.txt"))
    except FileNotFoundError:
        pass
