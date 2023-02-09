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

from PySide6.QtCore import QPoint

from tests import wind


class MockMouseEvent:
    """Mock event for testing."""

    def position(self):
        """Mock method for testing event."""
        assert wind
        return self

    @staticmethod
    def toPoint():
        """Mock method that returns QPoint."""
        return QPoint(1, 1)


def test_titlebar_buttons_min(wind):
    """Test titlebar button widget."""
    minbtn = wind.titleBar.minimizeButton
    minbtn.window_action()
    minbtn.window_action()
    assert wind.isMinimized() or wind.isVisible()


def test_titlebar_buttons_max(wind):
    """Test titlebar button widget."""
    maxbtn = wind.titleBar.maximizeButton
    maxbtn.window_action()
    maxbtn.window_action()
    assert wind.isMaximized() or wind.isVisible()


def test_titlebar_move(wind):
    """Test titlebar move event."""
    titlebar = wind.titleBar
    rect = titlebar.rect()
    event = MockMouseEvent()
    titlebar.mousePressEvent(event)
    titlebar.mouseMoveEvent(event)
    titlebar.mouseReleaseEvent(event)
    assert rect == titlebar.rect()


def test_titlebar_not_move(wind):
    """Test titlebar not move event."""
    titlebar = wind.titleBar
    titlebar._pressed = False
    event = MockMouseEvent()
    titlebar.mouseMoveEvent(event)


def test_titlebar_doubleclick(wind):
    """Test titlebar doubleclick event."""
    titlebar = wind.titleBar
    titlebar._pressed = False
    titlebar.mouseDoubleClickEvent(None)
    titlebar.mouseDoubleClickEvent(None)
    assert wind.isMaximized() or wind.isVisible()


def test_menubar_style(wind):
    """Test titlebar style dialog event."""
    menubar = wind.menubar
    options = menubar.options_menu
    options.styleAction.trigger()
    assert options.dialog
    options.saveStyle()
    options.closeStyleDialog()
