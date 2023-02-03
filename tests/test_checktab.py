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

from tests import wind, tempdir, torrent_versions, switchTab, waitfor, temp_file
from torrentfileQt import checkTab
from torrentfileQt.checkTab import TreeWidget

class Obj:
    value = None

def mock_func(_):
    return Obj.value

checkTab.browse_files = mock_func
checkTab.browse_folder = mock_func
checkTab.browse_torrent = mock_func

@pytest.fixture(params=torrent_versions())
def dir2(request):
    dirname = tempdir(6, 2, 27, [".rar", ".mp3", ".mkv", ".dat"])
    maker = request.param
    torrent = maker(
        path=dirname,
        piece_length=18,
        outfile=dirname + ".torrent",
        announce=["url1", "url2"]
    )
    torrent.write()
    return dirname, dirname + ".torrent"


# def test_missing_files_check(dir2, wind):
#     """Test missing files checker proceduire."""
#     dirname, torrent = dir2
#     checktab = wind.tabs.checkWidget
#     switchTab(wind.stack, checktab)
#     dirpath = Path(dirname)
#     for item in dirpath.iterdir():
#         if item.is_file():
#             os.remove(item)
#     checktab.file_group.setPath(torrent)
#     checktab.content_group.setPath(dirname)
#     checktab.checkButton.click()
#     func = lambda: checktab.treeWidget.topLevelItemCount() >= 0
#     assert waitfor(3, func)

# def test_shorter_files_check(wind, dir2):
#     """Test missing files checker proceduire."""
#     checktab = wind.tabs.checkWidget
#     dirname, torrent = dir2
#     dirpath = Path(dirname)
#     switchTab(wind.stack, checktab)

#     def shortenfile(item):
#         """Shave some data off the end of file."""
#         temp = bytearray(2**19)
#         with open(item, "rb") as fd:
#             fd.readinto(temp)
#         with open(item, "wb") as fd:
#             fd.write(temp)

#     if os.path.exists(dirpath):
#         for item in dirpath.iterdir():
#             if item.is_file():
#                 shortenfile(item)
#     checktab.file_group.setPath(torrent)
#     checktab.content_group.setPath(dirname)
#     checktab.checkButton.click()
#     func = lambda: checktab.treeWidget.topLevelItemCount() >= 0
#     assert waitfor(3, func)

# def test_check_tab(wind, dir2):
#     """Test checker procedure."""
#     checktab = wind.tabs.checkWidget
#     dirname, torrent = dir2
#     switchTab(wind.stack, checktab)
#     checktab.file_group.setPath(torrent)
#     checktab.content_group.setPath(dirname)
#     checktab.checkButton.click()
#     func = lambda: checktab.textEdit.toPlainText() != ""
#     assert waitfor(3, func)

# def test_check_tab_input1(wind, dir2):
#     """Test checker procedure."""
#     checktab = wind.tabs.checkWidget
#     dirname, torrent = dir2
#     switchTab(wind.stack, checktab)
#     Obj.value = dirname
#     checktab.content_folders.click()
#     func = lambda: checktab.content_group.getPath() != ""
    # assert waitfor(3, func)

# def test_check_tab_input_2(wind, dir2):
#     """Test checker procedure."""
#     checktab = wind.tabs.checkWidget
#     dirname, torrent = dir2
#     switchTab(wind.stack, checktab)
#     Obj.value = dirname
#     checktab.file_button.click()
#     assert checktab.file_group.getLabelText() != ""

# def test_check_tab4(wind):
#     """Test checker procedure again."""
#     checktab = wind.tabs.checkWidget
#     switchTab(wind.stack, checktab)
#     tree_widget = checktab.treeWidget
#     assert tree_widget.invisibleRootItem() is not None

# def test_clear_logtext(wind):
#     """Test checker logTextEdit widget function."""
#     checktab = wind.tabs.checkWidget
#     switchTab(wind.stack, checktab)
#     text_edit = checktab.textEdit
#     text_edit.insertPlainText("sometext")
#     text_edit.clear_data()
#     assert text_edit.toPlainText() == ""
