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

from tests import dir1, dir2, ttorrent, wind, MockEvent


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


def test_editor_accept_method(wind, ttorrent):
    """Test drag enter event on editor widget."""
    window, app = wind
    editor = window.central.editorWidget
    editor.window.central.setCurrentWidget(editor)
    app.processEvents()
    event = MockEvent(ttorrent)
    assert editor.dragEnterEvent(event)
    assert editor.data == event.mimeData().data('text/plain')


def test_editor_drop_event(wind, ttorrent):
    """Test drop event on editor widget."""
    window, app = wind
    editor = window.central.editorWidget
    editor.window.central.setCurrentWidget(editor)
    app.processEvents()
    event = MockEvent(ttorrent)
    amount = len("file:///")
    assert editor.dropEvent(event)
    assert editor.line.text() == event.mimeData().text()[amount:]


def test_editor_table_fields(wind, ttorrent):
    """Test the edit fields of table widget."""
    window, app = wind
    editor = window.central.editorWidget
    editor.window.central.setCurrentWidget(editor)
    app.processEvents()
    table = editor.table
    editor.line.setText(ttorrent)
    table.handleTorrent.emit(ttorrent)
    found = 0
    for i in range(table.rowCount()):
        if table.item(i, 0):
            if table.item(i, 0).text() in ["httpseeds", "url-list", "announce-list"]:
                found += 1
                widget = table.cellWidget(i, 1)
                widget.add_button.click()
                widget.line_edit.setText("url1")
                widget.add_button.click()
                widget.line_edit.setText("url2")
                widget.combo.focusOutEvent(None)
                lst = [widget.combo.itemText(j) for j in range(widget.combo.count())]
                assert "url1" in lst
                assert "url2" in lst
                for _ in range(widget.combo.count()):
                    widget.remove_button.click()
                assert widget.combo.count() == 0
    assert found == 3
