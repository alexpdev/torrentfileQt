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

from tests import dir1, dir2, proc_time, rmpath, tempfile, ttorrent, wind
from torrentfileQt import checkTab
from torrentfileQt.checkTab import ProgressBar, TreePieceItem, TreeWidget


class Obj:
    value = None


def mock_func(_):
    return Obj.value


def test_fixture():
    """Test Fixtures."""
    assert dir1 and dir2 and ttorrent and wind


def test_missing_files_check(dir2, ttorrent, wind):
    """Test missing files checker proceduire."""
    checktab = wind.tabs.checkWidget
    wind.stack.setCurrentWidget(checktab)
    dirpath = Path(dir2)
    for item in dirpath.iterdir():
        if item.is_file():
            os.remove(item)
    checktab.file_group.setPath(ttorrent)
    checktab.content_group.setPath(dir2)
    checktab.checkButton.click()
    proc_time()
    assert checktab.treeWidget.topLevelItemCount() > 0


def test_shorter_files_check(wind, ttorrent, dir2):
    """Test missing files checker proceduire."""
    checktab = wind.tabs.checkWidget
    dirpath = Path(dir2)
    wind.stack.setCurrentWidget(checktab)

    def shortenfile(item):
        """Shave some data off the end of file."""
        temp = bytearray(2**19)
        with open(item, "rb") as fd:
            fd.readinto(temp)
        with open(item, "wb") as fd:
            fd.write(temp)

    if os.path.exists(dirpath):
        for item in dirpath.iterdir():
            if item.is_file():
                shortenfile(item)
    checktab.file_group.setPath(ttorrent)
    checktab.content_group.setPath(dir2)
    checktab.checkButton.click()
    proc_time()
    assert checktab.treeWidget.topLevelItemCount() > 0


def test_check_tab(wind, ttorrent, dir1):
    """Test checker procedure."""
    checktab = wind.tabs.checkWidget
    wind.stack.setCurrentWidget(checktab)
    checktab.file_group.setPath(ttorrent)
    checktab.content_group.setPath(dir1)
    checktab.checkButton.click()
    proc_time()
    assert checktab.textEdit.toPlainText() != ""


def test_check_tab_input1(wind, dir1):
    """Test checker procedure."""
    checktab = wind.tabs.checkWidget
    wind.stack.setCurrentWidget(checktab)
    Obj.value = dir1
    checkTab.browse_folder = mock_func
    checktab.content_folders.click()
    assert checktab.content_group.getPath() != ""


def test_check_tab_input_2(wind, dir1):
    """Test checker procedure."""
    checktab = wind.tabs.checkWidget
    wind.stack.setCurrentWidget(checktab)
    Obj.value = dir1
    checkTab.browse_folder = mock_func
    checktab.file_button.click()
    assert checktab.file_group.getLabelText() != ""


def test_check_tab4(wind):
    """Test checker procedure again."""
    checktab = wind.tabs.checkWidget
    wind.stack.setCurrentWidget(checktab)
    tree_widget = checktab.treeWidget
    assert tree_widget.invisibleRootItem() is not None


def test_clear_logtext(wind):
    """Test checker logTextEdit widget function."""
    checktab = wind.tabs.checkWidget
    wind.stack.setCurrentWidget(checktab)
    text_edit = checktab.textEdit
    text_edit.insertPlainText("sometext")
    text_edit.clear_data()
    assert text_edit.toPlainText() == ""


def test_checktab_tree(wind):
    """Check tree item counting functionality."""
    checktab = wind.tabs.checkWidget
    wind.stack.setCurrentWidget(checktab)
    tree = TreeWidget(parent=checktab)
    item = TreePieceItem(type=0, tree=tree)
    item.progbar = ProgressBar(parent=tree, size=1000000)
    item.count(100000000)
    assert item.counted == 1000000


@pytest.mark.parametrize("size", list(range(18, 20)))
@pytest.mark.parametrize("index", list(range(1, 7, 2)))
@pytest.mark.parametrize("version", [1, 2, 3])
@pytest.mark.parametrize("ext", [".mkv", ".rar", ".r00", ".mp3"])
def test_singlefile(size, ext, index, version, wind):
    """Test the singlefile for create and check tabs."""
    createtab = wind.tabs.createWidget
    checktab = wind.tabs.checkWidget
    wind.stack.setCurrentWidget(createtab)
    testfile = str(tempfile(exp=size))
    tfile = testfile + ext
    os.rename(testfile, tfile)
    metafile = tfile + ".torrent"
    createtab.path_group.setPath(tfile)
    createtab.output_path_edit.setText(metafile)
    createtab.piece_length_combo.setCurrentIndex(index)
    proc_time()
    btns = [createtab.v1button, createtab.v2button, createtab.hybridbutton]
    for i, btn in enumerate(btns):
        if i + 1 == version:
            btn.click()
            break
    createtab.submit_button.click()
    while proc_time(0.3):
        if wind.statusBar().currentMessage() != "Processing":
            break
    wind.stack.setCurrentWidget(checktab)
    checktab.file_group.setPath(metafile)
    checktab.content_group.setPath(tfile)
    checktab.checkButton.click()
    proc_time()
    widges = checktab.treeWidget.itemWidgets
    assert all(i.total == i.value for i in widges.values())
    rmpath(tfile, metafile)


@pytest.mark.parametrize("version", [1, 2, 3])
def test_singlefile_large(version, wind):
    """Test the singlefile with large size for create and check tabs."""
    createtab = wind.tabs.createWidget
    checktab = wind.tabs.checkWidget
    wind.stack.setCurrentWidget(checktab)
    testfile = str(tempfile(exp=28))
    tfile = testfile + ".dat"
    os.rename(testfile, tfile)
    metafile = tfile + ".torrent"
    createtab.path_group.setPath(tfile)
    createtab.output_path_edit.setText(metafile)
    btns = [createtab.v1button, createtab.v2button, createtab.hybridbutton]
    for i, btn in enumerate(btns):
        if i + 1 == version:
            btn.click()
            break
    createtab.submit_button.click()
    while proc_time(0.3):
        if wind.statusBar().currentMessage() != "Processing":
            break
    checktab.file_group.setPath(metafile)
    checktab.content_group.setPath(tfile)
    checktab.checkButton.click()
    widges = checktab.treeWidget.itemWidgets
    proc_time(0.3)
    assert all(i.total == i.value for i in widges.values())
    rmpath(tfile, metafile)
