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
from PySide6.QtWidgets import QApplication, QMainWindow

from tests import wind
from torrentfileQt import qss
from torrentfileQt.infoTab import denom
from torrentfileQt.window import TabWidget


def test_wind():
    """Test wind fixture."""
    assert wind


def test_denom():
    """Test denom function."""
    num = denom(50000000000)
    assert num == "50.0GB"


def test_denom_small():
    """Test denom function for small number."""
    num = denom(357)
    assert num == "357"


def test_window1(wind):
    """Test Main Window Functionality."""
    window, _ = wind
    assert window is not None


def test_window2(wind):
    """Test Window Functionality."""
    window, _ = wind
    assert isinstance(window, QMainWindow)


def test_app1(wind):
    """Test app subclass."""
    _, app = wind
    assert isinstance(app, QApplication)


def test_app2(wind):
    """Test app subclass instance attribute."""
    window, app = wind
    assert app is window.app


def test_qss():
    """For coverage reporting."""
    assert qss is not None


def test_window_menubar1(wind):
    """Test window Menubar widget."""
    window, _ = wind
    assert window.menubar is not None


def test_tab_widget(wind):
    """Test window Tab widget."""
    window, _ = wind
    tabwidget = window.central
    assert isinstance(tabwidget, TabWidget)
