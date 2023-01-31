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
from torrentfile.torrent import TorrentFile, TorrentFileHybrid, TorrentFileV2

from tests import (MockEvent, dir2, dir3, proc_time, rmpath, tempfile,
                   ttorrent, wind)
from torrentfileQt import infoTab


class Obj:
    value = None


def mock_func(_):
    return Obj.value


def test_fixture():
    """Test fixtures."""
    assert dir2 and tempfile and ttorrent and wind and dir3


def test_info_tab_select1(wind, ttorrent):
    """Test Info tab select1."""

    infotab = wind.tabs.infoWidget
    proc_time()
    wind.stack.setCurrentWidget(infotab)
    button = infotab.selectButton
    Obj.value = [ttorrent]
    infoTab.browse_torrent = mock_func
    button.selectTorrent()
    assert infotab.nameEdit.text() != ""


@pytest.mark.parametrize(
    "creator", [TorrentFile, TorrentFileV2, TorrentFileHybrid]
)
def test_infotab_select2(wind, dir2, creator):
    """Test getting info for single file torrent."""
    torrent = creator(path=dir2)
    del torrent.meta["created by"]
    del torrent.meta["creation date"]
    del torrent.meta["announce-list"]
    outfile, _ = torrent.write()
    infotab = wind.tabs.infoWidget
    proc_time()
    wind.stack.setCurrentWidget(infotab)
    button = infotab.selectButton
    Obj.value = [outfile]
    infoTab.browse_torrent = mock_func
    button.selectTorrent()
    name = torrent.meta["info"]["name"]
    assert infotab.nameEdit.text() == name
    rmpath(outfile, dir2)


@pytest.mark.parametrize(
    "creator", [TorrentFile, TorrentFileV2, TorrentFileHybrid]
)
@pytest.mark.parametrize("size", list(range(16, 22)))
def test_infotab_single(wind, creator, size):
    """Test getting info for single file torrent."""
    tfile = tempfile(exp=size)
    torrent = creator(path=tfile)
    del torrent.meta["created by"]
    del torrent.meta["creation date"]
    del torrent.meta["announce-list"]
    outfile, _ = torrent.write()
    infotab = wind.tabs.infoWidget
    proc_time()
    wind.stack.setCurrentWidget(infotab)
    button = infotab.selectButton
    Obj.value = [outfile]
    infoTab.browse_torrent = mock_func
    button.selectTorrent()
    name = torrent.meta["info"]["name"]
    assert infotab.nameEdit.text() == name
    rmpath(outfile, tfile)


@pytest.mark.parametrize(
    "creator", [TorrentFile, TorrentFileV2, TorrentFileHybrid]
)
def test_infotab_nested(wind, creator, dir3):
    """Test getting info for single file torrent."""
    torrent = creator(path=dir3)
    del torrent.meta["created by"]
    del torrent.meta["creation date"]
    del torrent.meta["announce-list"]
    outfile, _ = torrent.write()
    infotab = wind.tabs.infoWidget
    proc_time()
    wind.stack.setCurrentWidget(infotab)
    button = infotab.selectButton
    Obj.value = [outfile]
    infoTab.browse_torrent = mock_func
    button.selectTorrent()
    name = torrent.meta["info"]["name"]
    assert infotab.nameEdit.text() == name
    rmpath(outfile)


def test_info_accept_method(wind, ttorrent):
    """Test drag enter event on info widget."""
    info = wind.tabs.infoWidget
    wind.stack.setCurrentWidget(info)
    proc_time()
    event = MockEvent(ttorrent)
    assert info.dragEnterEvent(event)
    event = MockEvent(None)
    assert not info.dragEnterEvent(event)


def test_info_move_event(wind, ttorrent):
    """Test move event on info widget."""
    info = wind.tabs.infoWidget
    wind.stack.setCurrentWidget(info)
    proc_time()
    event = MockEvent(ttorrent)
    assert info.dragMoveEvent(event)
    event = MockEvent(None)
    assert not info.dragMoveEvent(event)


def test_info_drop_event(wind, ttorrent):
    """Test drop event on editor widget."""
    info = wind.tabs.infoWidget
    wind.stack.setCurrentWidget(info)
    proc_time()
    event = MockEvent(ttorrent)
    assert info.dropEvent(event)


def test_info_drop_false(wind):
    """Test drop event on editor widget is false."""
    info = wind.tabs.infoWidget
    wind.stack.setCurrentWidget(info)
    proc_time()
    event = MockEvent(None)
    assert not info.dropEvent(event)
