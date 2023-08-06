"""
The build plugin is used to execute the build routines for non-python components.
"""
import pprint
import uuid

import dict_tools.data as data


def new(hub, builder_plugin: str, build_name: str = None, **opt) -> str:
    """
    Process the given opts through the builder plugin.
    The opts are put onto the hub.tiamat.BUILDS structure using an assigned run name
    """
    if builder_plugin == "init":
        raise RecursionError("Cannot call builder.init from builder.init")

    if not build_name:
        # Get a semi-random string for the build name
        build_name = str(uuid.uuid1())

    if build_name in hub.tiamat.BUILDS:
        raise ValueError(f"Build '{build_name}' already exists")

    # Add the new build opts from the build plugin to the binary
    new_build = hub.builder[builder_plugin].new(**opt)
    hub.tiamat.BUILDS[build_name] = data.NamespaceDict(new_build)

    # Verify that the plugin used to use these options is kept with the build name
    hub.tiamat.BUILDS[build_name].builder_plugin = builder_plugin
    hub.log.debug(
        f"Build config '{build_name}':\n{pprint.pformat(hub.tiamat.BUILDS[build_name])}"
    )
    return build_name


def run_all(hub, **opt):
    """
    Run all the builds in hub.tiamat.BUILDS
    When needed, this can easily be modified to run multiple builds at once in a process pool
    """
    for build_name in hub.tiamat.BUILDS.keys():
        hub.builder.init.run(
            builder_plugin=hub.tiamat.BUILDS[build_name]["builder_plugin"],
            build_name=build_name,
            **opt,
        )


def run(
    hub,
    builder_plugin: str,
    build_name: str,
    pkg_tgt: str = None,
    no_clean: bool = True,
    **opt,
):
    # Start performing the actual build
    hub.builder[builder_plugin].run(build_name)

    # Run packaging plugins on the build
    if pkg_tgt:
        hub.package.init.build(build_name)

    # Clean up after the build
    if not no_clean:
        hub.builder[builder_plugin].clean(build_name)
