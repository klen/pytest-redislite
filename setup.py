import pathlib

import pkg_resources
from setuptools import setup


def parse_requirements(path: str) -> "list[str]":
    with pathlib.Path(path).open(encoding="utf-8") as requirements:
        return [str(req) for req in pkg_resources.parse_requirements(requirements)]


setup(install_requires=parse_requirements("requirements.txt"))
