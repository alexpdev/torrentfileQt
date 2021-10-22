<<<<<<< HEAD
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


=======
>>>>>>> 8b2985791de7cc1c6157fbed3d81351b671e0a99
pushButtonStyleSheet = """
    QPushButton{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: transparent;
        border-width: 1px;
        border-style: solid;
        font: 14pt bold;
        color: #a9b7c6;
        padding: 2px;
        background-color: #000000;
    }
    QPushButton::default{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-width: 1px;
        color: #a9b7c6;
        padding: 2px;
        background-color: #000000;
    }
    QPushButton:hover{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-bottom-width: 1px;
        border-style: solid;
        color: #FFFFFF;
        padding-bottom: 2px;
        background-color: #000000;
    }
    QPushButton:pressed{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-bottom-width: 2px;
        border-style: solid;
        color: #e67e22;
        padding-bottom: 1px;
        background-color: #000000;
    }
    QPushButton:disabled{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: transparent;
        border-bottom-width: 2px;
        border-style: solid;
        color: #808086;
        padding-bottom: 1px;
        background-color: #000000;
    }
    """

push2ButtonStyleSheet = """
    QPushButton {
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


toolButtonStyleSheet = """
    QToolButton {
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


checkBoxStyleSheet = """
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


tabBarStyleSheet = """
    QTabWidget {
        background-color:#EEE;
    }
    QTabWidget::pane {
            background-color:#EEE;
    }
    QTabBar::tab {
        border-style: solid;
        border-top-color: #e67e22;
        border-right-color: #e67e22;
        border-left-color: #e67e22;
        border-bottom-color: #e67e22;
        border-bottom-width: 1px;
        border-style: solid;
        font-size: 11pt;
        color: #e9e7e6;
        padding-left: 8px;
        padding-right: 8px;
        margin-left: 4px;
        background-color: #444;
    }
    QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {
        border-style: solid;
        border-top-color: #e67e22;
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
        margin-left: 4px;
        background-color: #444;
    }"""


radioButtonStyleSheet = """
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

lineEditStyleSheet = """
    QLineEdit {
        border-color: #1a1a1a;
        font-size: 11pt;
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
        background-color: #222;
        color: #ddd;
    }
    """

altLineEditStyleSheet = """
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

editStyleSheet = """
    QLineEdit {
        border-width: 1px; border-radius: 4px;
        border-color: rgb(58, 58, 58);
        border-style: inset;
        padding: 0 8px;
        color: #f5f5f5;
        background:#000000;
        selection-background-color:#007b50;
        selection-color: #FFFFFF;
    }"""


comboBoxStyleSheet = """
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


textEditStyleSheet = """
    QPlainTextEdit {
        border: #1a1a1a 2px solid;
        border-radius: 4px;
        color: #FFFFFF;
        font: 11pt;
        background-color: #646464;
    }"""


labelStyleSheet = """
    QLabel {
        color: #191716;
    }
    """
