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

import os
from pathlib import Path

import pytest
from torrentfile import TorrentFile, TorrentFileHybrid, TorrentFileV2

from tests.context import rmpath, tstdir, tstdir2, tstfile
from torrentfileQt.window import alt_start


@pytest.fixture(scope="module")
def wind():
    window, app = alt_start()
    yield window
    app.quit()


@pytest.fixture(scope="module", params=[tstdir, tstdir2])
def tdir(request):
    root = request.param()
    yield root
    rmpath(root)


@pytest.fixture(scope="module", params=list(range(12, 26)))
def tfile(request):
    path = tstfile(val=request.param)
    yield path
    rmpath(path)


@pytest.mark.parametrize(
    "hasher", [TorrentFile, TorrentFileV2, TorrentFileHybrid]
)
def test_missing_files_check(hasher, wind, tdir):
    checktab = wind.central.checkWidget
    args = {"path": tdir}
    torrent = hasher(**args)
    metafile, _ = torrent.write()
    contents = tdir
    dir1 = Path(contents) / "dir1"
    for item in dir1.iterdir():
        if item.is_file():
            os.remove(item)
    checktab.fileInput.setText(metafile)
    checktab.searchInput.setText(contents)
    checktab.checkButton.click()
    assert checktab.treeWidget.topLevelItemCount() > 0
    rmpath(metafile)


# @pytest.mark.parametrize("hasher", [TorrentFile, TorrentFileV2,
#                                     TorrentFileHybrid])
# def test_check_2tab5(hasher, wind, tdir):
#     checktab = wind.central.checkWidget
#     args = {"path": tdir, "piece_length": 2**21}
#     torrent = hasher(**args)
#     metafile, _ = torrent.write()
#     contents = tdir
#     checktab.fileInput.setText(metafile)
#     checktab.searchInput.setText(contents)
#     checktab.checkButton.click()
#     assert checktab.textEdit.toPlainText() != ""
#     rmpath(metafile)


@pytest.mark.parametrize(
    "hasher", [TorrentFile, TorrentFileV2, TorrentFileHybrid]
)
def test_check_2tab(hasher, wind, tfile):
    checktab = wind.central.checkWidget
    args = {"path": tfile}
    torrent = hasher(**args)
    metafile, _ = torrent.write()
    contents = tfile
    checktab.fileInput.setText(metafile)
    checktab.searchInput.setText(contents)
    checktab.checkButton.click()
    assert checktab.textEdit.toPlainText() != ""
    rmpath(metafile)


def test_check_tab4(wind):
    checktab = wind.central.checkWidget
    tree_widget = checktab.treeWidget
    assert tree_widget.invisibleRootItem() is not None
