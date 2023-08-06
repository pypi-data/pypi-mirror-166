import os


def version(hub, directory: str, name: str) -> str:
    """
    Gather the version number of the pop project if possible.

    :param hub: The redistributed pop central hub.
    :param directory: The target directory that contains the python project to build
    :param name: The name of the entrypoint binary
    """
    name = name.replace("-", "_")
    path = os.path.join(directory, name, "version.py")
    _locals = {}
    version_ = "1"
    try:
        if os.path.isfile(path):
            with open(path) as fp:
                exec(fp.read(), None, _locals)
                version_ = _locals["version"]
    except Exception:
        pass

    return version_
