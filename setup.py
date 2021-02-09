#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from setuptools import find_packages, setup


def get_parent_dir():
    return Path(__file__).resolve().parent


def read_relative_to_cwd(*path_tokens: str, encoding: str = "utf-8") -> str:
    try:
        with open(get_parent_dir().joinpath(*path_tokens), encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        return ""


PACKAGE_NAME = "FacebookTuring"
SHARED_LIBRARIES = ["Core"]
PACKAGE_DIRS = [PACKAGE_NAME] + SHARED_LIBRARIES
CONSOLE_SCRIPTS = {
    "api-server": "Api.app:app",
    "rabbit-worker": "BackgroundTasks.app:app",
}
# SOURCES_ROOT = "src"

setup(
    name=PACKAGE_NAME,
    version="0.1",
    description=PACKAGE_NAME,
    # long_description=read("README.md"),
    packages=find_packages(),
    # packages=find_packages(SOURCES_ROOT),
    package_dir={p: p for p in PACKAGE_DIRS},
    # package_dir={"": SOURCES_ROOT},
    # py_modules=[p.stem for p in Path(SOURCES_ROOT).glob("*.py")],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[read_relative_to_cwd("requirements.txt").splitlines()],
    entry_points={"console_scripts": [f"{PACKAGE_NAME}-{k} = {PACKAGE_NAME}.{v}" for k, v in CONSOLE_SCRIPTS.items()]},
)
