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

import pyben
import pytest

from tests import dir1, dir2, ttorrent, wind


def test_fixtures():
    """Test fixtures."""
    assert dir1 and dir2 and ttorrent and wind


@pytest.mark.parametrize("field", ["announce", "name", "private", "comment"])
def test_editor_torrent_loading(field, wind, ttorrent):
    """Testing editor widget functionality."""
    window, app = wind
    editor = window.central.editorWidget
    editor.window.central.setCurrentWidget(editor)
    editor.fileButton.browse(ttorrent)
    app.processEvents()
    fields = []
    for i in range(editor.table.rowCount()):
        fields.append(editor.table.item(i, 0).text())
    assert field in fields


def test_editor_torrent_saving(wind, ttorrent):
    """Testing editor widget saving functionality."""
    window, app = wind
    editor = window.central.editorWidget
    editor.window.central.setCurrentWidget(editor)
    app.processEvents()
    editor.fileButton.browse(ttorrent)
    for i in range(editor.table.rowCount()):
        item1 = editor.table.item(i, 0)
        item2 = editor.table.item(i, 1)
        if item1.text() == "announce":
            item2.setText("other")
            break
    app.processEvents()
    editor.button.click()
    meta = pyben.load(ttorrent)
    assert meta["announce"] == "other"
