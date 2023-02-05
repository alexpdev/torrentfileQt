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
"""Module for testing procedures on Bencode editor module."""

import pyben
import pytest

from tests import (MockEvent, switchTab, temp_file, tempdir, torrent_versions,
                   wind)
from torrentfileQt import infoTab


class MockReturn:
    """Mock class for tests."""

    value = None


def mock_func(_):
    """Mock function for tests."""
    assert wind
    return MockReturn.value


infoTab.browse_torrent = mock_func


@pytest.fixture(params=torrent_versions())
def torrent_file(request):
    """Test fixture for tesing info widget."""
    size = 29
    file_path = temp_file(size)
    maker = request.param
    outfile = file_path + ".torrent"
    torrent = maker(
        path=file_path,
        announce=["urla", "urlb"],
        source="some source string",
        piece_length=19,
        outfile=outfile,
    )
    torrent.write()
    return outfile


@pytest.fixture(params=torrent_versions())
def torrent_file1(request):
    """Test fixture for testing info widget."""
    size = 29
    tdir = tempdir(8, 3, size, [".mkv", ".rar", ".r00", ".wav", ".log"])
    maker = request.param
    outfile = tdir + ".torrent"
    torrent = maker(
        path=tdir,
        private=True,
        announce=["url1"],
        comment="this is a comment",
        piece_length=2**19,
        outfile=outfile,
    )
    torrent.write()
    meta = pyben.load(outfile)
    del meta["creation date"]
    del meta["announce-list"]
    del meta["created by"]
    pyben.dump(meta, outfile)
    return outfile


def test_info_select_button(wind, torrent_file):
    """Test function for testing infor widget."""
    widget = wind.tabs.infoWidget
    switchTab(wind.stack, widget=widget)
    MockReturn.value = torrent_file
    widget.selectButton.click()
    assert len(widget.pathEdit.text()) > 0
    assert not widget.clear()


def test_info_select_with_dir(wind, torrent_file1):
    """Test function for testing infor widget."""
    widget = wind.tabs.infoWidget
    switchTab(wind.stack, widget=widget)
    MockReturn.value = torrent_file1
    widget.selectButton.click()
    assert len(widget.pathEdit.text()) > 0
    assert not widget.clear()


def test_info_drag_enter_event(wind, torrent_file):
    """Test function for testing infor widget."""
    widget = wind.tabs.infoWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(torrent_file)
    assert widget.dragEnterEvent(event)


def test_info_drag_enter_no_event(wind):
    """Test function for testing infor widget."""
    widget = wind.tabs.infoWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(None)
    assert not widget.dragEnterEvent(event)


def test_info_drag_move_event(wind, torrent_file):
    """Test function for testing infor widget."""
    widget = wind.tabs.infoWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(torrent_file)
    assert widget.dragMoveEvent(event)


def test_info_drag_move_no_event(wind):
    """Test function for testing infor widget."""
    widget = wind.tabs.infoWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(None)
    assert not widget.dragMoveEvent(event)


def test_info_drop_event(wind, torrent_file):
    """Test function for testing infor widget."""
    widget = wind.tabs.infoWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(torrent_file)
    assert widget.dropEvent(event)


def test_info_drop_no_event(wind):
    """Test function for testing infor widget."""
    widget = wind.tabs.infoWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(None)
    assert not widget.dropEvent(event)
