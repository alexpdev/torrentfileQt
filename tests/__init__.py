#! /usr/bin/python3
# -*- coding: utf-8 -*-

##############################################################################
# Copyright 2020 AlexPDev
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
"""Unit tests and fixtures for torrentfileQt Application."""

import atexit
import itertools
import os
import random
import shutil
import string
import sys
import time
from tempfile import mkdtemp, mkstemp

import pytest
from torrentfile.torrent import TorrentFile, TorrentFileHybrid, TorrentFileV2

from torrentfileQt import Application

APP = Application.start()


class TempFileDirs:
    """Class for temporary files."""

    paths = set()

    tempdir = mkdtemp()
    paths.add(tempdir)

    @classmethod
    def cleanup(cls):  # pragma: nocover
        """Clean up temporary files."""
        cleaned = set()
        for i in cls.paths:
            if not os.path.exists(i):
                continue
            if os.path.isfile(i):
                os.remove(i)
            else:
                shutil.rmtree(i)
            cleaned.add(i)
        cls.paths -= cleaned


def switchTab(stack, widget=None, index=None):
    """Switch to new tab."""
    if not widget:
        stack.setCurrentIndex(index)  # pragma: nocover
    else:
        stack.setCurrentWidget(widget)
    APP.processEvents()


def waitfor(timeout: int, func, *args, **kwargs):
    """Wait for result to appear."""
    then = time.time()
    while time.time() - then < timeout:
        if func(*args, **kwargs):
            return True
        APP.processEvents()  # pragma: nocover
    return False  # pragma: nocover


def gen_seq():
    """Get random sequence."""
    printable = string.printable * 12
    whitespace = string.whitespace * 6
    characters = list(printable + whitespace)
    random.shuffle(characters)
    return "".join(characters)


def torrent_versions():
    """
    Return torrent file creators.
    """
    return (TorrentFile, TorrentFileHybrid, TorrentFileV2)


def temp_file(size, suffix=None, dir=None):
    """Create temporary file.

    Creates a temporary file for unittesting purposes.py

    Parameters
    ----------
    size : int
        size of files
    suffix : str, optional
        the suffix for the path
    dir : str, optional
        location of the temp file

    Returns
    -------
    str
        absolute path to file.
    """
    seq = gen_seq().encode("utf8")
    if not dir:
        dir = TempFileDirs.tempdir
    fd, path = mkstemp(suffix=suffix, dir=dir)
    with os.fdopen(fd, "bw") as fp:
        while size > 0:
            fp.write(seq)
            size -= len(seq)
    TempFileDirs.paths.add(path)
    return path


def tempdir(files: int, subdirs: int, size: int, suffixes=None):
    """Create temporary directory.

    Parameters
    ----------
    files : int
        number of files
    subdirs : int
        number of subdirectories
    size : int
        size of each file
    suffixes : list
        suffixes to be used for each file.

    Returns
    -------
    str
        path to common root for directory.
    """
    files_per_subdir = files // subdirs
    parent = mkdtemp(dir=TempFileDirs.tempdir)
    paths = []
    subdir = parent
    if not suffixes:
        suffixes = [""]  # pragma: nocover
    suffixes = itertools.cycle(suffixes)
    for _ in range(subdirs):
        path = mkdtemp(dir=subdir)
        TempFileDirs.paths.add(path)
        paths.append(path)
        subdir = path
    for path in paths:
        for _ in range(files_per_subdir):
            temp_file(size, dir=path, suffix=next(suffixes))
    TempFileDirs.paths.add(parent)
    return parent


@atexit.register
def teardown():  # pragma: nocover
    """Remove all temporary directories and files."""
    APP.quit()
    TempFileDirs.cleanup()


@pytest.fixture(scope="package")
def wind():
    """
    Create a window and application for testing.

    Returns
    -------
    `tuple`
        information to pass to test function.
    """
    window = APP.window
    return window


class MockEvent:
    """Imitate functionality of a QtEvent."""

    def __init__(self, path):
        """Construct event."""
        self.path = path
        self.accepted = False

    def accept(self):
        """Accept function."""
        self.accepted = True

    def ignore(self):
        """Ignore event."""
        self.accepted = False

    class MimeData:
        """Mock Qt MimeData class."""

        def __init__(self, text):
            """Construct mimeData class."""
            self.txt = text
            if self.txt == "":
                self.hasUrls = False
            else:
                self.hasUrls = True

        class URL:
            """URL Mock object."""

            def __init__(self, url):
                """Construct URL Mock object."""
                self.url = url

            def toLocalFile(self):
                """Convert URL to local path."""
                return self.url

        def urls(self):
            """Return the text passed to constructor."""
            return [self.URL(self.txt)]

    def mime_data(self):
        """Return a mock of Qt MimeData class."""
        if not self.path:
            mdata = self.MimeData("")
        else:
            mdata = self.MimeData(self.path)
        return mdata

    mimeData = mime_data
