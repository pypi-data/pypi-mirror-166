import os
import sys


def report(hub, build_name: str):
    """
    :param hub: The redistributed pop central hub.
    :param build_name: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[build_name]
    art = os.path.abspath(os.path.join("dist", opts.name))

    # This is the only print statement from the program, everything else gets logged
    # through stderr
    print(art, file=sys.stdout, flush=True)

    # Save the location of the result to an environment variable for CICD or
    # wrapper scripts
    os.environ["TIAMAT_BUILD_PACKAGE"] = art
