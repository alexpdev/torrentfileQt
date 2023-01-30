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
from PySide6.QtWidgets import QMainWindow

from tests import wind
from torrentfileQt import qss
from torrentfileQt.__main__ import main
from torrentfileQt.infoTab import denom
from torrentfileQt.utils import StyleManager
from torrentfileQt.window import TabWidget


def test_denom():
    """Test denom function."""
    num = denom(50000000000)
    assert num == "50.0GB"


def test_denom_small():
    """Test denom function for small number."""
    num = denom(357)
    assert num == "357"
    assert wind
    assert main


def test_wind(wind):
    """Test app subclass."""
    assert isinstance(wind, QMainWindow)


def test_qss():
    """For coverage reporting."""
    assert qss is not None


def test_window_menubar1(wind):
    """Test window Menubar widget."""
    assert wind.menubar is not None


def test_tab_widget(wind):
    """Test window Tab widget."""
    tabwidget = wind.central
    assert isinstance(tabwidget, TabWidget)


def test_change_theme(wind):
    """Test changing the theme from the menubar."""
    wind.menubar.file_menu.actionLightTheme.trigger()
    wind.menubar.file_menu.actionDarkTheme.trigger()
    assert wind.menubar.file_menu.actionLightTheme.text() == "Light Theme"
    assert wind.menubar.file_menu.actionDarkTheme.text() == "Dark Theme"


def test_increase_font(wind):
    """Test font size plus menu option."""
    fontsize = wind.central.createWidget.path_label.font().pointSize()
    wind.menubar.file_menu.actionFontPlus.trigger()
    wind.menubar.file_menu.actionFontPlus.trigger()
    assert wind.central.createWidget.path_label.font().pointSize() > fontsize


def test_decrease_font(wind):
    """Test font size minus menu option."""
    fontsize = wind.central.createWidget.path_label.font().pointSize()
    wind.menubar.file_menu.actionFontMinus.trigger()
    wind.menubar.file_menu.actionFontMinus.trigger()
    assert wind.central.createWidget.path_label.font().pointSize() < fontsize


def test_styleManager():
    """Test style manager from utils module."""
    themes = {
        "test": """
QWidget {
    background-color: #000;
    color: #0AF;
    border-color: #F71;
    border-width: 3px;
    border-style: outset;
    border-radius: 8px;
}
QLineEdit,
QLabel {
    font-size: 15pt;


}
/* this is a comment*/


QCheckBox::indicator {
    background-color: red;
    margin: ;
}

/* this is a longer
comment that spans two lines */

QPushButton:pressed {
    border-width:
    3px;
    border-style:
    solid;
    border-color:
    #F71;
}

QPushButton:hover {color: #080;}
/* some comment
*/
QComboBox {
    border: 12px solid pink;
}"""
    }
    manager = StyleManager(themes)
    manager.current = themes["test"]
    collection = manager.parser.parse(themes["test"])
    manager.parser._compile()
    assert len(collection) > 1
