#! /usr/bin/python3
# -*- coding: utf-8 -*-

#############################################################################
# Copyright (C) 2021 alexpdev
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
############################################################################
"""Setup package."""

import json

from setuptools import find_packages, setup

INFO = json.load(open("package.json"))
INFO["long_description"] = open("README.md").read()
with open("requirements.txt") as req:
    INFO["install_requires"] = req.read().split("\n")

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
    packages=find_packages(exclude=["env", "tests"]),
    install_requires=["torrentfile", "PyQt6", "pyben"],
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
