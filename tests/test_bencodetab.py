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
from torrentfile.torrent import TorrentFileHybrid

from tests import dir1, dir2, proc_time, tempfile, ttorrent, wind
from torrentfileQt.bencodeTab import Item


def test_fix():
    """Test fixtures."""
    assert dir1 and dir2 and tempfile and ttorrent and wind


def test_bencode_load_file(ttorrent, wind):
    """Test the load file function in the becodeEditWidget."""
    widget = wind.central.bencodeEditWidget
    widget.load_file([ttorrent])
    wind.central.setCurrentWidget(widget)
    proc_time(1)
    assert widget.treeview.rowCount() > 0


def test_bencode_load_folder(ttorrent, wind):
    """Test the load folder function in the bencodeEditWidget."""
    widget = wind.central.bencodeEditWidget
    dirname = os.path.dirname(ttorrent)
    widget.load_folder(dirname)
    wind.central.setCurrentWidget(widget)
    proc_time(1)
    assert widget.treeview.rowCount() > 0


@pytest.mark.parametrize("size", list(range(17, 20)))
def test_bencode_model(wind, ttorrent, size):
    """Test the bencodeEditor Item model."""
    paths = [ttorrent]
    for i in range(8):
        tfile = tempfile(exp=size + 2)
        args = {
            "path": tfile,
            "outfile": str(tfile) + ".torrent",
            "url_list": [f"url{i}", f"url{i+1}"],
            "announce": [f"url{i+2}", f"url{i+3}"],
            "comment": f"This is a comment + {i}",
            "source": f"SomeSource{i}",
            "private": 1,
            "piece_length": size - 1,
        }
        torrent = TorrentFileHybrid(**args)
        torrent.write()
        paths.append(args["outfile"])
    print(paths)
    widget = wind.central.bencodeEditWidget
    wind.central.setCurrentWidget(widget)
    proc_time()
    common = os.path.commonpath(paths)
    widget.load_folder(common)
    treeview = widget.treeview
    treeview.expandAll()
    proc_time()
    total = treeview.rowCount()
    for i in range(total):
        item = treeview.item(i, 0)
        assert str(item.itemData) == item.text()
        ritem = item
        while ritem.hasChildren():
            ritem = ritem.child(0)
            print(ritem.text())
        index = treeview.model().index(0, 0, ritem.index())
        treeview.model().setData(index, "marshmallow", 0)
        assert ritem.text() is not None
        proc_time()
        print(ritem.text())
        treeview.save_item(item)
    widget.clear_contents()
    proc_time(1)
    widget.save_changes()
    assert treeview.rowCount() == 0


def test_bencode_item(wind, ttorrent):
    """Test the bencode tab item object."""
    _ = wind
    meta = pyben.load(ttorrent)
    item = Item(value=ttorrent, data=meta)
    item.buildItem(meta, item)
    assert len(item.childItems) > 0
