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
import os

import pytest
from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar
from torrentfile import TorrentFile, TorrentFileHybrid, TorrentFileV2

from tests.context import rmpath, tstdir, tstdir2, tstfile
from torrentfileQt import qss
from torrentfileQt.window import TabWidget, alt_start


@pytest.fixture(scope="module")
def wind():
    """Pytest fixture for generating a new mainwindow wiget."""
    window, _ = alt_start()
    yield window
    print(window)


@pytest.fixture(scope="module", params=[tstdir, tstdir2])
def tdir(request):
    """Generate temporary directorie for tesing."""
    root = request.param()
    yield root


@pytest.fixture(scope="module", params=list(range(14, 28)))
def tfile(request):
    """Create temporary file for testing."""
    path = tstfile(val=request.param)
    yield path


@pytest.fixture(
    scope="module", params=[TorrentFile, TorrentFileV2, TorrentFileHybrid]
)
def ttorrent1(tfile, request):
    """Generate a metafile for testing."""
    path = tfile
    args = {
        "path": path,
        "private": 1,
        "announce": "tracker1.com",
        "comment": "this is a comment",
        "source": "Tracker",
    }
    torrent = request.param(**args)
    outfile, _ = torrent.write()
    yield outfile


@pytest.fixture(
    scope="module", params=[TorrentFile, TorrentFileV2, TorrentFileHybrid]
)
def dtorrent1(tdir, request):
    """Generate a metafile for testing with dir."""
    path = tdir
    args = {
        "path": path,
        "private": 1,
        "announce": "tracker1.com",
        "comment": "this is a comment",
        "source": "Tracker",
    }
    torrent = request.param(**args)
    outfile, _ = torrent.write()
    yield outfile


@pytest.fixture(
    scope="module", params=[TorrentFile, TorrentFileV2, TorrentFileHybrid]
)
def ttorrent2(tfile, request):
    """Generate a metafile for testing with file."""
    path = tfile
    args = {"path": path}
    torrent = request.param(**args)
    outfile, _ = torrent.write()
    yield outfile


@pytest.fixture(
    scope="module", params=[TorrentFile, TorrentFileV2, TorrentFileHybrid]
)
def dtorrent2(tdir, request):
    """Generate a metafile for testing with second dir."""
    args = {"path": tdir}
    torrent = request.param(**args)
    outfile, _ = torrent.write()
    yield outfile


def test_window1(wind):
    """Test Main Window Functionality."""
    assert wind is not None  # nosec


def test_window2(wind):
    """Test Window Functionality."""
    assert isinstance(wind, QMainWindow)  # nosec


def test_app1(wind):
    """Test app subclass."""
    assert wind.app is not None  # nosec


def test_app2(wind):
    """Test app subclass instance attribute."""
    assert isinstance(wind.app, QApplication)  # nosec


def test_qss():
    """For coverage reporting."""
    assert qss  # nosec


def test_window_menubar1(wind):
    """Test window Menubar widget."""
    assert wind.menubar is not None  # nosec


def test_window_statusbar1(wind):
    """Test window Statusbar widget."""
    assert wind.statusbar is not None  # nosec


def test_window_statusbar2(wind):
    """Test window Statusbar widget again."""
    assert isinstance(wind.statusbar, QStatusBar)  # nosec


def test_tab_widget(wind):
    """Test window Tab widget."""
    tabwidget = wind.central
    assert isinstance(tabwidget, TabWidget)  # nosec


def test_info_tab_select1(wind, ttorrent1):
    """Test Info tab select1."""
    infotab = wind.central.infoWidget
    button = infotab.selectButton
    button.selectTorrent(files=[ttorrent1])
    assert infotab.nameEdit.text() != ""  # nosec


def test_info_tab_select2(wind, ttorrent2):
    """Test Info tab selection."""
    infotab = wind.central.infoWidget
    button = infotab.selectButton
    button.selectTorrent(files=[ttorrent2])
    assert infotab.nameEdit.text() != ""  # nosec


def test_info_tab_dselect1(wind, dtorrent1):
    """Test Info tab selection directory."""
    infotab = wind.central.infoWidget
    button = infotab.selectButton
    button.selectTorrent(files=[dtorrent1])
    assert infotab.nameEdit.text() != ""  # nosec


def test_info_tab_dselect2(wind, dtorrent2):
    """Test Info tab selection directory again."""
    infotab = wind.central.infoWidget
    button = infotab.selectButton
    button.selectTorrent(files=[dtorrent2])
    assert infotab.nameEdit.text() != ""  # nosec


def test_create_tab_dir(tdir, wind):
    """Test create tab with folder."""
    root = tdir
    createtab = wind.central.createWidget
    button = createtab.browse_dir_button
    button.browse(root)
    torfile = root + ".test.torrent"
    outbutton = createtab.output_button
    outbutton.output(outpath=torfile)
    createtab.announce_input.setPlainText("announce.com")
    createtab.comment_input.setText("comment")
    createtab.private.click()
    submit = createtab.submit_button
    submit.click()
    assert os.path.exists(torfile)  # nosec


def test_create_tab_file(wind, tfile):
    """Test create tab with file."""
    createtab = wind.central.createWidget
    button = createtab.browse_file_button
    button.browse(tfile)
    torfile = tfile + ".test.torrent"
    outbutton = createtab.output_button
    outbutton.output(outpath=torfile)
    createtab.announce_input.setPlainText("announce.com")
    createtab.comment_input.setText("comment")
    createtab.private.click()
    submit = createtab.submit_button
    submit.click()
    assert os.path.exists(torfile)  # nosec


def test_create_tab_file_v2(wind, tfile):
    """Test create tab with file v2."""
    createtab = wind.central.createWidget
    button = createtab.browse_file_button
    createtab.v2button.click()
    button.browse(tfile)
    torfile = tfile + ".test.torrent"
    outbutton = createtab.output_button
    outbutton.output(outpath=torfile)
    createtab.announce_input.setPlainText("announce.com")
    createtab.comment_input.setText("comment")
    createtab.private.click()
    submit = createtab.submit_button
    submit.click()
    assert os.path.exists(torfile)  # nosec


def test_create_tab_file_hybrid(wind, tfile):
    """Test create tab with file hybrid."""
    createtab = wind.central.createWidget
    button = createtab.browse_file_button
    createtab.hybridbutton.click()
    button.browse(path=tfile)
    torfile = tfile + ".test.torrent"
    outbutton = createtab.output_button
    outbutton.output(outpath=torfile)
    createtab.announce_input.setPlainText("announce.com")
    createtab.comment_input.setText("comment")
    createtab.private.click()
    submit = createtab.submit_button
    submit.click()
    assert os.path.exists(torfile)  # nosec


def test_export_menu(wind, ttorrent2):
    """Test menubar action menu expornt."""
    infotab = wind.central.infoWidget
    button = infotab.selectButton
    button.selectTorrent(files=[ttorrent2])
    path = os.path.abspath("./tests/testfile.txt")
    wind.menubar.export(path=path)
    assert os.path.exists(path)  # nosec
    rmpath(path)
