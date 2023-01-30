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
"""Testing module for most of GUI."""

import pytest
from torrentfile import magnet
from torrentfile.torrent import TorrentFile

from tests import (
    MockEvent,
    dir1,
    dir2,
    proc_time,
    rmpath,
    tempfile,
    ttorrent,
    wind,
)


@pytest.fixture(scope="module")
def torrent(dir1):
    """Creates torrent pytest fixture."""
    args = {
        "path": dir1,
        "source": "source",
        "announce": ["https://tracker1.com/announce"],
        "piece_length": "16",
        "comment": "some comment",
    }
    torrent = TorrentFile(**args)
    outfile, meta = torrent.write()
    yield outfile, meta
    rmpath(outfile)


def test_fixture():
    """Testing pytest fixtures."""
    assert [dir1, dir2, tempfile, wind, ttorrent]


def test_create_magnet(wind, torrent):
    """Test creating Magnet URI from a torrent file path."""
    outfile, _ = torrent
    tab = wind.central.toolWidget
    wind.central.setCurrentWidget(tab)
    widget = tab.magnetgroup
    widget.pathEdit.setText(str(outfile))
    widget.submit_button.click()
    out = widget.magnetEdit.text()
    proc_time()
    assert out == magnet(outfile)


def test_create_magnet_method(wind, torrent):
    """Test creating Magnet URI from a torrent file path."""
    outfile, _ = torrent
    tab = wind.central.toolWidget
    wind.central.setCurrentWidget(tab)
    tab = tab.magnetgroup
    tab.metafilebutton.select_metafile(outfile)
    tab.submit_button.magnet()
    out = tab.magnetEdit.text()
    proc_time()
    assert out == magnet(outfile)


def test_magnet_accept_method(wind, ttorrent):
    """Test drag enter event on editor widget."""
    tab = wind.central.toolWidget
    tab.window.central.setCurrentWidget(tab)
    proc_time()
    event = MockEvent(ttorrent)
    assert tab.magnetgroup.dragEnterEvent(event)
    event = MockEvent(None)
    assert not tab.magnetgroup.dragEnterEvent(event)


def test_magnet_move_event(wind, ttorrent):
    """Test move event on magnet widget."""
    tools = wind.central.toolWidget
    tools.window.central.setCurrentWidget(tools)
    proc_time()
    event = MockEvent(ttorrent)
    assert tools.magnetgroup.dragMoveEvent(event)
    event = MockEvent(None)
    assert not tools.magnetgroup.dragMoveEvent(event)


def test_magnet_drop_event(wind, ttorrent):
    """Test drop event on editor widget."""
    tools = wind.central.toolWidget
    tools.window.central.setCurrentWidget(tools)
    proc_time()
    event = MockEvent(ttorrent)
    assert tools.magnetgroup.dropEvent(event)


def test_magnet_drop_false(wind):
    """Test drop event on editor widget returns None."""
    tools = wind.central.toolWidget
    tools.window.central.setCurrentWidget(tools)
    proc_time()
    event = MockEvent(None)
    assert not tools.magnetgroup.dropEvent(event)


def test_piecelengthcalculator(wind, dir1):
    """Test the piece length calculator."""
    tools = wind.central.toolWidget
    tools.window.central.setCurrentWidget(tools)
    proc_time()
    calculator = tools.piece_length_calculator
    calculator.browse_folders(dir1)
    assert calculator.path_line.text() == dir1


def test_piecelengthcalculator_file(wind):
    """Test the piece length calculator with a single file."""
    widget = wind.central.toolWidget
    widget.window.central.setCurrentWidget(widget)
    proc_time()
    calculator = widget.piece_length_calculator
    temp = str(tempfile())
    calculator.browse_files(temp)
    assert calculator.path_line.text() == temp
    calculator.piece_length_combo.setCurrentIndex(3)
    calculator.calculate_piece_length()
    rmpath(temp)
