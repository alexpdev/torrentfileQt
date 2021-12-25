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
import os
import shutil
import string
import sys
from datetime import datetime
from pathlib import Path

import pytest
from torrentfile import TorrentFile, TorrentFileHybrid, TorrentFileV2

from torrentfileQt import alt_start

WINDOW, APP = alt_start()


def exception_hook(exctype, value, traceback):  # pragma:  no cover
    """Except hook capturing."""
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)


def tempfile(path=None, exp=18):
    """Create temporary file.

    Creates a temporary file for unittesting purposes.py

    Parameters
    ----------
    path : str, optional
        relative path to temporary files, by default None
    exp : int, optional
        Exponent used to determine size of file., by default 18

    Returns
    -------
    str
        absolute path to file.
    """
    seq = (string.printable + string.whitespace).encode("utf-8")
    root = Path(__file__).parent / "TESTDIR"
    if not os.path.exists(root):
        os.mkdir(root)
    if not path:
        path = root / (str(datetime.timestamp(datetime.now())) + ".file")
    parts = Path(path).parts
    partial = root
    for i, part in enumerate(parts):
        partial = partial / part
        if i == len(parts) - 1:
            with open(partial, "wb") as binfile:
                size = 2 ** exp
                while size > 0:
                    if len(seq) < size:
                        binfile.write(seq)
                        size -= len(seq)
                        seq += seq
                    else:
                        binfile.write(seq[:size])
                        size -= size
        else:
            if not os.path.exists(partial):
                os.mkdir(partial)
    return partial


def rmpath(*args):
    """Remove file or directory path.

    Parameters
    ----------
    args : list[str]
        Filesystem locations for removing.
    """
    for arg in args:
        if not os.path.exists(arg):
            continue
        if os.path.isdir(arg):
            try:
                shutil.rmtree(arg)
            except PermissionError:  # pragma: nocover
                pass
        elif os.path.isfile(arg):
            try:
                os.remove(arg)
            except PermissionError:  # pragma: nocover
                pass


def tempdir(ext="1", files=None):
    """Create temporary directory.

    Parameters
    ----------
    ext : str, optional
        extension to file names, by default "1"
    files : `list`
        alternate list of files.

    Returns
    -------
    str
        path to common root for directory.
    """
    if not files:
        files = [
            f"dir{ext}/file1.png",
            f"dir{ext}/file2.mp4",
            f"dir{ext}/file3.mp3",
            f"dir{ext}/file4.zip",
        ]
    paths = []
    for path in files:
        temps = tempfile(path=path, exp=18)
        paths.append(temps)
    return os.path.commonpath(paths)


@atexit.register
def teardown():  # pragma: nocover
    """Remove all temporary directories and files."""
    APP.quit()
    root = Path(__file__).parent / "TESTDIR"
    if os.path.exists(root):
        rmpath(root)


@pytest.fixture(scope="package")
def dir1():
    """Create a specific temporary structured directory.

    Yields
    ------
    str
        path to root of temporary directory
    """
    root = tempdir()
    yield root
    rmpath(root)


@pytest.fixture
def dir2():
    """Create a specific temporary structured directory2.

    Yields
    ------
    str
        path to root of temporary directory
    """
    root = tempdir(ext="2")
    yield root
    rmpath(root)


@pytest.fixture
def dir3():
    """Create a specific temporary structured directory3.

    Yields
    ------
    str
        path to root of temporary directory
    """
    files = [
        "dir3/subdir/file1.jpg",
        "dir3/file2.zip",
        "dir3/subdir/subsubdir/file3.mp3",
        "dir3/file4.txt",
        "dir3/subdir/file5.epub"
    ]
    root = tempdir(files=files)
    yield root
    rmpath(root)


@pytest.fixture(scope="package")
def wind():
    """
    Create a window and application for testing.

    Returns
    -------
    `tuple`
        information to pass to test function.
    """
    window, app = WINDOW, APP
    return window, app


@pytest.fixture(params=[TorrentFile, TorrentFileHybrid, TorrentFileV2])
def ttorrent(request, dir2):
    """
    Generate a metafile for testing.

    Parameters
    ----------
    request : MetaFile
        an instance of torrentfile creator.
    dir2 : `str`
        path to temporary directory

    Yields
    ------
    `str`
        path to new .torrent file.
    """
    args = {
        "path": dir2,
        "outfile": str(dir2) + "t.torrent",
        "comment": "This is a comment",
        "source": "SomeSource",
        "private": 1
    }

    torrent = request.param(**args)
    outfile, _ = torrent.write()
    yield outfile
    rmpath(outfile)
