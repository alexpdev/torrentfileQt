#! /usr/bin/python3
# -*- coding: utf-8 -*-

# ############################################################################
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

import string
from pathlib import Path

theme = """
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
    border: 1px inset $_3;
    background-color: $_4;
    margin-left: 8px;
    margin-right: 8px;
    border-radius: 8px;
}
QComboBox,
QLineEdit {
    padding: 6px;
}
QGroupBox QComboBox::drop-down {
    border-bottom-right-radius: 9px;
    border-top-right-radius: 9px;
    background-color: $_16;
}
QGroupBox QComboBox::down-arrow {
    image: url($_arrow);
}
QPushButton {
    background-color: $_16;
    font-weight: bold;
    padding: 4px;
    margin-left: 4px;
    margin-right: 4px;
    border-radius: 8px;
    border-style: outset;
    border-color: $_3;
    border-width: 2px;
}
QPushButton:hover {
    background-color: $_20;
}
QPushButton:pressed {
    background-color: $_20;
    border-style: inset;
}
QGroupBox {
    margin-left: 4px;
    margin-right: 4px;
}
QGroupBox::title {
    font-weight: bold;
    font-size: 11pt;
}
QWidget#tabbar {
    background-color: $_10;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
}
QMenuBar,
QWidget#titlebar {
    background-color: $_16;
}
#titlebar QLabel {
    font-weight: bold;
}
QRadioButton,
QCheckBox,
QToolButton,
QLabel {
    background-color: transparent;
    font-size: 10pt;
}
QPushButton[titlebutton="true"]{
    background-color: transparent;
    border-color: transparent;
    padding: 1px;
    border-width: 0px;
}
QHeaderView {
    gridline-color: transparent;
    color: $_1;
    background-color: $_14;
    border-radius: 8px;
}
QHeaderView::section {
    color: $_1;
    background-color: $_14;
    font-weight: bold;
    border-radius: 8px;
}
QStatusBar {
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
}
QMenuBar {
    padding-top: 3px;
    font-size: 10pt;
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
    background-color: $_7;
}
QScrollBar:horizontal {
    border: 1px solid $_7;
    background-color: $_5;
    height: 18px;
    margin: 0px 18px 0 18px;
}
QScrollBar::handle:horizontal {
    background-color: $_7;
    border: 1px solid $_17;
    border-radius: 6px;
    min-height: 20px;
}
QScrollBar::add-line:horizontal {
    border: 1px solid $_17;
    background-color: $_14;
    width: 18px;
    height: 16px;
    border-radius: 5px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal {
    border: 1px solid $_17;
    background-color: $_14;
    width: 18px;
    height: 16px;
    border-radius: 5px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}
QScrollBar::right-arrow:horizontal {
    width: 8px;
    height: 8px;
}
QScrollBar::left-arrow:horizontal {
    width: 8px;
    height: 8px;
}
QScrollBar::add-page:horizontal {
    background: none;
}
QScrollBar::sub-page:horizontal {
    background: none;
}
QScrollBar:vertical {
    background-color: $_5;
    width: 18px;
    margin: 18px 0 18px 0;
    border: 1px solid $_7;
}
QScrollBar::handle:vertical {
    background-color: $_7;
    border: 1px solid $_17;
    border-radius: 6px;
    min-height: 20px;
}
QScrollBar::add-line:vertical {
    border: 1px solid $_17;
    background-color: $_14;
    height: 18px;
    width: 16px;
    border-radius: 5px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    border: 1px solid $_17;
    background-color: $_14;
    height: 18px;
    width: 16px;
    border-radius: 5px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
QScrollBar::up-arrow:vertical {
    width: 8px;
    height: 8px;
}
QScrollBar::down-arrow:vertical {
    width: 8px;
    height: 8px;
}
QScrollBar::add-page:vertical {
    background: none;
}
QScrollBar::sub-page:vertical {
    background: none;
}
QStatusBar {
    background-color: qlineargradient(
        spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 $_13,stop:1 $_2);
    color: $_1;
    border-color: $_6;
    font-weight: bold;
}
*[DropGroupBox="true"] {
    border: 1px dashed $_14;
    background-color: $_13;
    border-radius: 15px;
    margin-top: 8px;
}
*[DropGroupBox="true"] QLabel {
    margin-top: 12px;
    font-weight: normal;
    font-size: 10pt;
}
*[DropGroupBox="true"]::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    font-weight: bold;
    font-size: 11pt;
    margin-left: 18px;
}
*[DropGroupBox="true"] QPushButton {
    background-color: transparent;
    border-width: 0px 0px 2px 0px;
    color: $_1;
}
*[DropGroupBox="true"] QPushButton:hover {
    border-color: $_18;
    color: $_15;
}
*[InfoTree="true"]{
    font-size: 10pt;
    margin: 15px;
    show-decoration-selected: 1;
}
*[InfoTree="true"]::item {
    margin-top: 1px;
    margin-bottom: 1px;
}
*[InfoTree="true"]::item:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 $_8, stop: 1 $_9);
    border: 1px solid $_3;
}
*[InfoTree="true"]::item:selected {
    border: 1px solid $_14;
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

#CreateOutButton {
    padding: 4px 55px 4px 55px;
}
#CreateSubmitButton {
    margin: 0px 15px 0px 15px;
}
#CreateCentralWidget QLabel {
    font-weight: bold;
    font-size: 10pt;
    margin: 0px 0px;
}
#CreatePathGroup QLabel {
    font-weight: normal;
    font-size: 9pt;
}
#CreateCentralWidget QComboBox {
    padding: 3px;
    margin: 3px;
}
#CreatePieceLength,
#CreateVersionBox {
    margin-top: 8px;
    border-radius: 8px;
    border-width: 1px;
    border-style: solid;
    border-color: $_14;
}
#CreatePieceLength::title,
#CreateVersionBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top-left;
    margin-left: 18px;
}
#CreateProgressTable {
    selection-background-color: $_18;
    color: $_1;
}
#CreateProgressTable QProgressBar {
    border: 4px solid $_10;
    border-radius: 14px;
    background-color: transparent;
    text-align: center;
    color: $_1;
}
#CreateProgressTable QProgressBar::chunk{
    background-color: $_19;
    border-radius: 10px;
}
#checkTree QProgressBar {
    border: 4px solid $_10;
    border-radius: 14px;
    background-color: transparent;
    text-align: center;
    color: $_1;
}
#checkTree QProgressBar::chunk{
    background-color: $_19;
    border-radius: 10px;
}
#checkTree {
    margin-bottom: 8px;
}
#checkTextEdit {
    margin-top: 8px;
}
#EditDropGroup {
    margin-left: 20px;
    margin-right: 20px;
}
#EditDropGroup QPushButton {
    margin-left: 3px;
    margin-right: 3px;
}
#EditGroupBox {
    padding: 0px;
    margin: 0px;
}
#EditGroupBox QPushButton {
    padding: 4px 6px;
    margin-left: 4px;
    margin-right: 4px;
    border-radius: 12px;
    border-color: $_3;
    border-width: 2px;
    background-color: $_16;
}
#EditGroupBox QComboBox {
    padding: 8px 0px;
    padding-right: 0px;
    margin-left: 4px;
    margin-right: 0px;
    max-width: 300px;
}
#EditGroupBox QComboBox QLineEdit {
    padding: 0px;
    margin: 0px;
}
#EditGroupBox QComboBox {
    margin-left: 0px;
}
#EditTable {
    margin: 8px;
    padding: 2px;
    gridline-color: $_17;
    font-size: 10pt;
    selection-background-color: $_18;
}
#EditTable QCheckBox {
    margin-left: 12px;
    padding: 4px;
}
#EditTable QGroupBox {
    background-color: $_4;
}
#EditSaveButton {
    margin: 15px;
    padding:8px;
}
#bencodeMainLabel,
#checkMainLabel,
#createMainLabel,
#editorMainLabel,
#infoMainLabel,
#rebuildMainLabel,
#toolMainLabel {
    font-size: 12pt;
    font-weight: bold;
    color: $_1;
}
#minButton:hover {
    icon: url(torrentfileQt/assets/min-light.png);
}
#maxButton:hover {
    icon: url(torrentfileQt/assets/max-light.png);
}
#closeButton:hover {
    icon: url(torrentfileQt/assets/close-light.png);
}
QSplitter::handle {
    background: $_8;
    width: 1px;
    margin-left: 222px;
    margin-right: 222px;
    margin-bottom: 2px;
    border-radius: 8px;
}
#toolTab * {
    margin: 2px;
}
#toolTab QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top-left;
    padding-left: 15px;
    padding-right: 15px;
}
"""


class Styles:
    """Style sheet class."""

    stylesheet = theme
    arrow_path = Path(__file__).parent / "assets" / "arrow-down.png"
    arrow = str(arrow_path).replace("\\", "/")
    dark = {
        "_1": "#FFFFFF",
        "_2": "#19232D",
        "_3": "#f61",
        "_4": "#333a3f",
        "_5": "#112244",
        "_6": "#661d12",
        "_7": "#311",
        "_8": "#555",
        "_9": "#333",
        "_10": "#111",
        "_11": "#704523",
        "_12": "#302513",
        "_13": "#1F3249",
        "_14": "#858585",
        "_15": "#FFFFAA",
        "_16": "#248",
        "_17": "#EA3",
        "_18": "#599F95",
        "_19": "#073",
        "_20": "#147",
        "_arrow": str(arrow),
    }
    light = {
        "_1": "#000000",
        "_2": "#E6DCD2",
        "_3": "#09E",
        "_4": "#CCC5C0",
        "_5": "#EEDDBB",
        "_6": "#99E2ED",
        "_7": "#CEE",
        "_8": "#AAA",
        "_9": "#CCC",
        "_10": "#EEE",
        "_11": "#8FBADC",
        "_12": "#CFDAEC",
        "_13": "#E0CDB6",
        "_14": "#7A7A7A",
        "_15": "#000055",
        "_16": "#DB7",
        "_17": "#15C",
        "_18": "#A6606A",
        "_19": "#F8C",
        "_20": "#EB8",
        "_arrow": str(arrow),
    }
    keys = {"light": light, "dark": dark}

    @staticmethod
    def compile(stylesheet, theme):
        """Compile style sheet."""
        template = string.Template(stylesheet)
        return template.substitute(theme)

    @staticmethod
    def tab_stylesheet(active):
        """Generate style sheet for Tab Widgets."""
        var = 8 if active else 9
        tab = f"""
            QPushButton[Tab="true"] {{
                padding-top: 18px;
                padding-bottom: 18px;
                padding-left: 8px;
                border-width: 0px;
                border-radius: 0px;
                margin: 0px;
                font-size: 10pt;
                background-color: $_{var};
        }}"""
        return tab
