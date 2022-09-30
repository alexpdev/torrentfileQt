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

from torrentfileQt.utils import get_icon

arrow = path2url(os.path.relpath(get_icon("arrow-down"), os.getcwd()))

dark_theme = ("""
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
QWidget {
    background-color: #39434d;
    border-width: 0px;
}
*[editToolBar="true"] {
    background-color: #3a3a3a;
    spacing: 3px;
}
*[editToolBar="true"] QComboBox {
    background-color: #000;
    margin-left: 6px;
    border-width: 1px inset #f71;
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
*[InfoTree="true"]{
    background-color: #19232D;
    font-size: 10pt;
    show-decoration-selected: 1;
}
*[InfoTree="true"]::item {
    border: 1px solid #d9d9d9;
    border-top-color: transparent;
    border-bottom-color: transparent;
    margin-top: 1px;
    margin-bottom: 1px;
}
*[InfoTree="true"]::item:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #211, stop: 1 #312);
    border: 1px solid #f71;
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
QCheckBox {
    color: #fff;
    padding: 4px;
    font-size: 12pt;
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
QComboBox {
    border: 2px solid #f73;
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
    background: #555;
    padding: 1px 1px 1px 1px;
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
QDialog {
    background-color:#000000;
}
QGroupBox {
    border-style: solid;
    border-width: 1px;
    border-color: #841;
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
    color: #fff;
    background-color: #222;
}
QLabel,
QLabel:disabled {
    border-width: 1px;
    background-color: transparent;
    padding: 0px;
    font-size: 8pt;
    border-color: transparent;
    selection-background-color: #2f4f4f;
}
QLineEdit {
    padding: 4px;
    border-width: 1px;
    border-style: groove;
    margin-top: 3px;
    margin-bottom: 3px;
    font-size: 9pt;
    background-color: #19232D;
}
QLabel {
    padding: 2px;
    padding-top: 4px;
    padding-bottom: 4px;
    font-size: 10pt;
    font-weight: bold;
}
QMainWindow::separator {
    background: #000;
    border-width: 0px;
}
QMainWindow::separator:hover {
    background: transparent;
}
QMenuBar {
    background-color: #322;
    padding: 2px;
    font-size: 9pt;
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
    font-size: 8pt;
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
    padding: 3px 4px 3px 4px;
    font-size: 12pt;
    font-weight: bold;
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
QRadioButton {
    background-color: transparent;
    font-size: 12pt;
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
    color: #FFF;
}
QTabWidget::pane {
    border-top: 2px solid black;
    font-size: 10pt;
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
    width: 110px;
    padding-left: 2px;
    padding-right: 2px;
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
    padding-bottom: 0px;
    margin-right: 2px;
    background-color: #333;
}
QTreeWidget {
    border: 1px solid #f61;
    background-color: #5a5a5a;
    font-size: 9pt;
    color: #eeeeee;
}
QTreeWidget::item::selected {
    color: #FFFFFF;
    font-size: 9pt;
    border-color: transparent;
}
QTreeWidget::item::hover {
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
    border: dotted #ded 2px;
}
QTableWidget QTableCornerButton::section{
    background-color: black;
    border: 2px brown solid;
}
QToolBar {
    spacing: 6px;
}
QToolButton {
    font-size: 8pt;
    border-style: outset;
    border-color: #e67e22;
    border-width: 2px;
    border-radius: 8px;
    color: #FFF;
    padding: 2px;
    margin: 2px;
    background-color: #112;
}
QToolButton:hover {
    border-style: inset;
    margin-bottom: 1px;
    padding: 2px;
    background-color: #000;
}
""" % arrow)

light_theme = ("""
* {
    background-color: #7ea4d1;
    color: #000000;
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
    border-color: #0CF;
    selection-background-color: #a6595b;
}
QWidget {
    background-color: #E3E6F1;
    border-width: 0px;
}
*[editToolBar="true"] {
    background-color: #3a3a3a;
    spacing: 3px;
}
*[editToolBar="true"] QComboBox {
    background-color: #3cc;
    margin-left: 6px;
    border: 1px inset #5b310b;
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
    font-size: 9pt;
    margin: 0px;
}
*[editCombo="true"] {
    margin: 0px 0px 0px 0px;
    font-size: 12pt;
    border-width: 1px;
    padding: 0px 0px 0px 0px;
    min-height: 19px;
}
*[editButton="true"] {
    margin: 2px;
    padding: 2px;
    font-size: 10pt;
    border-radius: 12px;
}
*[infoLine="true"] {
    background-color: transparent;
    color: #000;
    font-size: 11pt;
    border-radius: 0px;
    border-width: 2px;
    padding: 0px;
    margin: 0px;
    border-left-color: transparent;
    border-right-color: transparent;
    border-top-color: transparent;
}
*[InfoTree="true"]{
    background-color: #a4bedf;
    font-size: 10pt;
    show-decoration-selected: 1;
}
*[InfoTree="true"]::item {
    border: 1px solid #d9d9d9;
    border-top-color: transparent;
    border-bottom-color: transparent;
    margin-top: 1px;
    margin-bottom: 1px;
}
*[InfoTree="true"]::item:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #e4cbcb, stop: 1 #edcbdc);
    border: 1px solid #f71;
}
*[InfoTree="true"]::item:selected {
    border: 1px solid #567dbc;
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
QAbstractScrollArea {
    background-color: #E3E6F1;
    border: 1px solid #0CF;
    border-radius: 4px;
    padding: 2px;
    color: #000;
}
QAbstractScrollArea:disabled {
    color: #E3E6F1;
}
QCheckBox {
    color: #000;
    padding: 4px;
    font-size: 12pt;
    border-color: transparent;
}
QCheckBox:disabled {
    color: #808086;
    font-size: 9pt;
    padding: 6px;
}
QCheckBox::indicator:checked {
    height: 13px;
    width: 13px;
    border-style: solid;
    border-width: 2px;
    border-color: #F41;
    color: #000;
    background-color: #FAEFEE;
}
QCheckBox::indicator:unchecked {
    height: 11px;
    width: 11px;
    border-style: solid;
    border-width: 2px;
    border-color: #F41;
    color: #000;
    background-color: transparent;
}
QComboBox QAbstractItemView {
    border: 1px solid #DFF;
    selection-background-color: lightgray;
}
QComboBox::down-arrow {
    image: url(%s);
}
QComboBox::down-arrow:on {
    top: 1px;
    background-color: #555;
}
QComboBox {
    border: 2px solid #F41;
    background-color: #3EC;
    font-size: 10pt;
    padding: 1px;
    min-width: 2em;
}
QComboBox:on {
    padding-top: 3px;
    padding-left: 4px;
}
QComboBox::drop-down {
    width: 20px;
    background: #0EE;
    padding: 1px;
    border-left-width: 2px;
    border-left-color: #449;
    border-left-style: outset;
}
QDialog {
    background-color: #CFE;
}
QGroupBox {
    border-style: solid;
    border-width: 1px;
    border-color: #CCF;
    margin: 8px;
    padding: 8px;
    border-radius: 12px;
    font-size: 15px;
    font-weight: bold;
}
QHeaderView::section {
    background-color: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1, stop:0 #719bfd:1 #88d9ff);
    color: #001111;
    font-size: 10pt;
    border: 1px solid #3cc;
    border-top-width: 0;
    border-left-color: #5e6163;
    border-right-color: #2a2c2d;
}
QHeaderView::section:hover {
    background-color: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1, stop:0 #77AFFF, stop:1 #99dcee);
    border-bottom-color: #AFF;
}
QHeaderView::section:first {
    border-left-width: 0;
}
QHeaderView::section:last {
    border-right-width: 0;
}
QHeaderView::section:checked {
    color: #000;
    background-color: #AFF;
}
QLineEdit {
    padding: 4px;
    border-width: 1px;
    border-style: groove;
    margin-top: 3px;
    margin-bottom: 3px;
    font-size: 9pt;
    background-color: #7ea4d1;
}
QLineEdit::read-only {
    background-color: #CFC;
}
QLabel {
    padding: 2px;
    padding-top: 4px;
    padding-bottom: 4px;
    font-size: 10pt;
    font-weight: bold;
}
QLabel,
QLabel:disabled {
    border-width: 1px;
    background-color: transparent;
    padding: 0px;
    font-size: 8pt;
    border-color: transparent;
    selection-background-color: #ccc;
}
QMenuBar {
    background-color: #eaffff;
    font-size: 9pt;
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
    font-size: 8pt;
    border: 1px solid #2d2d2d;
}
QMenu::item:disabled {
    color: #999999;
}
QMenu::item:selected {
    background-color: #4b9eCf;
}
QMenu::icon {
    border: 0px solid transparent;
    background-color: transparent;
}
QMenu::icon:checked {
    background-color: #ecf9ff;
    border: 1px inset red;
    position: absolute;
    top: 1px;
    right: 1px;
    bottom: 1px;
    left: 1px;
}
QMenu::separator {
    height: 2px;
    background-color: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1, stop:0 #282a2b, stop:1 #45484b);
    margin: 0 1px;
}
QMenu::indicator {
    width: 13px;
    height: 13px;
    background-color: #F55;
}
QMainWindow::separator {
    background: #0114fe;
    border-width: 0px;
}
QMainWindow::separator:hover {
    background: transparent;
}
QPlainTextEdit {
    background-color: #7ea4d1;
}
QPushButton{
    margin-top: 3px;
    margin-bottom: 3px;
    margin-left: 8px;
    margin-right: 8px;
    border-style: outset;
    border-top-color: #E66;
    border-right-color: #F55;
    border-left-color: #F43;
    border-bottom-color: #F41;
    border-radius: 6px;
    border-width: 3px;
    padding-top: 4px;
    font-size: 12pt;
    padding-bottom: 4px;
    font-weight: bold;
    color: #000000;
    background-color: #8eC2fd;
}
QPushButton:hover{
    border-style: inset;
    border-width: 3px;
    color: #6b3232;
    background-color: #5bc6f9;
}
QPushButton:pressed {
    border-style: inset;
    border-bottom-width: 3px;
    color: #482622;
    background-color: #d0f5fd;
}
QPushButton:disabled {
    border-style: solid;
    border-bottom-width: 1px;
    border-style: solid;
    color: #011;
    padding-bottom: 1px;
    background-color: #CCC;
}
QRadioButton {
    background-color: transparent;
    border: transparent;
    padding-top: 2px;
    font-size: 12pt;
    margin-top: 2px;
    margin-bottom: 2px;
    padding-bottom: 4px;
    color: #005;
}
QRadioButton::indicator::unchecked {
    border: 2px inset #333;
    border-radius: 6px;
    background-color:  #ffe006;
    width: 13px;
    height: 13px;
}
QRadioButton::indicator::unchecked:hover {
    border-radius: 5px;
    background-color: #fdfd00;
    width: 13px;
    height: 13px;
}
QRadioButton::indicator::checked {
    border: 2px inset #8e5740;
    border-radius: 4px;
    background-color: #f00;
    width: 13px;
    height: 13px;
}
QScrollArea QWidget QWidget:disabled {
    background-color: #E3E6F1;
}
QScrollBar:horizontal {
    height: 16px;
    margin: 2px 16px 2px 16px;
    border: 1px solid #EA7;
    border-radius: 4px;
    background-color: #25b511;
}
QScrollBar:vertical {
    background-color: #25b511;
    width: 16px;
    margin: 16px 2px 16px 2px;
    border: 1px solid #EA7;
    border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background-color: #AE7;
    border: 1px solid #EA7;
    border-radius: 4px;
    min-width: 8px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #665997;
    border: #553997;
    border-radius: 4px;
    min-width: 8px;
}
QScrollBar::handle:horizontal:focus {
    border: 1px solid #1A72BB;
}
QScrollBar::handle:vertical {
    background-color: #AE7;
    border: 1px solid #EA7;
    min-height: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background-color: #665997;
    border: #553997;
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
QScrollBar::sub-line:horizontal:hover,
QScrollBar::sub-line:horizontal:on {
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
QScrollBar::sub-line:vertical:hover,
QScrollBar::sub-line:vertical:on {
    height: 12px;
    width: 12px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
QStatusBar {
    border-top-color: #3c5953;
    border-top-width: 1px;
    font-size: 8pt;
    padding: 3px;
    color: #000000;
}
QTabWidget::pane {
    border-top-color: #667;
    border-top-width: 2px;
    border-top-style: outset;
    border-bottom-color: #444;
    border-bottom-width: 1px;
    font-size: 10pt;
}
QTabWidget::tab-bar {
    left: 5px;
}
QTabBar::tab {
    border-style: outset;
    border-color: #66aeff;
    border-width: 3px;
    color: #000000;
    font-size: 10pt;
    font-weight: bold;
    padding-left: 4px;
    padding-right: 4px;
    margin-right: 2px;
    padding-bottom: 2px;
    background-color: #faf7e7;
}
QTabBar::tab:hover {
    color: #002288;
}
QTabBar::tab:selected, QTabBar::tab:last:selected {
    border-color: #AFF;
    border-bottom-color: transparent;
    font-style: bold;
    border-width: 2px;
    border-style: inset;
    color: #000000;
    font-size: 10pt;
    padding-bottom: 0px;
    margin-right: 2px;
    margin-bottom: -3px;
    background-color: #E3E6F1;
}
QTableWidget {
    color: #000;
    font-size: 11pt;
    background-color: #7ea4d1;
    border-color: #8FF;
    border-width: 2px;
    border-style: ridge;
    border-radius: 4px;
    margin: 10px;
    selection-background-color: #F0AFA3;
    gridline-color: #ac4a02;
}
QTableWidget::item:selected:hover {
    background-color: #E66;
}
QTableWidget::item:hover {
    background-color: #CFF;
    border: dotted #ded 2px;
}
QTableWidget QTableCornerButton::section{
    background-color: black;
    border: 2px brown solid;
}
QToolBar {
    spacing: 6px;
}
QToolButton {
    border-style: outset;
    font-size: 8pt;
    border-color: #111;
    border-width: 3px;
    border-radius: 8px;
    color: #000;
    padding: 2px;
    margin: 2px;
    background-color: #8ea2fd;
}
QToolButton:hover {
    border-style: inset;
    margin-bottom: 1px;
    padding: 2px;
    background-color: #5bc6f9;
}
QTreeWidget {
    border: 1px solid #ACF;
    background-color: #7eadd1;
    font-size: 9pt;
    color: #000;
}
QTreeWidget::item::selected {
    font-size: 9pt;
    color: #000000;
    border-color: transparent;
}
QTreeWidget::item::hover {
    color: #3F3833;
    border-color: transparent;
}
QTreeWidget::indicator::checked {
    background-color: #000000;
    border: 1px solid #EC9;
}
QTreeWidget::indicator::unchecked {
    background-color: #000000;
    border: 1px solid #EC9;
}
QTreeWidget QProgressBar {
    color: black;
    background-color: #323;
    font-size: 12pt;
    border: 1px solid black;
    border-radius: 3px;
    margin-left: 2px;
    margin-right: 2px;
    text-align: center;
}
QTreeWidget QProgressBar::chunk {
    background-color: #99F;
    margin-left: .5px;
    margin-right: 0px;
    margin-top: 0px;
    margin-bottom: 0px;
    border-radius: 3px;
    width: 16px;
}
""" % arrow)
