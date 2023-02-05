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
"""Module for testing procedures on Check Tab."""

import pytest

from tests import switchTab, tempdir, torrent_versions, wind
from torrentfileQt import checkTab


class MockReturn:
    """Mock class for testing."""

    value = None


def mock_func(_):
    """Mock function for testing."""
    assert wind
    return MockReturn.value


checkTab.browse_files = mock_func
checkTab.browse_folder = mock_func
checkTab.browse_torrent = mock_func


@pytest.fixture(scope="module")
def tdir():
    """Test fixture for unit test suite."""
    dirname = tempdir(6, 2, 27, [".r00", ".mp3", ".mkv", ".dat", ".zip"])
    return dirname


@pytest.fixture(params=torrent_versions(), scope="module")
def ttorrent(tdir, request):
    """Test fixture for unit test suite."""
    maker = request.param
    torrent = maker(
        path=tdir,
        piece_length=18,
        outfile=tdir + ".torrent",
        announce=["url1", "url2"],
    )
    torrent.write()
    return tdir, tdir + ".torrent"


def test_check_tab_setPath(tdir, wind):
    """Test function for check tab."""
    tab = wind.tabs.checkWidget
    switchTab(wind.stack, tab)
    tab.setPath(tdir)
    assert tab.content_group.getPath() == tdir


def test_checktab_setTorrent(ttorrent, wind):
    """Test function for check tab."""
    _, torrent = ttorrent
    tab = wind.tabs.checkWidget
    switchTab(wind.stack, tab)
    tab.setTorrent(torrent)
    assert tab.file_group.getPath() == torrent


def test_checktab_browse_torrent(ttorrent, wind):
    """Test function for check tab."""
    _, torrent = ttorrent
    tab = wind.tabs.checkWidget
    switchTab(wind.stack, tab)
    MockReturn.value = torrent
    tab.file_button.click()
    assert tab.file_group.getPath() == torrent


def test_checktab_browse_folder(tdir, wind):
    """Test function for check tab."""
    tab = wind.tabs.checkWidget
    switchTab(wind.stack, tab)
    MockReturn.value = tdir
    tab.content_folders.click()
    assert tab.content_group.getPath() == tdir


def test_checktab_browse_files(tdir, wind):
    """Test function for check tab."""
    tab = wind.tabs.checkWidget
    switchTab(wind.stack, tab)
    MockReturn.value = tdir
    tab.content_files.click()
    assert tab.content_group.getPath() == tdir


def test_checktab_thread(ttorrent, wind):
    """Test function for check tab."""
    tdir, torrent = ttorrent
    tab = wind.tabs.checkWidget
    switchTab(wind.stack, tab)
    checkTab.RecheckThread.start = checkTab.RecheckThread.run
    tab.content_group.setPath(tdir)
    tab.populate_tree(torrent, tdir)
    assert tab.treeWidget.rootitem.childCount() > 0
    tab.treeWidget.clear()


def test_checktab_submit(ttorrent, wind):
    """Test function for check tab."""
    tdir, torrent = ttorrent
    tab = wind.tabs.checkWidget
    switchTab(wind.stack, tab)
    checkTab.RecheckThread.start = checkTab.RecheckThread.run
    tab.setPath(tdir)
    tab.setTorrent(torrent)
    tab.checkButton.click()
    assert tab.treeWidget.rootitem.childCount() > 0
    tab.treeWidget.clear()
    tab.textEdit.clear_data()
