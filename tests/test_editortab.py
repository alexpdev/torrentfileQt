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

from tests import switchTab, temp_file, torrent_versions, wind
from torrentfileQt import editorTab


class MockReturn:
    """Mock class for testing."""

    value = None


def mock_func(_):
    """Mock function for testing."""
    assert wind
    return MockReturn.value


editorTab.browse_torrent = mock_func


@pytest.fixture(params=torrent_versions(), scope="module")
def torent(request):
    """Test fixture for editor widget."""
    maker = request.param
    tempfile = temp_file(25)
    torrent = maker(
        path=tempfile,
        piece_length=18,
        private=True,
        source="source",
        comment="comment",
        outfile=tempfile + ".torrent",
        announce=["url1", "url2", "url8"],
        web_seeds=["url4", "url5", "url6"],
    )
    torrent.write()
    return tempfile + ".torrent"


def test_editor_file_button(wind, torent):
    """Test function for editor tab functions."""
    tab = wind.tabs.editorWidget
    switchTab(wind.stack, tab)
    MockReturn.value = torent
    tab.fileButton.click()
    assert tab.table.rowCount() > 0


def test_editor_save_button(wind, torent):
    """Test function for editor tab functions."""
    tab = wind.tabs.editorWidget
    switchTab(wind.stack, tab)
    MockReturn.value = torent
    tab.fileButton.click()
    tab.save_button.click()
    assert tab.table.rowCount() > 0


def test_editor_table(wind, torent):
    """Test function for editor tab functions."""
    tab = wind.tabs.editorWidget
    switchTab(wind.stack, tab)
    tab.editTorrent(torent)
    table = tab.table
    for i in range(tab.table.rowCount()):
        label = table.item(i, 0)
        if label.text() in ["announce list", "url list", "httpseeds"]:
            box = table.cellWidget(i, 1)
            box.line_edit.setText("url3")
            box.add_button.click()
            for i in range(box.combo.count()):
                box.combo.setCurrentIndex(i)
                box.remove_button.click()
                break
            break
    tab.save_button.click()
