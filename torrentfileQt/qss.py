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
"""Module for stylesheets."""

import os
from urllib.request import pathname2url as path2url

arrow = os.path.join(os.environ["ASSETS"], "arrow-down.png")


dark_theme = """
* {
    background-color: #19232D;
    color: #FFFFFF;
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
QScrollBar {
    border-color: #f61;
    selection-background-color: #2f4f4f;
}

QLabel,
QLabel:disabled {
    border-width: 1px;
    background-color: transparent;
    padding: 0px;
    border-color: transparent;
    selection-background-color: #2f4f4f;
}

QMainWindow::separator {
    background: #000;
    border-width: 0px;
}

QMainWindow::separator:hover {
    background: transparent;
}

QWidget {
    background-color: #39434d;
    border-width: 0px;
}

QAbstractScrollArea {
    background-color: #19232D;
    border: 1px solid #f61;
    border-radius: 4px;
    padding: 2px;
    color: #E0E1E3;
}

QAbstractScrollArea:disabled {
    color: #9DA9B5;
}

QScrollArea QWidget QWidget:disabled {
    background-color: #19232D;
}

QScrollBar:horizontal {
    height: 16px;
    margin: 2px 16px 2px 16px;
    border: 1px solid #455364;
    border-radius: 4px;
    background-color: #19232D;
}

QScrollBar:vertical {
    background-color: #19232D;
    width: 16px;
    margin: 16px 2px 16px 2px;
    border: 1px solid #455364;
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

QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on {
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

QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {
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

QTabWidget::pane {
    border-top: 2px solid black;
}

QTabWidget::tab-bar {
    left: 5px;
}

QTabBar::tab {
    border-style: outset;
    border-color: #f61;
    border-width: 3px;
    font-size: 10pt;
    color: #e9e7e6;
    padding-left: 8px;
    padding-right: 8px;
    margin-right: 2px;
    padding-bottom: 2px;
    background-color: #444;
}

QTabBar::tab:hover {
    color: #ffffff;
}

QTabBar::tab:selected, QTabBar::tab:last:selected {
    border-color: #e76500;
    font-style: bold;
    border-width: 2px;
    border-style: inset;
    color: #ffffff;
    padding-left: 8px;
    padding-right: 8px;
    padding-bottom: 0px;
    margin-right: 2px;
    background-color: #333;
}

QPushButton{
    margin-top: 3px;
    margin-bottom: 3px;
    margin-left: 8px;
    margin-right: 8px;
    border-style: outset;
    border-top-color: #e18133;
    border-right-color: #e67f2f;
    border-left-color: #e67f2f;
    border-bottom-color: #e67e22;
    border-radius: 8px;
    border-width: 3px;
    padding-top: 4px;
    padding-bottom: 4px;
    font: 13pt bold;
    color: #dedede;
    background-color: #111;
}

QPushButton:hover{
    border-style: inset;
    border-width: 3px;
    color: #efefefef;
    background-color: #000;
}

QPushButton:pressed{
    border-style: inset;
    border-bottom-width: 3px;
    color: #ffffff;
    background-color: #112;
}

QPushButton:disabled{
    border-style: solid;
    border-bottom-width: 1px;
    border-style: solid;
    color: #bbb;
    padding-bottom: 1px;
    background-color: #444;
}

QToolButton {
    font-size: 9pt;
    border-style: outset;
    border-color: #e67e22;
    border-width: 3px;
    border-radius: 8px;
    color: #FFF;
    padding: 5px;
    padding-top: 3px;
    background-color: #112;
}

QToolButton:hover {
    border-style: inset;
    margin-bottom: 1px;
    padding: 4px;
    background-color: #000;
}

QRadioButton {
    background-color: transparent;
    font-size: 11pt;
    border: transparent;
    padding-top: 2px;
    margin-top: 2px;
    margin-bottom: 2px;
    padding-bottom: 4px;
    color: #fff;
}

QRadioButton::indicator::unchecked {
    border: 1px inset #f73;
    border-radius: 6px;
    background-color:  #323232;
    width: 13px;
    height: 13px;
}

QRadioButton::indicator::unchecked:hover {
    border-radius: 5px;
    background-color:  #323232;
    width: 13px;
    height: 13px;
}

QRadioButton::indicator::checked {
    border: 1px inset #d73;
    border-radius: 5px;
    background-color: #ff5;
    width: 13px;
    height: 13px;
}

QCheckBox {
    color: #fff;
    padding: 4px;
    font-size: 11pt;
    border-color: transparent;
}

QCheckBox:disabled {
    color: #808086;
    padding: 6px;
}

QCheckBox::indicator:checked {
    height: 13px;
    width: 13px;
    border-style:solid;
    border-width: 2px;
    border-color: #e67e22;
    color: #a9b7c6;
    background-color: #d63d12;
}

QCheckBox::indicator:unchecked {
    height: 11px;
    width: 11px;
    border-style:solid;
    border-width: 2px;
    border-color: #e67e22;
    color: #a9b7c6;
    background-color: transparent;
}

QTreeWidget {
    border: 1px solid #f61;
    background-color: #5a5a5a;
    font: 8pt;
    color: #eeeeee;
}

QTreeWidget::item::selected {
    color: #FFFFFF;
    font-size: 9pt;
    border-color: transparent;
}

QTreeWidget::item::hover {
    font-size: 9pt;
    color: #CFF8DC;
    border-color: transparent;
}

QTreeWidget::indicator::checked {
    background-color: #ffffff;
    border: 1px solid #536D79;
}

QTreeWidget::indicator::unchecked {
    background-color: #ffffff;
    border: 1px solid #536D79;
}

QTreeWidget QHeaderView::section {
    background-color: black;
    color: white;
}

QTreeWidget QHeaderView::section {
    border: 1px solid #e57e22;
    background-color: black;
    color: white;
}

QTreeWidget QProgressBar {
    color: black;
    background-color: #7a7a7a;
    border: 1px solid black;
    border-radius: 3px;
    margin-left: 2px;
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
    color: #fff;
    border-color: #f71;
    border-width: 2px;
    border-style: ridge;
    border-radius: 4px;
    margin: 10px;
    font-size: 11pt;
    selection-background-color: #3a3a3a;
    gridline-color: #ac4a02;
}

QTableWidget::item:selected:hover {
    background-color: #7c7d7b;
}

QTableWidget::item:hover {
    background-color: #7c7d7b;
    border: dotted #ded 1px;
}

QTableWidget QTableCornerButton::section{
    background-color: black;
    border: 2px brown solid;
}

QHeaderView::section {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0,
                    y2: 1, stop:0 #54585b, stop:1 #393c3e);
    color: #bbbbbb;
    padding: 1px 2px 1px 4px;
    border: 1px solid #323232;
    border-top-width: 0;
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
    color: #fff;
    background-color: #222;
}
QMenuBar {
    background-color: #322;
    padding: 2px;
    margin-bottom: 2px;
    border-bottom: 2px solid #555555;
}
QMenuBar::item:pressed {
    background-color: #4b6eaf;
}
QMenuBar::item:selected:!pressed {
    background-color: #585b5d;
}
QMenu {
    border: 1px solid #2d2d2d;
}
QMenu::item:disabled {
    color: #999999;
}
QMenu::item:selected {
    background-color: #4b6eaf;
}
QMenu::icon {
    border: 0px solid transparent;
    background-color: transparent;
}
QMenu::icon:checked {
    background-color: blue;
    border: 1px inset red;
    position: absolute;
    top: 1px;
    right: 1px;
    bottom: 1px;
    left: 1px;
}
QMenu::separator {
    height: 2px;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0,
                    y2: 1, stop:0 #282a2b, stop:1 #45484b);
    margin: 0 1px;
}
QMenu::indicator {
    width: 13px;
    height: 13px;
    background-color: blue;
}

QDialog {
    background-color:#000000;
}

QLineEdit {
    padding: 4px;
    border-width: 1px;
    border-style: groove;
    margin-top: 3px;
    margin-bottom: 3px;
    font: 9pt;
    background-color: #19232D;
}

QLabel {
    padding: 2px;
    padding-top: 4px;
    padding-bottom: 4px;
    font-size: 10pt;
    font-weight: bold;
}

QStatusBar {
    border: 2px groove black;
}

QComboBox {
    border: 2px solid #f73;
    padding: 1px 1px 1px 3px;
    font-size: 10pt;
    min-width: 2em;
}
QComboBox:on {
    padding-top: 3px;
    padding-left: 4px;
}
QComboBox::drop-down {
    width: 20px;
    background: #555;
    padding: 0px 2px 0px 2px;
    border-left-width: 2px;
    border-left-color: #311;
    border-left-style: outset;
}
QComboBox::down-arrow:on {
    top: 1px;
}
QComboBox QAbstractItemView {
    border: 1px solid #444;
    selection-background-color: lightgray;
}
QComboBox::down-arrow {
    image: url(%s);
}
""" % path2url(
    str(arrow)
)

light_theme = """
* {
    padding: 0px;
    margin: 0px;
    border: transparent 0px solid;
    border-radius: 0px;
    font-size: 10pt;
}
QLineEdit,
QTextEdit,
QListWidget,
QTableWidget,
QComboBox,
QTreeWidget {
    color: black;
    background-color: #000;
    border-color: black;
    border-width: 1px;
    border-radius: 2px;
    border-style: solid;
}
QTabBar::tab
QLabel,
QCheckBox,
QRadioButton,
QPushButton,
QToolButton {
    font-weight: bold;
    font-size: 10pt;
}
QPushButton,
QToolButton {
    border-style: outset;
    border-width: 3px;
    border-color: #555;
    border-radius: 8px;
    background-color: #efeccf;
}
QPushButton::hover,
QToolButton::hover {
    background-color: #dfdcef;
}
QPushButton:pressed,
QToolButton:pressed {
    border-style: inset;
    border-color: #333;
    background-color: #efeccc;
}
QDialog,
QWidget {
    background-color: #eae7e9;
}
QTabWidget::pane {
    border-top: 0px solid
}
QTabWidget::tab-bar {
    left: 5px;
}
QTabBar {
    border-color: transparent;
}
QTabBar::tab {
    border-style: outset;
    border-color: black;
    font-size: 10pt;
    border-right-width: 1px;
    border-left-width: 1px;
    border-top-width: 1px;
    border-bottom-color: transparent;
    border-bottom-width: 0px;
    color: black;
    padding-left: 8px;
    padding-right: 8px;
    margin-right: 2px;
    padding-bottom: 2px;
    background-color: #d1d0c9;
}
QTabBar::tab:hover {
    color: #00F;
}
QTabBar::tab:selected, QTabBar::tab:last:selected {
    border-color: black;
    font-style: bold;
    border-width: 2px;
    border-bottom-width: 0px;
    border-style: inset;
    color: black;
    padding-left: 8px;
    padding-right: 8px;
    padding-bottom: 0px;
    margin-right: 2px;
    background-color: #eae7e9;
}
QAbstractScrollArea,
QCombobox QAbstractItemView {
    background-color: #eee;
    border: 1px solid #444;
    border-radius: 4px;
    padding: 2px;
    color: #000;
}
"""

infoLineEdit = """
QLineEdit {
    background-color: transparent;
    color: #FFF;
    border-radius: 0px;
    border-width: 2px;
    font-size: 11pt;
    padding: 0px;
    margin: 0px;
    border-left-color: transparent;
    border-right-color: transparent;
    border-top-color: transparent;
}
"""

infoLineEditLight = """
QLineEdit {
    border-radius: 0px;
    border-width: 2px;
    color: black;
    font-size: 11pt;
    padding: 0px;
    margin: 0px;
    border-left-color: transparent;
    border-right-color: transparent;
    border-top-color: transparent;
    border-bottom-color: black;
}
"""

pushButtonEdit = """
QPushButton {
    padding: 3px;
    margin: 0px;
    font-size: 9pt;
}
"""

table_styles = {
    "LineEdit": """
    QLineEdit {
        padding: 0px;
        margin: 0px;
        padding: 0px;
    }
    """,
    "ComboBox": """
    QComboBox {
        font-size: 12pt;
        margin: 0px 0px 0px 0px;
        border-width: 1px;
        padding: 0px 0px 0px 0px;
        min-height: 19px;
    }
    """,
    "button": """
    QToolButton {
        margin: 2px;
        padding: 2px;
        border-radius: 12px;
    }
    """,
}
