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

from PyQt6.QtWidgets import QCheckBox, QComboBox, QLabel, QLineEdit, QTextEdit

from torrentfileQt.qss import (
    comboBoxStyleSheet,
    lineEditStyleSheet,
    checkBoxStyleSheet,
    labelStyleSheet,
)


class TextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setReadOnly(True)
        self.setAcceptRichText(True)
        self.setFontWeight(10)
        self.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoBulletList)


class CheckBox(QCheckBox):

    stylesheet = checkBoxStyleSheet

    def __init__(self, label, parent=None):
        super().__init__(label, parent=parent)
        self.setStyleSheet(self.stylesheet)


class Label(QLabel):
    """Label Identifier for Window Widgets.

    Subclass: QLabel
    """

    stylesheet = labelStyleSheet

    def __init__(self, text, parent=None):
        super().__init__(text, parent=parent)
        self.setStyleSheet(self.stylesheet)
        font = self.font()
        font.setBold(True)
        font.setPointSize(12)
        self.setFont(font)


class LineEdit(QLineEdit):

    stylesheet = lineEditStyleSheet

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.setStyleSheet(self.stylesheet)


class ComboBox(QComboBox):

    stylesheet = comboBoxStyleSheet

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        self.args = args
        self.kwargs = kwargs
        self.setStyleSheet(self.stylesheet)
        self.addItem("")
        for exp in range(14, 24):
            if exp < 20:
                item = str((2 ** exp) // (2 ** 10)) + "KB"
            else:
                item = str((2 ** exp) // (2 ** 20)) + "MB"
            self.addItem(item, 2 ** exp)
        self.setEditable(False)
