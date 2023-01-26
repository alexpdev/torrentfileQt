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

import os
from urllib.request import pathname2url as path2url
from string import Template

from torrentfileQt.utils import get_icon

arrow = path2url(os.path.relpath(get_icon("arrow-down"), os.getcwd()))

colors = {
    "_1":"#FFFFFF",
    "_2":"#19232D",
    "_3":"#f61",
    "_4":"#2f4f4f",
    "_5":"#402503",
    "_6":"#d63d12",
    "_7":"#311",
    "_8":"#555",
    "_9":"#333",
    "_10":"#111",
    "_11":"#704523",
    "_12":"#302513",
    "_arrow": arrow
}


dark = """
* {
    background-color: $_2;
    color: $_1;
    padding: 0px;
    margin: 0px;
    border-width: 0px;
    border-style: solid;
}
QMenu,
QTreeWidget,
QTreeWidget::item,
QTableWidget,
QTableWidget::item,
QHeaderView::section,
QTableView QTableCornerButton::section,
QLineEdit,
QTextEdit,
QComboBox,
QComboBox:editable,
QComboBox QAbstractItemView,
QProgressBar,
QScrollBar {
    border-width: 0px;
    border-style: solid;
    border-radius: 0px;
    padding: 0px;
    margin: 0px;
}
QHeaderView::section,
QTableView QTableCornerButton::section,
QLineEdit,
QTextEdit,
QComboBox:editable,
QComboBox,
QComboBox QAbstractItemView,
QProgressBar,
QPushButton {
    background-color: $_4;
}

QPushButton[titlebutton="true"] {
    background: transparent;
    margin: 3px;
    border: 0px transparent solid;
}
QScrollBar {
    border-color: $_3;
    selection-background-color: $_4;
}
QToolButton#titlebaricon {
    background-color: transparent;
    border-width: 0px;
    border-radius: 0px;
}
QLabel#titlebartitle {
    background-color: transparent;
    margin: 0px;
    padding: 0px;
}
QWidget#titlebar {
    background: $_5;
}
QWidget#tabbar {
    background: $_2;
}
QPushButton[Tab="true"] {
    background-color: transparent;
    border-radius: 0px;
    border-top-width: 0px;
    border-left-width: 0px;
    border-bottom-width: 0px;
    border-right-width: 3px;
    border-color: $_3;
    margin: 0px;
    padding-top: 15px;
    padding-bottom: 15px;
}
QPushButton[ActiveTab="true"] {
    background-color: $_8;
}
*[editToolBar="true"] {
    background-color: $_9;
    spacing: 3px;
}
*[editToolBar="true"] QComboBox {
    background-color: #000;
    margin-left: 6px;
    border-width: 1px inset $_3;
    border-radius: 4px;
    font-size: 9pt;
    padding: 3px;
}
*[editToolBar="true"] QComboBox QLineEdit {
    margin: 0px;
    padding: 0px;
}
*[createButton="true"] {
    padding: 3px;
    margin: 0px;
    font-size: 9pt;
}
*[editCombo="true"] {
    font-size: 12pt;
    margin: 0px 0px 0px 0px;
    border-width: 1px;
    padding: 0px 0px 0px 0px;
    min-height: 19px;
}
*[editLine="true"] {
    margin-left: 25px;
}
*[editButton="true"] {
    margin-left: 2px;
    margin-right: 2px;
    font-size: 10pt;
    border-radius: 12px;
}
*[editFileButton="true"] {
    margin-right: 20px;
}
*[infoLine="true"] {
    background-color: transparent;
    color: $_1;
    border-radius: 0px;
    border-width: 2px;
    font-size: 11pt;
    padding: 0px;
    margin: 0px;
    border-left-color: transparent;
    border-right-color: transparent;
    border-top-color: transparent;
}
*[InfoTree="true"]{
    background-color: $_2;
    font-size: 10pt;
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
                                stop: 0 #211, stop: 1 #312);
    border: 1px solid $_3;
}
*[InfoTree="true"]::item:selected {
    border: 1px solid #e0d3ba;
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
QMenu {
    margin: 0px;
    padding: 0px;
    background-color: $_7;
    color: $_1;
}
QMenuBar {
    margin: 1px;
    padding: 3px;
    spacing: 0px;
    background-color: transparent;
    color: $_1;
}
QAbstractScrollArea {
    background-color: $_2;
    border: 1px solid $_3;
    border-radius: 4px;
    padding: 2px;
    color: $_1;
}
QAbstractScrollArea:disabled {
    color: #9DA9B5;
}
QCheckBox {
    color: $_1;
    padding: 4px;
    font-size: 12pt;
    border-color: transparent;
}
QCheckBox:disabled {
    color: $_8;
    padding: 6px;
}
QCheckBox::indicator:checked {
    height: 13px;
    width: 13px;
    border-style:solid;
    border-width: 2px;
    border-color: $_3;
    color: #1;
    background-color: #6;
}
QCheckBox::indicator:unchecked {
    height: 11px;
    width: 11px;
    border-style:solid;
    border-width: 2px;
    border-color: $_3;
    color: $_1;
    background-color: transparent;
}
QComboBox {
    border: 2px solid $_3;
    padding: 1px;
    font-size: 10pt;
    min-width: 2em;
}
QComboBox:on {
    padding-top: 3px;
    padding-left: 4px;
}
QComboBox::drop-down {
    width: 20px;
    background: $_8;
    padding: 1px 1px 1px 1px;
    border-left-width: 2px;
    border-left-color: $_7;
    border-left-style: outset;
}
QComboBox::down-arrow:on {
    top: 1px;
}
QComboBox QAbstractItemView {
    border: 1px solid $_9;
    selection-background-color: lightgray;
}
QComboBox::down-arrow {
    image: url($_arrow);
}
QDialog {
    background-color: $_10;
}
QGroupBox {
    border-style: solid;
    border-width: 1px;
    border-color: $_11;
    margin: 8px;
    padding: 8px;
    border-radius: 12px;
    font-size: 15px;
    font-weight: bold;
}
QHeaderView::section {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0,
                    y2: 1, stop:0 #54585b, stop:1 #393c3e);
    color: #CFF;
    padding: 1px 2px 1px 4px;
    border: 1px solid #323232;
    border-top-width: 0;
    font-size: 10pt;
    font-weight: bold;
    border-left-color: #5e6163;
    border-right-color: #2a2c2d;
}
QHeaderView::section:hover {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0,
                    y2: 1, stop:0 #64686b, stop:1 #494c4e);
    border-bottom-color: #424242;
}
QHeaderView::section:first {
    border-left-width: 0;
}
QHeaderView::section:last {
    border-right-width: 0;
}
QHeaderView::section:checked {
    color: $_1;
    background-color: $_9;
}
QLabel,
QLabel:disabled {
    border-width: 1px;
    background-color: transparent;
    padding: 0px;
    font-size: 8pt;
    border-color: transparent;
    selection-background-color: $_4;
}
QLineEdit {
    padding: 4px;
    border-width: 1px;
    border-style: groove;
    margin-top: 3px;
    margin-bottom: 3px;
    font-size: 9pt;
    background-color: $_2;
}
QLabel {
    padding: 2px;
    padding-top: 4px;
    padding-bottom: 4px;
    font-size: 10pt;
    font-weight: bold;
}
QPushButton{
    margin-top: 3px;
    margin-bottom: 3px;
    margin-left: 8px;
    margin-right: 8px;
    border-style: outset;
    border-bottom-color: $_3;
    border-radius: 2px;
    border-top-width: 0px;
    border-left-width: 0px;
    border-right-width: 0px;
    border-bottom-width: 3px;
    padding: 5px 6px 5px 6px;
    font-size: 10pt;
    font-weight: bold;
    color: $_1;
    background-color: $_11;
}
QPushButton:hover{
    border-style: inset;
    border-bottom-color: #e67e22;
    color: #efefefef;
    background-color: $_12;
}
QPushButton:pressed{
    border-style: groove;
    border-bottom-width: 3px;
    border-bottom-color: $_3;
    color: $_1;
    background-color: $_5;
}
QPushButton:disabled{
    border-style: solid;
    border-bottom-width: 1px;
    border-style: solid;
    color: #bbb;
    padding-bottom: 1px;
    background-color: $_9;
}
QRadioButton {
    background-color: transparent;
    font-size: 12pt;
    border: transparent;
    padding-top: 2px;
    margin-top: 2px;
    margin-bottom: 2px;
    padding-bottom: 4px;
    color: $_1;
}
QRadioButton::indicator::unchecked {
    border: 1px inset $_3;
    border-radius: 6px;
    background-color:  $_2;
    width: 13px;
    height: 13px;
}
QRadioButton::indicator::unchecked:hover {
    border-radius: 5px;
    background-color:  $_2;
    width: 13px;
    height: 13px;
}
QRadioButton::indicator::checked {
    border: 1px inset $_3;
    border-radius: 5px;
    background-color: #ff5;
    width: 13px;
    height: 13px;
}
QScrollArea QWidget QWidget:disabled {
    background-color: $_2;
}
QScrollBar:horizontal {
    height: 16px;
    margin: 2px 16px 2px 16px;
    border: 1px solid $_4;
    border-radius: 4px;
    background-color: $_2;
}
QScrollBar:vertical {
    background-color: $_2;
    width: 16px;
    margin: 16px 2px 16px 2px;
    border: 1px solid $_4;
    border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background-color: #60798B;
    border: 1px solid #455364;
    border-radius: 4px;
    min-width: 8px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #346792;
    border: #346792;
    border-radius: 4px;
    min-width: 8px;
}
QScrollBar::handle:horizontal:focus {
    border: 1px solid #1A72BB;
}
QScrollBar::handle:vertical {
    background-color: #60798B;
    border: 1px solid #455364;
    min-height: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background-color: #346792;
    border: #346792;
    border-radius: 4px;
    min-height: 8px;
}
QScrollBar::handle:vertical:focus {
    border: 1px solid #1A72BB;
}
QScrollBar::add-line:horizontal {
    margin: 0px 0px 0px 0px;
    height: 12px;
    width: 12px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}
QScrollBar::add-line:horizontal:hover,
QScrollBar::add-line:horizontal:on {
    height: 12px;
    width: 12px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}
QScrollBar::add-line:vertical {
    margin: 3px 0px 3px 0px;
    height: 12px;
    width: 12px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::add-line:vertical:hover,
QScrollBar::add-line:vertical:on {
    height: 12px;
    width: 12px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal {
    margin: 0px 3px 0px 3px;
    height: 12px;
    width: 12px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on {
    height: 12px;
    width: 12px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    margin: 3px 0px 3px 0px;
    height: 12px;
    width: 12px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical:hover, QScrollBar::sub-line:vertical:on {
    height: 12px;
    width: 12px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
QStatusBar {
    border-top-color: black;
    background: #19232D;
    border-top-width: 1px;
    padding: 3px;
    font-size: 8pt;
    color: $_1;
}
QTreeWidget {
    border: 1px solid $_3;
    background-color: #5a5a5a;
    font-size: 9pt;
    color: #eeeeee;
}
QTreeWidget::item::selected {
    color: $_1;
    font-size: 9pt;
    border-color: transparent;
}
QTreeWidget::item::hover {
    color: #CFF8DC;
    border-color: transparent;
}
QTreeWidget::indicator::checked {
    background-color: $_1;
    border: 1px solid #536D79;
}
QTreeWidget::indicator::unchecked {
    background-color: $_1;
    border: 1px solid #536D79;
}
QTreeWidget QProgressBar {
    color: black;
    background-color: #7a7a7a;
    border: 1px solid black;
    border-radius: 3px;
    margin-left: 2px;
    font-size: 12pt;
    font-weight: bold;
    margin-right: 2px;
    text-align: center;
}
QTreeWidget QProgressBar::chunk {
    background-color: #3ae1de;
    margin-left: .5px;
    margin-right: 0px;
    margin-top: 0px;
    margin-bottom: 0px;
    border-radius: 3px;
    width: 16px;
}
QTableWidget {
    color: $_1;
    border-color: $_3;
    border-width: 2px;
    border-style: ridge;
    border-radius: 4px;
    margin: 10px;
    font-size: 11pt;
    selection-background-color: $_9;
    gridline-color: $_6;
}
QTableWidget::item:selected:hover {
    background-color: #7c7d7b;
}
QTableWidget::item:hover {
    background-color: #7c7d7b;
    border: dotted #ded 2px;
}
QTableWidget QTableCornerButton::section{
    background-color: black;
    border: 2px $_6 solid;
}
QToolBar {
    spacing: 6px;
}
QToolButton {
    font-size: 8pt;
    border-style: outset;
    border-color: $_3;
    border-width: 3px;
    border-radius: 8px;
    color: $_1;
    padding: 2px;
    margin: 1px;
    background-color: $_10;
}
QToolButton:hover {
    border-style: inset;
    background-color: $_10;
}
QToolButton:pressed {
    border-style: ridge;
    margin-bottom: 0px;
    margin-top: 2px;
    margin-left: 2px;
    margin-right: 0px;
    padding-bottom: 1px;
    padding-right: 1px;
    border-color: $_3;
    background-color: #000;
}
"""

theme = Template(dark)
dark_theme = theme.substitute(colors)
light_theme = theme.substitute(colors)
