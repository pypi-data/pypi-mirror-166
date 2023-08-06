import os

__func_alias__ = {"compile_": "compile"}


def compile_(hub, directory: str, requirements: str) -> str:
    """
    Write all the requirements from opts to a temporary build requirements file
    """
    # Make a requirements file
    req = os.path.join(directory, "__build_requirements.txt")
    with open(requirements) as rfh:
        data_ = rfh.read()
    with open(req, "w+") as wfh:
        wfh.write(data_)

    return req
