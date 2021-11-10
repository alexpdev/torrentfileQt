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
    name=INFO["name"],
    version=INFO["version"],
    description=INFO["description"],
    long_description=INFO["long_description"],
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
    ],
    keywords=INFO["keywords"],
    author=INFO["author"],
    author_email=INFO["email"],
    url=INFO["url"],
    project_urls={"Source Code": "https://github.com/alexpdev/torrentfileQt"},
    license=INFO["license"],
    packages=find_packages(exclude=["env"]),
    entry_points={"console_scripts": "torrentfileQt = torrentfileQt.window:start"},
    include_package_data=True,
    tests_require=["pytest"],
    install_require=INFO["torrentfile", "PyQt6", "pyben"],
    setup_requires=["setuptools", "wheel"],
    zip_safe=False,
    test_suite="complete",
)
