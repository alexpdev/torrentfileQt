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

import os

import pyben
import pytest
from PySide6.QtCore import QItemSelectionModel, Qt
from torrentfile.torrent import TorrentFileHybrid

from tests import dir1, dir2, proc_time, tempfile, ttorrent, wind
from torrentfileQt import bencodeTab
from torrentfileQt.bencodeTab import Item


def test_fix():
    """Test fixtures."""
    assert dir1 and dir2 and tempfile and ttorrent and wind


@pytest.fixture(params=list(range(17, 20)))
def treedir(request):
    """Fixture for temporary torrent files."""
    paths = []
    for i in range(8):
        tfile = tempfile(exp=request.param + 2)
        args = {
            "path": tfile,
            "outfile": str(tfile) + ".torrent",
            "url_list": [f"url{i}", f"url{i+1}"],
            "announce": [f"url{i+2}", f"url{i+3}"],
            "comment": f"This is a comment + {i}",
            "source": f"SomeSource{i}",
            "private": 1,
            "piece_length": request.param - 1,
        }
        torrent = TorrentFileHybrid(**args)
        torrent.write()
        paths.append(args["outfile"])
    return os.path.commonpath(paths)


def test_bencode_load_file(ttorrent, wind):
    """Test the load file function in the becodeEditWidget."""
    widget = wind.tabs.bencodeEditWidget

    def browse_torrent_mock(_):
        return [ttorrent]

    bencodeTab.browse_torrent = browse_torrent_mock
    widget.load_file()
    wind.stack.setCurrentWidget(widget)
    proc_time(1)
    assert widget.treeview.rowCount() > 0


def test_bencode_load_folder(ttorrent, wind):
    """Test the load folder function in the bencodeEditWidget."""
    widget = wind.tabs.bencodeEditWidget
    dirname = os.path.dirname(ttorrent)

    def browse_folder_mock(_):
        return dirname

    bencodeTab.browse_folder = browse_folder_mock
    widget.load_folder()
    wind.stack.setCurrentWidget(widget)
    proc_time(1)
    assert widget.treeview.rowCount() > 0


def test_treedir(treedir, wind):
    """Test item functions and model."""
    widget = wind.tabs.bencodeEditWidget

    def browse_folder_mock(_):
        return treedir

    bencodeTab.browse_folder = browse_folder_mock
    widget.load_folder()
    proc_time(1)
    assert widget.treeview.model().rowCount() > 0
    total = widget.treeview.rowCount()
    for i in range(total):
        item = widget.treeview.item(i, 0)
        ritem = item
        while ritem.hasChildren():
            ritem = ritem.child(0)
            parent = ritem.parent()
            isindex = ritem.isIndex()
            isroot = ritem.isRoot()
            icon = ritem.icon()
            text = ritem.text()
            _ = ritem.edited()
            _ = ritem.childCount()
            _ = ritem.columnCount()
            _ = ritem.data()
            index = ritem.index()
            for role in [Qt.DisplayRole, Qt.EditRole, Qt.DecorationRole]:
                info = widget.treeview.model().data(index, role)
                if info:
                    assert info in [text, icon]
            proc_time()
            if not ritem.hasChildren():
                widget.treeview.model().flags(index)
                assert isindex is False
                assert isroot is False
                assert parent.index() == widget.treeview.model().parent(index)
                proc_time()
                widget.treeview.model().setData(
                    index, "marshmallow", Qt.EditRole
                )
                proc_time()
                ritem.setData("smores")
                proc_time()
        widget.save_changes()
        proc_time()
        widget.treeview.save_item(item)
        proc_time()
        widget.treeview.clear()
        proc_time()
        widget.clear_contents()
        proc_time()
        assert widget.treeview.rowCount() == 0


def test_treeremove(treedir, wind):
    """Test item functions and model."""
    widget = wind.tabs.bencodeEditWidget

    def test_folder_mock(_):
        return treedir

    bencodeTab.browse_folder = test_folder_mock
    widget.load_folder()
    proc_time(1)
    assert widget.treeview.model().rowCount() > 0
    total = widget.treeview.rowCount()
    for i in range(total):
        item = widget.treeview.item(i, 0)
        ritem = item
        rect = widget.treeview.visualRect(ritem.index())
        widget.treeview.setSelection(
            rect, QItemSelectionModel.SelectionFlag.Select
        )
        widget.insert_view_item()
        widget.remove_view_item()


def test_bencode_item(treedir):
    """Test build items."""
    items = []
    for fd in os.listdir(treedir):
        if fd.endswith(".torrent"):
            path = os.path.join(treedir, fd)
            meta = pyben.load(path)
            root = Item(data=meta, value=path)
            Item.buildItem(meta, root)
            assert root.hasChildren()
            items.append(root)
    assert len(items) > 0
