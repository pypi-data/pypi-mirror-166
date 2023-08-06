def sig_new(hub, *args, **kwargs) -> dict[str, any]:
    """
    Collect all the arguments from the opts needed for a build.
    """


def sig_run(hub, build_name: str):
    """
    Make the calls to perform the build process using the OPTs in "build_name"
    """
    # Build opts can be retrieved using the build name
    hub.tiamat.BUILDS[build_name]

    # A generic virtualenv plugin can be created within which to run the build
    hub.virtualenv.init.create(build_name)

    # Helper functions can be called from hub.tool
    # This allows for organization of code so that everything doesn't need to be crammed into one giant file
    hub.tool["my_build_plugin_metadir"].helper_plugin.function(build_name)


def sig_clean(hub, build_name: str):
    """
    Clean up virtual environments and intermediate files after a build
    """
