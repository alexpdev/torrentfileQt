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
"""Style Sheets for Qt Widgets a.k.a. QSS."""

treeSheet = """
    QTreeWidget {
        border: 1px solid #1a1a6a;
        background-color: #5a5a5a;
        font: 8pt;
        color: #eeeeee;
    }
    QTreeWidget::item::selected {
        color: #FFFFFF;
        font-size: 9pt;
    }
    QTreeWidget::item::hover {
        font-size: 9pt;
        color: #CFF8DC;
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
    """

treeViewSheet = """
    QTreeView {
        border: 1px solid #1a1a6a;
        background-color: #5a5a5a;
        font: 8pt;
        color: #eeeeee;
    }
    QTreeView::item::selected {
        color: #FFFFFF;
        font-size: 9pt;
    }
    QTreeView::item::hover {
        font-size: 9pt;
        color: #CFF8DC;
    }
    QTreeView::indicator::checked {
        background-color: #ffffff;
        border: 1px solid #536D79;
    }
    QTreeView::indicator::unchecked {
        background-color: #ffffff;
        border: 1px solid #536D79;
    }
    QTreeView QHeaderView::section {
        background-color: black;
        color: white;
    }
    QTreeView QHeaderView::section {
        border: 1px solid #e57e22;
        background-color: black;
        color: white;
    }
    QTreeView QProgressBar {
        background-color: #7a7a7a;
        border: 1px solid black;
        border-radius: 3px;
        margin-left: 2px;
        margin-right: 2px;
        text-align: center;
    }
    QTreeView QProgressBar::chunk {
        background-color: #3ae1de;
        margin-left: .5px;
        margin-right: .5px;
        margin-top: 1px;
        margin-bottom: 1px;
        border-radius: 3px;
        width: 16px;
    }
    """


tableSheet = """
    QTableWidget {
        background-color: #5a5a5a;
        color: #ddd;
        border-color: #e57e22;
        border-width: 2px;
        border-style: ridge;
        font-size: 12pt;
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
        font-size: 12pt;
        background-color: black;
        color: white;
    }
    QTableWidget QHeaderView::section {
        border: 1px solid #e57e22;
        background-color: black;
        color: white;
    }
"""


menuSheet = """
    QMenu{
        background-color:#000000;
        padding-top: 2px;
        padding-bottom: 2px;
    }
    QMenuBar {
        font-size: 10pt;
        background:rgb(30, 30, 30);
        color: #FFFFFF;
        margin-bottom: 1px;
        padding: 3px;
    }
    QMenuBar::item {
        spacing: 3px;
        padding: 1px 4px;
        padding-left: 6px;
        padding-right: 6px;
        padding-top: 3px;
        padding-bottom: 3px;
        background: transparent;
    }
    QMenuBar::item:selected {
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-bottom-width: 1px;
        border-style: solid;
        color: #FFFFFF;
        padding-bottom: 0px;
        background-color: #000000;
    }
    QMenu::item:selected {
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: #e67e22;
        border-bottom-color: transparent;
        border-left-width: 2px;
        color: #FFFFFF;
        padding-left:15px;
        padding-top:4px;
        padding-bottom:4px;
        padding-right:7px;
        background-color:#000000;
    }
    QMenu::item {
        border-style: solid;
        font-size: 10px;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: transparent;
        border-bottom-width: 1px;
        border-style: solid;
        color: #a9b7c6;
        padding-left:17px;
        padding-top:4px;
        padding-bottom:4px;
        padding-right:7px;
        background-color:#000000;
    }"""


dialogSheet = """
    QDialog {
        background-color:#000000;
    }
    """

statusBarSheet = """
    QStatusBar {
        color:#a11;
    }
    """

toolBoxSheet = """
    QToolBox {
        color: #a9b7c6;
        background-color:#000000;
    }
    QToolBox::tab {
        color: #a9b7c6;
        background-color:#000000;
    }
    QToolBox::tab:selected {
        color: #FFFFFF;
        background-color:#000000;
    }"""


scrollAreaSheet = """
    QScrollArea {
        color: #FFFFFF;
        background-color:#000000;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }"""


pushButtonSheet = """
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
        font: 14pt bold;
        color: #dedede;
        background-color: #111;
    }
    QPushButton:hover{
        border-style: inset;
        border-width: 3px;
        color: #efefefef;
        background-color: #200;
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
    """


push2ButtonSheet = """
    QPushButton {
        border-style: outset;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-bottom-width: 1px;
        border-style: solid;
        color: #FEFEFE;
        padding-top: 5px;
        padding-bottom: 5px;
        margin: 2px;
        background-color: #444;
    }
    QPushButton:hover{
        border-style: outset;
        border-top-color: transparent;
        border-right-color: #d65e22;
        border-left-color: #d65e22;
        border-bottom-color: #e67e22;
        border-width: 2px;
        border-style: solid;
        color: #FFFFFF;
        background-color: #000000;
    }
    """


toolButtonSheet = """
    QToolButton {
        font-size: 10pt;
        border-style: solid;
        border-left-color: transparent;
        border-right-color: transparent;
        border-top-color: transparent;
        border-bottom-color: #e67e22;
        border-width: 2px;
        padding-top: 2px;
        padding-bottom: 2px;
        padding-left: 3px;
        padding-right: 3px;
        margin-top: 1px;
        margin-bottom: 1px;
        color: #a9b7c6;
        background-color: #444;
    }
    QToolButton:hover{
        border-top-color: transparent;
        border-right-color: #e67e22;
        border-left-color: #e67e22;
        border-bottom-color: #e67e22;
        border-width: 3px;
        border-style: inset;
        color: #FFFFFF;
        padding-bottom: 3px;
        background-color: #000000;
    }
    """


checkBoxSheet = """
    QCheckBox {
        color: #000;
        padding: 4px;
        font-size: 15px;
    }
    QCheckBox:disabled {
        color: #808086;
        padding: 6px;
    }
    QCheckBox:hover {
        color: #00a;
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
    }"""


tabSheet = """
    QTabWidget {
        background-color:#EEE;
    }
    QTabWidget::pane {
            background-color:#EEE;
    }
    """


tabBarSheet = """
    QTabBar::tab {
        border-style: outset;
        border-color: #951;
        border-width: 3px;
        font-size: 11pt;
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
    }"""


radioButtonSheet = """
    QRadioButton {
        color: #a9b7c6;
        background-color:#000000;
        padding: 1px;
    }
    QRadioButton::indicator:checked {
        height: 10px;
        width: 10px;
        border-style:solid;
        border-radius:5px;
        border-width: 1px;
        border-color: #e67e22;
        color: #a9b7c6;
        background-color: #e67e22;
    }
    QRadioButton::indicator:!checked {
        height: 10px;
        width: 10px;
        border-style:solid;
        border-radius:5px;
        border-width: 1px;
        border-color: #e67e22;
        color: #a9b7c6;
        background-color: transparent;
    }
    """

lineEditSheet = """
    QLineEdit {
        border-color: #1a1a1a;
        font-size: 12pt;
        border-width: 1px;
        border-radius: 4px;
        border-style: inset;
        padding: 0 8px;
        color: #FFFFFF;
        background: #646464;
        selection-background-color: #411;
        selection-color: #0ff;
    }
    QLineEdit::disabled {
        background-color: #444;
        color: #ddd;
    }
    """


createLineEditSheet = """
    QLineEdit {
        border-color: #1a1a1a;
        font: 12pt;
        border-width: 1px;
        border-radius: 4px;
        border-style: inset;
        padding: 0 8px;
        color: #FFFFFF;
        background: #646464;
        selection-background-color: #411;
        selection-color: #0ff;
    }
    QLineEdit::disabled {
        background-color: #444;
        color: #ddd;
    }
    """

infoLineEditSheet = """
    QLineEdit {
        border-color: #3a3a3a;
        border-bottom-width: 2px;
        border-radius: 0px;
        border-style: inset;
        padding: 0 8px;
        font: 11pt bold;
        color: #000;
        background: #fff;
        selection-background-color: #bbbbbb;
        selection-color: #3c3f41;
    }
    QLineEdit::disabled {
        background-color: #fff;
        color: #000;
    }
    """

comboBoxSheet = """
    QComboBox {
        color: #FFF;
        background: #3a3a3a;
        font-size: 12pt;
    }
    QComboBox:editable {
        background: #1e1d23;
        color: #a9b7c6;
        selection-background-color:#3a3a3a;
    }
    QComboBox QAbstractItemView {
        color: #FFF;
        background: #3a3a3a;
        selection-color: #FFFFFF;
        selection-background-color:#3a3a3a;
    }
    QComboBox:!editable:on, QComboBox::drop-down:editable:on {
        color: #a9b7c6;
        background: #1e1d23;
    }
    QFontComboBox {
        color: #a9b7c6;
        background-color:#000000;
    }"""


logTextEditSheet = """
    QPlainTextEdit {
        selection-background-color: #aaa;
        background-color: #000;
        border: #00f 1px solid;
        color: #fff;
    }
"""

textEditSheet = """
    QPlainTextEdit {
        selection-background-color:#f39c12;
        background-color: #646464;
        border: #1a1a1a 2px solid;
        color: #fff;
        font: 10pt;
        border-radius: 4px;
    }
"""

labelSheet = """
    QLabel {
        font-size: 12pt;
        margin-top: 2px;
        margin-bottom: 2px;
        font-weight: bold;
        color: #191716;
    }
"""

spinboxSheet = """
    QSpinBox {
        color: #a9b7c6;
        background-color:#000000;
    }
    QDoubleSpinBox {
        color: #a9b7c6;
        background-color:#000000;
}"""


progressbarSheet = """
    QProgressBar {
        border: 2px solid black;
        border-radius: 8px;
        text-align: center;
    }
    QProgressBar::chunck {
        background-color: black;
        width: 8px;
        margin: 1px;
    }
"""


headerSheet = """
    QHeaderView {
        background-color: black;
        border: 1px solid #e67e22;
        height: 4px;
        color: black;
    }
"""


mainWindowSheet = """
    QMainWindow {
        background-color:#ddd;
    }
    """
