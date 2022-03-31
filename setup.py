#! /usr/bin/python3
# -*- coding: utf-8 -*-

##############################################################################
# Copyright 20** AlexPDev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################
"""Setup package."""

import json

from setuptools import find_packages, setup


def get_info():
    """Gather information from package files."""
    info = json.load(open("package.json"))
    info["long_description"] = open("README.md").read()
    return info


INFO = get_info()


setup(
    url=INFO["url"],
    name=INFO["name"],
    author=INFO["author"],
    license=INFO["license"],
    version=INFO["version"],
    keywords=INFO["keywords"],
    include_package_data=True,
    author_email=INFO["email"],
    description=INFO["description"],
    long_description=INFO["long_description"],
    packages=find_packages(exclude=[".env"]),
    install_requires=["torrentfile", "pyben", "PySide6"],
    project_urls={"Source Code": "https://github.com/alexpdev/torrentfileQt"},
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": "torrentfileQt = torrentfileQt.window:start"
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
    ],
)
