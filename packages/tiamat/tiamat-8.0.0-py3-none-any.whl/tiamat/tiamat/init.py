import os
import sys


def __init__(hub):
    """
    Initialize the structure of the project
    """
    hub.pop.sub.load_subdirs(hub.tiamat)
    hub.pop.sub.add(dyne_name="virtualenv")
    hub.pop.sub.add(dyne_name="package")
    hub.pop.sub.add(dyne_name="builder")
    hub.pop.sub.add(dyne_name="tool")
    hub.pop.sub.load_subdirs(hub.tool, recurse=True)

    # Multiple builds can be run at once, this structure contains the OPTs for all running builds
    hub.tiamat.BUILDS = {}


def cli(hub):
    """
    Execute a single build routine from the CLI.

    :param hub: The redistributed pop central hub.
    """
    hub.pop.config.load(["tiamat"], cli="tiamat")
    if hub.SUBPARSER == "clean":
        hub.tiamat.clean.all(hub.OPT.tiamat.directory)
    elif hub.SUBPARSER == "freeze":
        if getattr(sys, "frozen", False):
            freeze = os.path.join(sys._MEIPASS, "app_freeze.txt")
            with open(freeze) as fh:
                print(fh.read())
        else:
            raise OSError(
                "freeze can only be called when tiamat is run as a pyinstaller binary"
            )
    elif hub.SUBPARSER is None:
        hub.config.ARGS["parser"].print_help()
        sys.exit()

    if hub.SUBPARSER == "build":
        builder_plugin = "pyinstaller"
    else:
        builder_plugin = hub.SUBPARSER

    # Indicate to pipelines that a build is starting
    os.environ["POP_BUILD"] = "1"
    os.environ["TIAMAT_BUILD"] = "1"

    # Initialize a new build in hub.tiamat.BUILDS
    build_name = hub.builder.init.new(builder_plugin=builder_plugin, **hub.OPT.tiamat)
    # Run all the builds in the hub.tiamat.BUILDS
    hub.builder.init.run_all(**hub.OPT.tiamat)
    # Report on the one build created from this cli
    hub.tiamat.post.report(build_name=build_name)
