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
from urllib.request import pathname2url as path2url

theme = """
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
    background-color: $_16;
    padding: 4px;
    margin-left: 4px;
    margin-right: 4px;
    border-radius: 8px;
    border-style: solid;
    border-color: $_3;
    border-width: 2px;
}
QGroupBox {
    margin-left: 4px;
    margin-right: 4px;
}
QGroupBox::title {
    font-weight: bold;
    font-size: 11pt;
    padding-left: 4px;
    padding-right: 4px;
}
QWidget#tabbar {
    background-color: $_10;
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
}
QHeaderView::section {
    color: $_1;
    background-color: $_14;
    font-weight: bold;
}
QStatusBar {
    background-color: $_4;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
}
QMenuBar {
    background-color: $_5;
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
    subcontrol-position: top center;
    font-weight: bold;
    font-size: 11pt;
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
    gridline-color: $_17;
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
                                stop: 0 $_8, stop: 1 $_9);
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
    subcontrol-position: top;
}
#CreateProgressTable {
    gridline-color: $_17;
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
#CheckTree {
    gridline-color: $_17;
    selection-background-color: $_18;
}
#CheckTree QProgressBar {
    border: 4px solid $_10;
    border-radius: 14px;
    background-color: transparent;
    text-align: center;
    color: $_1;
}
#CheckTree QProgressBar::chunk{
    background-color: $_19;
    border-radius: 10px;
}
#EditDropGroup {
    margin-left: 20px;
    margin-right: 20px;
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
"""

class Styles:
    arrow_path = Path(__file__).parent / "assets" / "arrow.png"
    arrow = path2url(str(arrow_path))
    dark = {
        "_1": "#FFFFFF",
        "_2": "#19232D",
        "_3": "#f61",
        "_4": "#333a3f",
        "_5": "#402503",
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
        "_16": "#55A",
        "_17": "#EA3",
        "_18": "#599F95",
        "_19": "#073",
        "_arrow": str(arrow),
    }
    light = {
        "_1": "#000000",
        "_2": "#59A3FD",
        "_3": "#CED",
        "_4": "#DA9",
        "_5": "#6F9",
        "_6": "#46DdE2",
        "_7": "#CFF",
        "_8": "#CCC",
        "_9": "#DDD",
        "_10": "#EEE",
        "_11": "#4075E3",
        "_12": "#A0D5E3",
        "_13": "#E9D0C1",
        "_14": "#8B8B8B",
        "_15": "#000055",
        "_16": "#BB6",
        "_17": "#26D",
        "_18": "#B7707B",
        "_19": "#073",
        "_arrow": str(arrow),
    }
    @staticmethod
    def compile(style):
        template = string.Template(theme)
        return template.substitute(style)

    light_theme = compile(light)
    dark_theme = compile(dark)

    def tab_style(active):
        var = 8 if active else 9
        tab = f"""
            QPushButton[Tab="true"] {{
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
        }}"""
        return tab
