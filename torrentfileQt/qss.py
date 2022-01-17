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

stylesheet = (
    """
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
    QLineEdit {
        border-width: 2px;
        padding: 4px;
        border-radius: 8px;
    }
    QAbstractScrollArea {
        background-color: #19232D;
        border: 1px solid #455364;
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
        border-top: 2px solid black
    }
    QTabWidget::tab-bar {
        left: 5px;
    }
    QTabBar::tab {
        border-style: outset;
        border-color: #f51;
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
        border: 2px inset #f73;
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
        border: 2px inset #d73;
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
        border: 1px solid #1a1a6a;
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
        margin-right: .5px;
        margin-top: 1px;
        margin-bottom: 1px;
        border-radius: 3px;
        width: 16px;
    }
    QTableWidget {
        background-color: #5a5a5a;
        color: #ddd;
        border-color: #e57e22;
        border-width: 2px;
        border-style: ridge;
        font-size: 11pt;
        selection-background-color: #3a3a3a;
        selection-color: #FFF;
        gridline-color: #ac4a02;
    }
    QTableWidget QTableCornerButton::section{
        background-color: black;
        border: 2px brown solid;
    }
    QTableWidget QHeaderView {
        border: 1px solid #e57e22;
        font-size: 11pt;
        background-color: black;
        color: white;
    }
    QTableWidget QHeaderView::section {
        background-color: black;
        color: white;
    }
    QMenu {
        background-color: black;
        margin: 2px;
    }
    QMenu::item {
        padding: 2px 25px 2px 20px;
        border: 1px solid transparent;
    }
    QMenu::item:selected {
        border-color: #e57e22;
        background: #333;
    }
    QMenu::icon:checked {
        background: gray;
        border: 1px inset gray;
        position: absolute;
        top: 1px;
        right: 1px;
        bottom: 1px;
        left: 1px;
    }
    QMenu::separator {
        height: 2px;
        background: lightblue;
        margin-left: 10px;
        margin-right: 5px;
    }
    QMenu::indicator {
        width: 13px;
        height: 13px;
    }
    QMenuBar {
        font-size: 9pt;
        border-bottom: 3px groove #115;
        background:rgb(30, 30, 30);
        color: #FFFFFF;
        margin-bottom: 1px;
        padding: 3px;
    }
    QMenuBar::item {
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: transparent;
        font-size: 9pt;
        padding: 6px;
        padding-top: 2px;
        background: transparent;
        border-bottom-width: 1px;
        border-style: solid;
        color: #a9b7c6;
    }
    QMenuBar::item:selected {
        border-style: ridge;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-bottom-width: 1px;
        color: #FFFFFF;
        padding-bottom: 3px;
        background-color: #000000;
    }
    QDialog {
        background-color:#000000;
    }
    QLineEdit {
        padding: 4px;
        margin-top: 3px;
        margin-bottom: 3px;
        font: 9pt;
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
        image: url("./assets/icons/down-arrow16.png");
    }
    """
)

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

pushButtonEdit = """
    QPushButton {
        padding: 3px;
        margin: 0px;
        font-size: 9pt;
    }
"""
