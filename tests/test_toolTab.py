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

import pytest

from tests import switchTab, temp_file, tempdir, torrent_versions, wind
from torrentfileQt import toolTab


class MockReturn:
    """Mock class for tests."""

    value = None


def mock_func(_):
    """Mock function for tests."""
    assert wind
    return MockReturn.value


toolTab.browse_torrent = mock_func
toolTab.browse_folder = mock_func
toolTab.browse_files = mock_func


@pytest.fixture(scope="module")
def tempfolder():
    """Test fixture for unit test suite."""
    folder = tempdir(6, 2, 27, [".r00", ".mp3", ".mkv", ".dat", ".zip"])
    return folder


@pytest.fixture(params=torrent_versions(), scope="module")
def temptor(tempfolder, request):
    """Test fixture for unit test suite."""
    maker = request.param
    torrent = maker(
        path=tempfolder,
        piece_length=22,
        outfile=tempfolder + ".torrent",
        announce=["url1"],
    )
    torrent.write()
    return tempfolder + ".torrent"


def test_magnet_buttons(wind, temptor):
    """Test tool tab magnet maker."""
    tab = wind.tabs.toolWidget
    switchTab(wind.stack, tab)
    magnetgroup = tab.magnetgroup
    MockReturn.value = temptor
    magnetgroup.metafilebutton.click()
    assert magnetgroup.pathEdit.text() == temptor
    magnetgroup.submit_button.click()
    assert magnetgroup.magnetEdit.text()


def test_magnet_button_dir(wind, tempfolder):
    """Test tool tab magnet maker."""
    tab = wind.tabs.toolWidget
    switchTab(wind.stack, tab)
    widget = tab.piece_length_calculator
    MockReturn.value = tempfolder
    widget.fileButton.click()
    assert widget.path_line.text() == tempfolder
    widget.folderButton.click()
    assert widget.path_line.text() == tempfolder
    widget.piece_length_combo.setCurrentIndex(1)


def test_magnet_button_file(wind):
    """Test tool tab magnet maker."""
    tfile = temp_file(20)
    tab = wind.tabs.toolWidget
    switchTab(wind.stack, tab)
    widget = tab.piece_length_calculator
    MockReturn.value = tfile
    widget.fileButton.click()
    assert widget.path_line.text() == tfile
    widget.folderButton.click()
    assert widget.path_line.text() == tfile
    widget.piece_length_combo.setCurrentIndex(1)
