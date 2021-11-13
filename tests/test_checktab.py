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

import os
from pathlib import Path

import pytest

from tests.context import Temp, build, mktorrent, pathstruct, rmpath
from torrentfileQt.checkTab import ProgressBar, TreePieceItem, TreeWidget


@pytest.mark.parametrize("struct", pathstruct())
@pytest.mark.parametrize("hasher", Temp.hashers)
def test_missing_files_check(hasher, struct):
    """Test missing files checker proceduire."""
    contents = build(struct)
    print("NEW FUNCTION \n\n\n\n\n\n\n\n\n\n\n\n")
    print(struct, hasher)
    metafile = mktorrent(contents, hasher)
    checktab = Temp.window.central.checkWidget
    Temp.window.central.setCurrentWidget(checktab)
    dir1 = Path(contents) / "dir1"
    if os.path.exists(dir1):
        for item in dir1.iterdir():
            if item.is_file():
                os.remove(item)
        checktab.fileInput.setText(metafile)
        checktab.searchInput.setText(contents)
        checktab.checkButton.click()
        assert checktab.treeWidget.topLevelItemCount() > 0  # nosec
        rmpath([metafile, contents])


@pytest.mark.parametrize("struct", pathstruct())
@pytest.mark.parametrize("hasher", Temp.hashers)
def test_shorter_files_check(hasher, struct):
    """Test missing files checker proceduire."""
    contents = build(struct)
    metafile = mktorrent(contents, hasher)
    checktab = Temp.window.central.checkWidget
    Temp.window.central.setCurrentWidget(checktab)
    dir1 = Path(contents) / "dir1"

    def shortenfile(item):
        """Shave some data off the end of file."""
        temp = bytearray(2 ** 19)
        with open(item, "rb") as fd:
            fd.readinto(temp)
        with open(item, "wb") as fd:
            fd.write(temp)

    if os.path.exists(dir1):
        for item in dir1.iterdir():
            if item.is_file():
                shortenfile(item)
    elif len(os.listdir(contents)) == 1:
        full = os.path.join(contents, os.listdir(contents)[0])
        shortenfile(full)
    checktab.fileInput.setText(metafile)
    checktab.searchInput.setText(contents)
    checktab.checkButton.click()
    assert checktab.treeWidget.topLevelItemCount() > 0  # nosec
    rmpath([metafile, contents])


@pytest.mark.parametrize("struct", pathstruct())
@pytest.mark.parametrize("hasher", Temp.hashers)
def test_check_tab(hasher, struct):
    """Test checker procedure."""
    path = build(struct)
    checktab = Temp.window.central.checkWidget
    Temp.window.central.setCurrentWidget(checktab)
    args = {"path": path}
    torrent = hasher(**args)
    metafile, _ = torrent.write()
    contents = path
    checktab.fileInput.setText(metafile)
    checktab.searchInput.setText(contents)
    checktab.checkButton.click()
    assert checktab.textEdit.toPlainText() != ""  # nosec
    rmpath([path, metafile])


@pytest.mark.parametrize("struct", pathstruct())
def test_check_tab_input1(struct):
    """Test checker procedure."""
    path = build(struct)
    checktab = Temp.window.central.checkWidget
    Temp.window.central.setCurrentWidget(checktab)
    checktab.browseButton2.browse(path)
    assert checktab.searchInput.text() != ""  # nosec


@pytest.mark.parametrize("struct", pathstruct())
def test_check_tab_input_2(struct):
    """Test checker procedure."""
    path = build(struct)
    checktab = Temp.window.central.checkWidget
    Temp.window.central.setCurrentWidget(checktab)
    checktab.browseButton1.browse(path)
    assert checktab.fileInput.text() != ""  # nosec


def test_check_tab4():
    """Test checker procedure again."""
    checktab = Temp.window.central.checkWidget
    Temp.window.central.setCurrentWidget(checktab)
    tree_widget = checktab.treeWidget
    assert tree_widget.invisibleRootItem() is not None  # nosec


def test_clear_logtext():
    """Test checker logTextEdit widget function."""
    checktab = Temp.window.central.checkWidget
    Temp.window.central.setCurrentWidget(checktab)
    text_edit = checktab.textEdit
    text_edit.insertPlainText("sometext")
    text_edit.clear_data()
    assert text_edit.toPlainText() == ""  # nosec


def test_checktab_tree():
    """Check tree item counting functionality."""
    checktab = Temp.window.central.checkWidget
    Temp.window.central.setCurrentWidget(checktab)
    tree = TreeWidget(parent=checktab)
    item = TreePieceItem(type=0, tree=tree)
    item.progbar = ProgressBar(parent=tree, size=1000000)
    item.count(100000000)
    assert item.counted == 1000000  # nosec
