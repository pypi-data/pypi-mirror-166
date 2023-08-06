"""
Routines to manage the setup and invocation of pyinstaller.
"""
import os
import shutil


def call(hub, bname: str):
    """
    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    dname = os.path.dirname(opts.s_path)
    if not os.path.isdir(dname):
        os.makedirs(os.path.dirname(opts.s_path))
    shutil.copy(opts.run, opts.s_path)
    hub.tiamat.cmd.run(opts.cmd, timeout=opts.timeout, fail_on_error=True)
