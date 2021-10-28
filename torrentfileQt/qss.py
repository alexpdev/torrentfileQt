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
        color: #eeeeee;
    }
    QTreeWidget::item::selected {
        color: #FFFFFF;
    }
    QTreeWidget::item::hover {
        color: #CFF8DC;
    }
    QTreeWidget::indicator::checked {
        background-color: #80CBC4;
        border: 1px solid #536D79;
    }
    QTreeWidget::indicator::unchecked {
	    background-color: #aad;
	    border: 1px solid #536D79;
    }
    """

menuSheet = """
    QMenu{
        background-color:#000000;
    }
    QMenuBar {
        background:rgb(30, 30, 30);
        color: #FFFFFF;
        margin-bottom: 1px;
        padding-bottom: 2px;
        font-size: 11pt;
    }
    QMenuBar::item {
        spacing: 3px;
        padding: 1px 4px;
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


mainWindowSheet = """
    QMainWindow {
        background-color:#ddd;
    }
    """

dialogSheet = """
    QDialog {
        background-color:#000000;
    }
    """

statusBarSheet = """
    QStatusBar {
        color:#027f7f;
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
    }
    """


pushButtonSheet = """
    QPushButton{
        margin-top: 3px;
        margin-bottom: 3px;
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-width: 1px;
        border-radius: 4px;
        padding: 2px;
        font: 14pt bold;
        color: #dedede;
        background-color: #111;
    }
    QPushButton::default{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-radius: 4px;
        border-width: 1px;
        padding: 2px;
        font: 14pt bold;
        color: #dedede;
        background-color: #111;
    }
    QPushButton:hover{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: #e67e22;
        border-left-color: #e67e22;
        border-bottom-color: #e67e22;
        border-width: 2px;
        border-radius: 3px;
        color: #efefefef;
        padding: 2px;
        background-color: #444;
    }
    QPushButton:pressed{
        border-style: solid;
        border-top-color: #e67e22;
        border-right-color: #e67e22;
        border-left-color: #e67e22;
        border-bottom-color: #e67e22;
        border-radius: 2px;
        border-bottom-width: 2px;
        padding: 1px;
        color: #ffffff;

        background-color: #444;
    }
    QPushButton:disabled{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: transparent;
        border-bottom-width: 2px;
        border-style: solid;
        color: #bbb;
        padding-bottom: 1px;
        background-color: #444;
    }
    """

push2ButtonSheet = """
    QPushButton {
        border-style: solid;
        border-top-color: #e67e22;
        border-right-color: #e67e22;
        border-left-color: #e67e22;
        border-bottom-color: #e67e22;
        border-bottom-width: 1px;
        border-style: solid;
        color: #FEFEFE;
        padding: 2px;
        background-color: #444;
    }
    QPushButton:hover{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-bottom-width: 2px;
        border-style: solid;
        color: #FFFFFF;
        padding-bottom: 1px;
        background-color: #000000;
    }"""


toolButtonSheet = """
    QToolButton {
        font-size: 10pt;
        border-style: solid;
        border-top-color: #e67e22;
        border-right-color: #e67e22;
        border-left-color: #e67e22;
        border-bottom-color: #e67e22;
        border-bottom-width: 1px;
        border-style: solid;
        color: #a9b7c6;
        padding: 2px;
        background-color: #444;
    }
    QToolButton:hover{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-bottom-width: 2px;
        border-style: solid;
        color: #FFFFFF;
        padding-bottom: 1px;
        background-color: #000000;
    }"""


checkBoxSheet = """
    QCheckBox {
        color: #000;
        padding: 6px;
    }
    QCheckBox:disabled {
        color: #808086;
        padding: 6px;
    }

    QCheckBox:hover {
        border-radius: 4px;
        border-style: #611 solid;
        padding: 4px;
        border-width: 2px;
        border-color: rgb(0, 0, 0);
        background-color:#dddddd;
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
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-width: 2px;
        font-size: 11pt;
        color: #e9e7e6;
        padding-left: 8px;
        padding-right: 8px;
        margin-right: 2px;
        background-color: #444;
    }
    QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {
        border-top-color: transparent;
        border-right-color: #e67e22;
        border-left-color: #e67e22;
        border-bottom-color: #e67e22;
        border-bottom-width: 2px;
        font-size: 11pt;
        font-style: bold;
        border-style: solid;
        color: #FFF;
        padding-left: 8px;
        padding-right: 8px;
        margin-right: 2px;
        background-color: #444;
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
        font-size: 10pt;
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

altLineEditSheet = """
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


textEditSheet = """
    QPlainTextEdit {
        selection-background-color:#f39c12;
        background-color: #646464;
        border: #1a1a1a 2px solid;
        color: #fff;
        border-style: solid;
        font: 9pt;
        border-radius: 4px;
        border-width: 1px;
    }
"""

labelSheet = """
    QLabel {
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
