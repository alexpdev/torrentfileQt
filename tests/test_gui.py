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

import pyben
import pytest
from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar

from tests.context import Temp, build, mktorrent, pathstruct, rmpath
from torrentfileQt import qss
from torrentfileQt.infoTab import denom
from torrentfileQt.window import TabWidget


def test_denom():
    """Test denom function."""
    num = denom(50000000000)
    assert num == "50.0GB"  # nosec


def test_denom_small():
    """Test denom function for small number."""
    num = denom(357)
    assert num == "357"  # nosec


def test_window1():
    """Test Main Window Functionality."""
    assert Temp.window is not None  # nosec


def test_window2():
    """Test Window Functionality."""
    assert isinstance(Temp.window, QMainWindow)  # nosec


def test_app1():
    """Test app subclass."""
    assert isinstance(Temp.app, QApplication)  # nosec


def test_app2():
    """Test app subclass instance attribute."""
    assert Temp.app is Temp.window.app  # nosec


def test_qss():
    """For coverage reporting."""
    assert qss is not None  # nosec


def test_window_menubar1():
    """Test window Menubar widget."""
    assert Temp.window.menubar is not None  # nosec


def test_window_statusbar1():
    """Test window Statusbar widget."""
    assert Temp.window.statusbar is not None  # nosec


def test_window_statusbar2():
    """Test window Statusbar widget again."""
    assert isinstance(Temp.window.statusbar, QStatusBar)  # nosec


def test_tab_widget():
    """Test window Tab widget."""
    tabwidget = Temp.window.central
    assert isinstance(tabwidget, TabWidget)  # nosec


@pytest.mark.parametrize("struct", pathstruct())
def test_create_tab_browse(struct):
    """Test Info tab select1."""
    path = build(struct)
    createtab = Temp.window.central.createWidget
    button = createtab.browse_file_button
    button.browse(path=path)
    assert createtab.path_input.text() == path  # nosec


@pytest.mark.parametrize("struct", pathstruct())
@pytest.mark.parametrize("hasher", Temp.hashers)
def test_info_tab_select1(struct, hasher):
    """Test Info tab select1."""
    path = build(struct)
    torrent = mktorrent(path, hasher)
    infotab = Temp.window.central.infoWidget
    button = infotab.selectButton
    button.selectTorrent(files=[torrent])
    assert infotab.nameEdit.text() != ""  # nosec


@pytest.mark.parametrize("struct", pathstruct())
def test_create_tab_dir(struct):
    """Test create tab with folder."""
    path = build(struct)
    root = path
    createtab = Temp.window.central.createWidget
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


@pytest.mark.parametrize(
    "field",
    [
        "announce",
        "announce list",
        "source",
        "private",
        "comment",
        "piece length",
    ],
)
@pytest.mark.parametrize("struct", pathstruct())
def test_create_tab_fields(struct, field):
    """Test create tab with folder."""
    path = build(struct)
    root = path
    createtab = Temp.window.central.createWidget
    button = createtab.browse_dir_button
    button.browse(root)
    torfile = root + ".test.torrent"
    outbutton = createtab.output_button
    outbutton.output(outpath=torfile)
    createtab.announce_input.setPlainText(
        "https://announce.com\nhttp://announce2.com\nhttp://announce4.com"
    )
    createtab.comment_input.setText("some comment")
    createtab.private.setChecked(True)
    createtab.source_input.setText("TestSource")
    submit = createtab.submit_button
    submit.click()
    result = pyben.load(torfile)
    assert field in result or field in result["info"]  # nosec


@pytest.mark.parametrize("struct", pathstruct())
@pytest.mark.parametrize("hasher", Temp.hashers)
def test_export_menu(struct, hasher):
    """Test menubar action menu expornt."""
    path = build(struct)
    torrent = mktorrent(path, hasher)
    infotab = Temp.window.central.infoWidget
    button = infotab.selectButton
    button.selectTorrent(files=[torrent])
    tpath = os.path.abspath(os.path.join(os.path.dirname(path), "torrent.txt"))
    Temp.window.menubar.export(path=tpath)
    assert os.path.exists(tpath)  # nosec
    rmpath(tpath)
