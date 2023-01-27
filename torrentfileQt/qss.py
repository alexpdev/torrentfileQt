#! /usr/bin/python3
# -*- coding: utf-8 -*-
# ##############################################################################
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
"""Module for stylesheets."""

from pathlib import Path
from urllib.request import pathname2url as path2url

arrow_path = Path(__file__).parent / "assets" / "arrow.png"
arrow = path2url(str(arrow_path))

dark = {
    "_1":"#FFFFFF",
    "_2":"#19232D",
    "_3":"#f61",
    "_4":"#333a3f",
    "_5":"#402503",
    "_6":"#661d12",
    "_7":"#311",
    "_8":"#555",
    "_9":"#333",
    "_10":"#111",
    "_11":"#704523",
    "_12":"#302513",
    "_13":"#192031",
    "_14":"#656565",
    "_arrow": str(arrow)
}

light = {
    "_1":"#000000",
    "_2":"#59A3FD",
    "_3":"#CED",
    "_4":"#DA9",
    "_5":"#6F9",
    "_6":"#46DdE2",
    "_7":"#CFF",
    "_8":"#CCC",
    "_9":"#DDD",
    "_10":"#EEE",
    "_11":"#4075E3",
    "_12":"#A0D5E3",
    "_13":"#E9D0C1",
    "_arrow": str(arrow)
}


style = """
QMainWindow {
    background-color: $_2;
}
QWidget#centralTabWidget {
    background-color: $_2;
}
QWidget,
QMainWindow {
    background-color: $_2;
    color: $_1;
}
QLineEdit,
QTextEdit,
QTableWidget,
QTreeView,
QTreeWidget,
QPlainTextEdit,
QComboBox {
    border: 1px solid $_3;
    background-color: $_4;
    margin-left: 8px;
    margin-right: 8px;
}
QLineEdit {
    padding: 6px;
}
QPushButton {
    background-color: $_11;
    padding: 4px;
    margin-left: 4px;
    margin-right: 4px;
    border-left-width: 0px;
    border-right-width: 0px;
    border-top-width: 0px;
    border-radius: 3px;
    border-style: solid;
    border-color: $_3;
    border-bottom-width: 3px;
}
QWidget#tabbar {
    background-color: $_9;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
}
QMenuBar,
QWidget#titlebar {
    background-color: $_5;
}
QRadioButton,
QCheckBox,
QToolButton,
QLabel {
    background-color: transparent;
    margin: 3px;
    padding 3px;
    font-size: 10pt;
}
QPushButton[titlebutton="true"]{
    background-color: transparent;
    border-color: transparent;
    padding: 1px;
    border-width: 0px;
}
QHeaderView::section {
    color: $_1;
    background-color: $_14;
}
QStatusBar {
    background-color: $_4;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
}
QMenuBar {
    background-color: $_5;
    padding: 2px;
    font-size: 9pt;
    margin-bottom: 2px;
}
QMenuBar::item:pressed {
    background-color: $_4;
}
QMenuBar::item:selected:!pressed {
    background-color: $_14;
}
QMenu {
    border: 1px solid $_9;
    font-size: 8pt;
}
QMenu::item:selected {
    background-color: $_14;
}
QMenu::separator {
    height: 2px;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0,
                    y2: 1, stop:0 $_8, stop:1 $_9);
    margin: 0 1px;
}
QMenu::indicator {
    width: 13px;
    height: 13px;
    background-color: $_7;
}
*[InfoTree="true"]{
    font-size: 10pt;
    margin: 15px;
    show-decoration-selected: 1;
}
*[InfoTree="true"]::item {
    border: 1px solid $_1;
    border-top-color: transparent;
    border-bottom-color: transparent;
    margin-top: 1px;
    margin-bottom: 1px;
}
*[InfoTree="true"]::item:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 $_6, stop: 1 $_5);
    border: 1px solid $_3;
}
*[InfoTree="true"]::item:selected {
    border: 1px solid $_14;
}
*[InfoTree="true"]::branch {
        background: palette(transparent);
}
*[InfoTree="true"]::branch:has-siblings:!adjoins-item {
    border-image: url(torrentfileQt/assets/vline.png) 0;
}
*[InfoTree="true"]::branch:has-siblings:adjoins-item {
    border-image: url(torrentfileQt/assets/branch-more.png) 0;
}
*[InfoTree="true"]::branch:!has-children:!has-siblings:adjoins-item {
    border-image: url(torrentfileQt/assets/branch-end.png) 0;
}

*[InfoTree="true"]::branch:has-children:!has-siblings:closed,
*[InfoTree="true"]::branch:closed:has-children:has-siblings {
        border-image: none;
        image: url(torrentfileQt/assets/branch-closed.png);
}
*[InfoTree="true"]::branch:open:has-children:!has-siblings,
*[InfoTree="true"]::branch:open:has-children:has-siblings  {
        border-image: none;
        image: url(torrentfileQt/assets/branch-open.png);
}
*[InfoTree="true"] QLineEdit {
    border-width: 0px;
    padding: 0px;
    margin: 0px;
    font-size: 9pt;
}
"""

def tab_style(active):
    var = 8 if active else 9
    tab = f"""
        QPushButton[Tab="true"]{{
            padding-top: 18px;
            padding-bottom: 18px;
            border-bottom-width: 0px;
            padding-left: 8px;
            margin: 0px;
            font-size: 10pt;
            border-left-width: 0px;
            background-color: $_{var};
            border-top-width: 0px;
            border-right-width: 0px;
            border-radius: 0px;
        }}
    """
    return tab
