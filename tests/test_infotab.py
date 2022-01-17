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
"""Testing module for most of GUI."""

import pytest
from torrentfile import TorrentFile, TorrentFileHybrid, TorrentFileV2

from tests import dir2, dir3, rmpath, tempfile, ttorrent, wind


def test_fixture():
    """Test fixtures."""
    assert dir2 and tempfile and ttorrent and wind and dir3


def test_info_tab_select1(wind, ttorrent):
    """Test Info tab select1."""
    window, app = wind
    infotab = window.central.infoWidget
    app.processEvents()
    window.central.setCurrentWidget(infotab)
    button = infotab.selectButton
    button.selectTorrent(path=ttorrent)
    assert infotab.nameEdit.text() != ""


@pytest.mark.parametrize(
    "creator", [TorrentFile, TorrentFileV2, TorrentFileHybrid]
)
def test_infotab_select2(wind, dir2, creator):
    """Test getting info for single file torrent."""
    window, app = wind
    torrent = creator(path=dir2)
    del torrent.meta["created by"]
    del torrent.meta["creation date"]
    del torrent.meta["announce-list"]
    outfile, _ = torrent.write()
    infotab = window.central.infoWidget
    app.processEvents()
    window.central.setCurrentWidget(infotab)
    button = infotab.selectButton
    button.selectTorrent(path=outfile)
    name = torrent.meta["info"]["name"]
    assert infotab.nameEdit.text() == name
    rmpath(outfile)


@pytest.mark.parametrize(
    "creator", [TorrentFile, TorrentFileV2, TorrentFileHybrid]
)
@pytest.mark.parametrize("size", list(range(16, 22)))
def test_infotab_single(wind, creator, size):
    """Test getting info for single file torrent."""
    window, app = wind
    tfile = tempfile(exp=size)
    torrent = creator(path=tfile)
    del torrent.meta["created by"]
    del torrent.meta["creation date"]
    del torrent.meta["announce-list"]
    outfile, _ = torrent.write()
    infotab = window.central.infoWidget
    app.processEvents()
    window.central.setCurrentWidget(infotab)
    button = infotab.selectButton
    button.selectTorrent(path=outfile)
    name = torrent.meta["info"]["name"]
    assert infotab.nameEdit.text() == name
    rmpath(outfile)


@pytest.mark.parametrize(
    "creator", [TorrentFile, TorrentFileV2, TorrentFileHybrid]
)
def test_infotab_nested(wind, creator, dir3):
    """Test getting info for single file torrent."""
    window, app = wind
    torrent = creator(path=dir3)
    del torrent.meta["created by"]
    del torrent.meta["creation date"]
    del torrent.meta["announce-list"]
    outfile, _ = torrent.write()
    infotab = window.central.infoWidget
    app.processEvents()
    window.central.setCurrentWidget(infotab)
    button = infotab.selectButton
    button.selectTorrent(path=outfile)
    name = torrent.meta["info"]["name"]
    assert infotab.nameEdit.text() == name
    rmpath(outfile)
