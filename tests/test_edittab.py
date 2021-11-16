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

from tests.context import Temp, build, mktorrent, pathstruct, rmpath


@pytest.mark.parametrize("field", ["announce", "name", "private", "comment"])
@pytest.mark.parametrize("size", list(range(16, 21)))
@pytest.mark.parametrize("struct", pathstruct())
@pytest.mark.parametrize("hasher", Temp.hashers)
def test_editor_torrent_loading(struct, hasher, size, field):
    """Testing editor widget functionality."""
    editor = Temp.window.central.editorWidget
    Temp.window.central.setCurrentWidget(editor)
    path = build(struct, size=size)
    editor.window.central.setCurrentWidget(editor)
    torrent = mktorrent(path, hasher=hasher)
    editor.fileButton.browse(torrent)
    fields = []
    for i in range(editor.table.rowCount()):
        fields.append(editor.table.item(i, 0).text())
    assert field in fields  # nosec
    rmpath(path)
    rmpath(torrent)


@pytest.mark.parametrize("size", list(range(16, 21)))
@pytest.mark.parametrize("struct", pathstruct())
@pytest.mark.parametrize("hasher", Temp.hashers)
def test_editor_torrent_saving(struct, hasher, size):
    """Testing editor widget saving functionality."""
    editor = Temp.window.central.editorWidget
    Temp.window.central.setCurrentWidget(editor)
    Temp.app.processEvents()
    path = build(struct, size=size)
    editor.window.central.setCurrentWidget(editor)
    torrent = mktorrent(path, hasher=hasher)
    editor.fileButton.browse(torrent)
    print(editor.table.rowCount())
    for i in range(editor.table.rowCount()):
        item1 = editor.table.item(i, 0)
        item2 = editor.table.item(i, 1)
        if item1.text() == "announce":
            item2.setText("other")
            break
    Temp.app.processEvents()
    editor.button.click()
    meta = pyben.load(torrent)
    assert meta["announce"] == "other"   # nosec
    rmpath(path)
    rmpath(torrent)
