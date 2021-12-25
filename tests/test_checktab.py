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

from tests import dir1, dir2, rmpath, tempfile, ttorrent, wind
from torrentfileQt.checkTab import ProgressBar, TreePieceItem, TreeWidget


def test_fixture():
    """Test Fixtures."""
    assert dir1 and dir2 and ttorrent and wind


def test_missing_files_check(dir2, ttorrent, wind):
    """Test missing files checker proceduire."""
    window, _ = wind
    checktab = window.central.checkWidget
    window.central.setCurrentWidget(checktab)
    dirpath = Path(dir2)
    for item in dirpath.iterdir():
        if item.is_file():
            os.remove(item)
    checktab.fileInput.setText(ttorrent)
    checktab.searchInput.setText(dir2)
    checktab.checkButton.click()
    assert checktab.treeWidget.topLevelItemCount() > 0


def test_shorter_files_check(wind, ttorrent, dir2):
    """Test missing files checker proceduire."""
    window, _ = wind
    checktab = window.central.checkWidget
    dirpath = Path(dir2)
    window.central.setCurrentWidget(checktab)

    def shortenfile(item):
        """Shave some data off the end of file."""
        temp = bytearray(2 ** 19)
        with open(item, "rb") as fd:
            fd.readinto(temp)
        with open(item, "wb") as fd:
            fd.write(temp)

    if os.path.exists(dirpath):
        for item in dirpath.iterdir():
            if item.is_file():
                shortenfile(item)
    checktab.fileInput.setText(ttorrent)
    checktab.searchInput.setText(dir2)
    checktab.checkButton.click()
    assert checktab.treeWidget.topLevelItemCount() > 0


def test_check_tab(wind, ttorrent, dir1):
    """Test checker procedure."""
    window, _ = wind
    checktab = window.central.checkWidget
    window.central.setCurrentWidget(checktab)
    checktab.fileInput.setText(ttorrent)
    checktab.searchInput.setText(dir1)
    checktab.checkButton.click()
    assert checktab.textEdit.toPlainText() != ""


def test_check_tab_input1(wind, dir1):
    """Test checker procedure."""
    window, _ = wind
    checktab = window.central.checkWidget
    window.central.setCurrentWidget(checktab)
    checktab.browseButton2.browse(dir1)
    assert checktab.searchInput.text() != ""


def test_check_tab_input_2(wind, dir1):
    """Test checker procedure."""
    window, _ = wind
    checktab = window.central.checkWidget
    window.central.setCurrentWidget(checktab)
    checktab.browseButton1.browse(dir1)
    assert checktab.fileInput.text() != ""


def test_check_tab4(wind):
    """Test checker procedure again."""
    window, _ = wind
    checktab = window.central.checkWidget
    window.central.setCurrentWidget(checktab)
    tree_widget = checktab.treeWidget
    assert tree_widget.invisibleRootItem() is not None


def test_clear_logtext(wind):
    """Test checker logTextEdit widget function."""
    window, _ = wind
    checktab = window.central.checkWidget
    window.central.setCurrentWidget(checktab)
    text_edit = checktab.textEdit
    text_edit.insertPlainText("sometext")
    text_edit.clear_data()
    assert text_edit.toPlainText() == ""


def test_checktab_tree(wind):
    """Check tree item counting functionality."""
    window, _ = wind
    checktab = window.central.checkWidget
    window.central.setCurrentWidget(checktab)
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
    window, _ = wind
    createtab = window.central.createWidget
    checktab = window.central.checkWidget
    window.central.setCurrentWidget(checktab)
    testfile = str(tempfile(exp=size))
    tfile = testfile + ext
    os.rename(testfile, tfile)
    metafile = tfile + ".torrent"
    createtab.path_input.clear()
    createtab.output_input.clear()
    createtab.browse_file_button.browse(tfile)
    createtab.output_input.setText(metafile)
    createtab.piece_length.setCurrentIndex(index)
    btns = [createtab.v1button, createtab.v2button, createtab.hybridbutton]
    for i, btn in enumerate(btns):
        if i + 1 == version:
            btn.click()
            break
    createtab.submit_button.click()
    createtab.submit_button.join()
    checktab.fileInput.clear()
    checktab.searchInput.clear()
    checktab.fileInput.setText(metafile)
    checktab.searchInput.setText(tfile)
    checktab.checkButton.click()
    ptext = checktab.textEdit.toPlainText()
    assert "100%" in ptext
    rmpath(tfile, metafile)
