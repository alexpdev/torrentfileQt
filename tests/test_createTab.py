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

import pyben
import pytest
from torrentfile.torrent import TorrentFileHybrid

from tests import dir1, dir2, proc_time, rmpath, tempfile, wind
from torrentfileQt import createTab
from torrentfileQt.createTab import TorrentFileCreator


class Obj:
    value = None


def mock_func(_):
    return Obj.value


def test_rmpath():
    """Test the rmpath function."""
    fake = "./ajdiednvikjdod"
    rmpath(fake)
    assert not os.path.exists(fake)


def test_fixtures():
    """Test fixtures."""
    assert dir1 and dir2 and tempfile and wind


def test_create_with_hasher1(dir2, wind):
    """Test the radio buttons on create tab v1 hasher."""
    metafile = dir2 + ".torrent"
    creator = wind.tabs.createWidget
    wind.stack.setCurrentWidget(creator)
    creator.path_group.setPath(dir2)
    creator.web_seed_input.setPlainText("url1")
    creator.output_path_edit.setText(metafile)
    proc_time()
    creator.v1button.setChecked(True)
    creator.piece_length_combo.setCurrentIndex(2)
    creator.submit_button.click()
    while proc_time(0.4):
        if wind.statusBar().currentMessage() != "Processing":
            break
    assert os.path.exists(metafile)
    rmpath(metafile)


def test_create_tab_browse(dir2, wind):
    """Test Info tab select1."""
    path = dir2
    createtab = wind.tabs.createWidget
    wind.stack.setCurrentWidget(createtab)
    proc_time()
    button = createtab.path_file_button
    Obj.value = dir2
    createTab.browse_files = mock_func
    button.browse()
    createtab.comment_edit.setText("Some Text")
    createtab.source_edit.setText("Some Source")
    assert createtab.path_group.getPath() == path


def test_create_tab_dir(dir2, wind):
    """Test create tab with folder."""
    path = dir2
    root = path
    createtab = wind.tabs.createWidget
    button = createtab.path_dir_button
    wind.stack.setCurrentWidget(createtab)
    proc_time()
    createTab.browse_folder = mock_func
    Obj.value = root
    button.browse()
    torfile = root + ".test.torrent"
    createtab.output_path_edit.setText(torfile)
    createtab.announce_input.setPlainText("announce.com")
    createtab.comment_edit.setText("comment")
    createtab.private.click()
    submit = createtab.submit_button
    submit.click()
    while proc_time(0.4):
        if wind.statusBar().currentMessage() != "Processing":
            break
    assert os.path.exists(torfile)
    rmpath(torfile)


@pytest.mark.parametrize(
    "field",
    [
        "announce",
        "announce-list",
        "source",
        "private",
        "comment",
        "piece length",
    ],
)
def test_create_tab_fields(dir2, field, wind):
    """Test create tab with folder."""
    path = dir2
    root = path
    createtab = wind.tabs.createWidget
    createtab.path_group.setPath(root)
    wind.stack.setCurrentWidget(createtab)
    proc_time(0.4)
    torfile = root + ".test.torrent"
    createtab.output_path_edit.setText(torfile)
    createtab.announce_input.setPlainText(
        "https://announce.com\nhttp://announce2.com\nhttp://announce4.com"
    )
    createtab.comment_edit.setText("some comment")
    createtab.private.setChecked(True)
    createtab.source_edit.setText("TestSource")
    submit = createtab.submit_button
    submit.click()
    proc_time(0.5)
    while proc_time(0.3):
        if wind.statusBar().currentMessage() != "Processing":
            break
    result = pyben.load(torfile)
    assert field in result or field in result["info"]
    rmpath(torfile)


def test_sized_create(wind):
    """Test browse file button on create tab."""
    path = str(tempfile(exp=28))
    createtab = wind.tabs.createWidget
    button = createtab.path_file_button
    Obj.value = path
    createTab.browse_files = mock_func
    button.click()
    proc_time()
    assert createtab.path_group.getPath() == path


def test_torrentfile_creator(dir1):
    """Test the QThread torrent file creator."""
    args = {"path": dir1, "outfile": dir1 + ".torrent"}
    creator = TorrentFileCreator(args, TorrentFileHybrid)
    creator.run()
    assert os.path.exists(dir1 + ".torrent")
    rmpath(dir1 + ".torrent")
