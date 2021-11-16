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
"""Setup and Teardown functions and fixtures used for Unit Tests."""

import atexit
import inspect
import os
import shutil
import string
import sys
import time
from datetime import datetime
from pathlib import Path

from torrentfile import TorrentFile, TorrentFileHybrid, TorrentFileV2

from torrentfileQt import alt_start


def rmpath(paths):
    """Remove File or Folder.

    Args:
        paths (`str` or `list`): File or Folder to delete.
    """
    if isinstance(paths, (str, os.PathLike)):
        paths = [paths]
    for path in paths:
        if os.path.exists(path):
            if os.path.isfile(path):
                func = os.remove
            else:
                func = shutil.rmtree
            try:
                func(path)
            except PermissionError:
                pass


def exception_hook(exctype, value, traceback):  # pragma:  no cover
    """Except hook capturing."""
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)


class Temp:
    """Namespace for global objects."""

    sys._excepthook = sys.excepthook
    sys.excepthook = exception_hook

    window, app = alt_start()
    testdir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.join(testdir, "TESTINGDIR")

    hashers = [TorrentFile, TorrentFileV2, TorrentFileHybrid]
    seq = string.printable + string.hexdigits + string.whitespace

    if not os.path.exists(root):
        os.mkdir(root)


def fillfile(filepath, size=21):
    """Fill temp files with content."""
    seq = Temp.seq * 8
    size = 2 ** size
    with open(filepath, "bw") as binfile:
        while size > 0:
            binfile.write(seq.encode("utf-8"))
            size -= len(seq)


def build(paths, size=21):
    """Build temporary paths provided."""
    stamp = str(datetime.timestamp(datetime.now()))
    funcname = inspect.stack()[1].function
    base = os.path.join(Temp.root, stamp + funcname)
    os.mkdir(base)
    for path in paths:
        parts = Path(path).parts
        bottom = base
        for part in parts[0:-1]:
            folder = os.path.join(bottom, part)
            if not os.path.exists(folder):
                os.mkdir(folder)
            bottom = folder
        filepath = os.path.join(base, path)
        fillfile(filepath, size=size)
    return base


def pathstruct():
    """Temporary directory fcr testing."""
    return [
        [
            "dir1/file1.bin",
            "dir2/file2.bin",
            "dir1/file3.bin",
            "file4.bin",
        ],
        [
            "dir1/dir2/file1.bin",
            "dir1/dir2/file2.bin",
            "dir3/file3.bin",
            "dir1/file4.bin",
            "dir3/file5.bin",
        ],
        [
            "dir1/file1.bin",
            "dir1/file2.bin",
            "dir1/file3.bin",
            "dir1/file4.bin",
            "dir1/file5.bin",
        ],
        [f"file1{str(datetime.timestamp(datetime.now()))}"],
    ]


def mktorrent(path, hasher=None):
    """Create .torrent file."""
    kwargs = {
        "path": path,
        "private": True,
        "announce": ["announce1", "announce2", "announce3"],
        "source": "source243324",
        "comment": "this",
    }
    torrent = hasher(**kwargs)
    outfile, _ = torrent.write()
    return outfile


@atexit.register
def teardown():
    """Remove temporary directories."""
    try:
        rmpath(Temp.root)
    except PermissionError:  # pragma: no cover
        time.sleep(0.5)
        teardown()
