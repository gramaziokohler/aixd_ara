#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# flake8: noqa
from __future__ import absolute_import
from __future__ import print_function

import io
from os import path

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

here = path.abspath(path.dirname(__file__))


def read(*names, **kwargs):
    return io.open(path.join(here, *names), encoding=kwargs.get("encoding", "utf8")).read()


long_description = read("README.md")
requirements = read("requirements.txt").split("\n")

setup(
    name="aixd_ara",
    version="0.10.6",
    description="Grasshopper plugin for the AIXD toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gramaziokohler/aixd_ara",
    author="Aleksandra Apolinarska",
    author_email="apolinarska@arch.ethz.ch",
    license="MIT license",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords=[],
    project_urls={},
    packages=["aixd_ara", "compas_aixd"],
    package_dir={"": "src"},
    package_data={},
    data_files=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    python_requires=">=3.8",
    extras_require={
        "dev": [
            "attrs >=17.4",
            "black",
            "bump2version >=1.0.1",
            "check-manifest >=0.36",
            "compas_invocations >=1.0.0",
            "doc8",
            "flake8",
            "invoke >=0.14",
            "isort",
            "pytest >=6.0",
            "sphinx_compas2_theme",
            "twine",
            "wheel",
        ],
    },
    entry_points={
        "console_scripts": [],
    },
    ext_modules=[],
)
