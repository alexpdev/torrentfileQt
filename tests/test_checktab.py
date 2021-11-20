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

from tests.context import Temp, build, fillfile, mktorrent, pathstruct, rmpath
from torrentfileQt.checkTab import ProgressBar, TreePieceItem, TreeWidget


@pytest.mark.parametrize("struct", pathstruct())
@pytest.mark.parametrize("hasher", Temp.hashers)
def test_missing_files_check(hasher, struct):
    """Test missing files checker proceduire."""
    contents = build(struct)
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
    rmpath(path)


@pytest.mark.parametrize("struct", pathstruct())
def test_check_tab_input_2(struct):
    """Test checker procedure."""
    path = build(struct)
    checktab = Temp.window.central.checkWidget
    Temp.window.central.setCurrentWidget(checktab)
    checktab.browseButton1.browse(path)
    assert checktab.fileInput.text() != ""  # nosec
    rmpath(path)


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


@pytest.mark.parametrize("size", list(range(16, 23)))
@pytest.mark.parametrize("index", list(range(1, 7)))
@pytest.mark.parametrize("ext", [".mkv", ".mp4", ".rar", ".zip"])
def test_singlefile(size, ext, index):
    """Test the singlefile for create and check tabs."""
    createtab = Temp.window.central.createWidget
    checktab = Temp.window.central.checkWidget
    Temp.window.central.setCurrentWidget(checktab)
    path = os.path.join(Temp.root, "file" + Temp.stamp() + ext)
    fillfile(path, size=size)
    createtab.path_input.clear()
    createtab.output_input.clear()
    createtab.browse_file_button.browse(path)
    # createtab.path_input.setText(path)
    createtab.output_input.setText(path + ".torrent")
    createtab.piece_length.setCurrentIndex(index)
    createtab.submit_button.click()
    checktab.fileInput.clear()
    checktab.searchInput.clear()
    checktab.fileInput.setText(path + ".torrent")
    checktab.searchInput.setText(path)
    checktab.checkButton.click()
    assert "100%" in checktab.textEdit.toPlainText()  # nosec
    rmpath([path, path + ".torrent"])
