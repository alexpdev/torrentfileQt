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

import pytest

from tests import MockEvent, switchTab, tempdir, wind
from torrentfileQt import createTab


class MockReturn:
    """Mock class for testing."""

    value = None


def mock_func(_):
    """Mock function for testing."""
    assert wind
    return MockReturn.value


createTab.browse_files = mock_func
createTab.browse_folder = mock_func
createTab.browse_torrent = mock_func


@pytest.fixture(scope="module")
def tdir():
    """Test fixture for create widget."""
    dirname = tempdir(6, 2, 27, [".r00", ".mp3", ".mkv", ".dat", ".zip"])
    return dirname


def test_create_setPath(wind, tdir):
    """Test functions for the create widget."""
    tab = wind.tabs.createWidget
    switchTab(wind.stack, tab)
    tab.setPath(tdir)
    assert tab.path_group.getPath() == tdir


def test_create_write_thread(wind, tdir):
    """Test functions for the create widget."""
    tab = wind.tabs.createWidget
    switchTab(wind.stack, tab)
    tab.setPath(tdir)
    createTab.TorrentFileCreator.start = createTab.TorrentFileCreator.run
    outval = tab.output_path_edit.text()
    tab.submit_button.click()
    assert os.path.exists(outval)


@pytest.mark.parametrize("version", [1, 2, 3])
def test_create_write_param_thread(wind, tdir, version):
    """Test functions for the create widget."""
    tab = wind.tabs.createWidget
    switchTab(wind.stack, tab)
    tab.setPath(tdir)
    if version == 2:
        tab.v2button.setChecked(True)
    elif version == 3:
        tab.hybridbutton.setChecked(True)
    else:
        tab.v1button.setChecked(True)
    createTab.TorrentFileCreator.start = createTab.TorrentFileCreator.run
    outval = tab.output_path_edit.text()
    tab.source_edit.setText("source")
    tab.private.setChecked(True)
    tab.comment_edit.setText("some comment")
    tab.announce_input.setPlainText("url1\nurl2")
    tab.web_seed_input.setPlainText("url3\nurl4")
    tab.submit_button.click()
    assert os.path.exists(outval)


def test_create_browse_dir(wind, tdir):
    """Test functions for the create widget."""
    tab = wind.tabs.createWidget
    switchTab(wind.stack, tab)
    MockReturn.value = tdir
    tab.path_dir_button.click()
    assert tab.path_group.getPath() == tdir


def test_create_browse_file(wind, tdir):
    """Test functions for the create widget."""
    tab = wind.tabs.createWidget
    switchTab(wind.stack, tab)
    MockReturn.value = tdir
    tab.path_file_button.click()
    assert tab.path_group.getPath() == tdir


def test_create_drag_enter_event(wind, tdir):
    """Test functions for the create widget."""
    widget = wind.tabs.createWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(tdir)
    assert widget.path_group.dragEnterEvent(event)


def test_create_drag_enter_no_event(wind):
    """Test functions for the create widget."""
    widget = wind.tabs.createWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(None)
    assert not widget.path_group.dragEnterEvent(event)


def test_create_drag_move_event(wind, tdir):
    """Test functions for the create widget."""
    widget = wind.tabs.createWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(tdir)
    assert widget.path_group.dragMoveEvent(event)


def test_create_drag_move_no_event(wind):
    """Test functions for the create widget."""
    widget = wind.tabs.createWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(None)
    assert not widget.path_group.dragMoveEvent(event)


def test_create_drop_event(wind, tdir):
    """Test functions for the create widget."""
    widget = wind.tabs.createWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(tdir)
    assert widget.path_group.dropEvent(event)


def test_create_drop_no_event(wind):
    """Test functions for the create widget."""
    widget = wind.tabs.createWidget
    switchTab(wind.stack, widget=widget)
    event = MockEvent(None)
    assert not widget.path_group.dropEvent(event)
