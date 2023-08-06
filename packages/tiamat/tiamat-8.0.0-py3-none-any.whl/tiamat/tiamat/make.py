import glob
import os
import shutil
import tempfile

import requests


def apply(hub, build_name: str):
    """
    Run the commands listed under the "make" config option.
    It is up to each builder plugin to call this itself.

    :param hub: The redistributed pop central hub.
    :param build_name: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[build_name]
    build = opts.build
    if not build:
        return
    bdir = tempfile.mkdtemp()
    cur_dir = os.getcwd()
    try:
        os.chdir(bdir)
        if opts.srcdir:
            for fn in os.listdir(opts.srcdir):
                shutil.copy(os.path.join(opts.srcdir, fn), bdir)
        for proj, conf in build.items():
            if not opts.srcdir:
                if "sources" in conf:
                    sources = conf["sources"]
                    if isinstance(sources, str):
                        sources = [sources]
                    for source in sources:
                        response = requests.get(source)
                        with open(
                            os.path.join(bdir, os.path.split(source)[1]), "wb"
                        ) as file:
                            file.write(response.content)
            if "make" in conf:
                for cmd in conf["make"]:
                    hub.tiamat.cmd.run(
                        cmd,
                        shell=True,
                        cwd=bdir,
                        timeout=opts.timeout,
                        fail_on_error=True,
                    )
            if "src" in conf and "dest" in conf:
                srcs = conf["src"]
                dest = os.path.join(opts.venv_dir, conf["dest"])
                hub.log.info(f"Copying: {srcs}->{dest}")
                if not isinstance(srcs, (list, tuple)):
                    srcs = [srcs]
                final_srcs = set()
                for src in srcs:
                    globed = glob.glob(src)
                    if not globed:
                        hub.log.warning(
                            f"Expression f{src} does not match any file paths"
                        )
                        continue
                    final_srcs.update(globed)
                for src in final_srcs:
                    fsrc = os.path.join(bdir, src)
                    if os.path.isfile(fsrc):
                        try:
                            shutil.copy(fsrc, dest, follow_symlinks=True)
                        except OSError as e:
                            hub.log.warning(
                                f"Unable to copy file {fsrc} to {dest}: {e}"
                            )
                            hub.tiamat.BUILDS[build_name].binaries.append(
                                (os.path.join(dest, os.path.basename(fsrc)), ".")
                            )
                    elif os.path.isdir(fsrc):
                        try:
                            fdest = os.path.join(dest, src)
                            shutil.copytree(fsrc, fdest)
                        except OSError as e:
                            hub.log.warning(
                                f"Unable to copy dir {fsrc} to {fdest}: {e}"
                            )
                    else:
                        hub.log.warning(f"FAILED TO FIND FILE {fsrc}")
    finally:
        os.chdir(cur_dir)
