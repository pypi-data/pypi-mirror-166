def build(hub, bname: str):
    """
    Given the build arguments, Make a package!

    :param bname: The name of the build configuration to use from the build.conf file.
    """
    pkg_builder = hub.OPT.tiamat.pkg_builder
    hub.package[pkg_builder].build(bname)
