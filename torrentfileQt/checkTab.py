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

import os
from PyQt6.QtCore import Qt

<<<<<<< HEAD
from PyQt6.QtWidgets import (QHBoxLayout, QPushButton,
                             QWidget, QFormLayout, QToolButton,
                             QFileDialog, QPlainTextEdit)
=======
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QTextBrowser,
    QPushButton,
    QWidget,
    QFormLayout,
    QRadioButton,
    QToolButton,
    QFileDialog,
)
>>>>>>> 8b2985791de7cc1c6157fbed3d81351b671e0a99

from torrentfile.checker import Checker

<<<<<<< HEAD
from torrentfileQt.qss import (pushButtonStyleSheet, toolButtonStyleSheet,
                               textEditStyleSheet)
=======
from torrentfileQt.qss import pushButtonStyleSheet, toolButtonStyleSheet
>>>>>>> 8b2985791de7cc1c6157fbed3d81351b671e0a99

from torrentfileQt.widgets import Label, LineEdit


class CheckWidget(QWidget):

    labelRole = QFormLayout.ItemRole.LabelRole
    fieldRole = QFormLayout.ItemRole.FieldRole
    spanRole = QFormLayout.ItemRole.SpanningRole

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.hlayout1 = QHBoxLayout()
        self.hlayout2 = QHBoxLayout()

        self.fileLabel = Label("Torrent File", parent=self)
        self.fileLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.fileInput = LineEdit(parent=self)
        self.browseButton1 = BrowseTorrents(parent=self)

        self.searchLabel = Label("Search Path", parent=self)
        self.searchLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.searchInput = LineEdit(parent=self)
        self.browseButton2 = BrowseFolders(parent=self)
        self.checkButton = CheckButton("Check", parent=self)

        self.hlayout1.addWidget(self.fileInput)
        self.hlayout1.addWidget(self.browseButton1)
        self.hlayout2.addWidget(self.searchInput)
        self.hlayout2.addWidget(self.browseButton2)

        self.layout.setWidget(1, self.labelRole, self.fileLabel)
        self.layout.setLayout(1, self.fieldRole, self.hlayout1)
        self.layout.setWidget(2, self.labelRole, self.searchLabel)
        self.layout.setLayout(2, self.fieldRole, self.hlayout2)
        self.textEdit = PlainTextEdit(parent=self)
        self.layout.setWidget(3, self.spanRole, self.textEdit)
        self.layout.setWidget(4, self.spanRole, self.checkButton)

        self.layout.setObjectName(u"CheckWidget_layout")
        self.hlayout1.setObjectName("CheckWidget_hlayout1")
        self.hlayout2.setObjectName("CheckWidget_hlayout2")
        self.browseButton2.setObjectName("CheckWidget_browseButton2")
        self.browseButton1.setObjectName("CheckWidget_browseButton1")
        self.fileLabel.setObjectName("CheckWidget_fileLabel")
        self.searchLabel.setObjectName("CheckWidget_searchLabel")
        self.fileInput.setObjectName("CheckWidget_fileInput")
        self.searchInput.setObjectName("CheckWidget_searchInput")


class CheckButton(QPushButton):
    """Button Widget for validating torrent files against downloaded contents.

    Args:
        text (`str`): The text displayed on the button itself.
        parent (`QWidget`, default=None): This widgets parent widget.
    """

    stylesheet = pushButtonStyleSheet

    def __init__(self, text, parent=None):
        """Construct the CheckButton Widget."""
        super().__init__(text, parent=parent)
        self.pressed.connect(self.submit)
        self.setStyleSheet(self.stylesheet)

    def submit(self):
        def parse_text(text):
            window.textEdit.insertPlainText(text + "\n")
        window = self.parent()
        tfile = window.fileInput.text()
        folder = window.searchInput.text()
        def func(text):
            window.textEdit.insertPlainText(text + "\n")
        Checker.add_callback(func)
        checker = Checker(tfile, folder)
        percent = checker.check()
        window.textEdit.appendPlainText("\n" + percent + "\n")


<<<<<<< HEAD
=======

class BrowseButton(QToolButton):
    """
    BrowseButton ToolButton for activating filebrowser.
>>>>>>> 8b2985791de7cc1c6157fbed3d81351b671e0a99

class BrowseTorrents(QToolButton):
    """BrowseButton ToolButton for activating filebrowser.

    Subclass of QToolButton

    Args:
        parent (`widget`): Parent widget.
    """

    stylesheet = toolButtonStyleSheet

    def __init__(self, parent=None):
        """Construct Toolbar Button for selecting .torrentfile to check."""
        super().__init__(parent=parent)
        self.setText("...")
        self.window = parent
        self.setStyleSheet(self.stylesheet)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.inputWidget = None
        self.pressed.connect(self.browse)

    def browse(self, path=None):
        """Browse action performed when user presses button.

        Opens File/Folder Dialog.

        Returns:
            path (`str`): Path to file or folder to include in torrent.
        """
        caption = "Choose .torrent file."
        if not path:
            path = QFileDialog.getOpenFileName(parent=self,
                                               caption=caption,
                                               filter="*.torrent")
        if not path: return
        path = os.path.realpath(path[0])
        self.parent().fileInput.clear()
        self.parent().fileInput.setText(path)


class BrowseFolders(QToolButton):
    """Browse Folders ToolButton for activating filedialog.

    Args:
        parent (`QWidget`, default=None): Widget this widget is the child of.
    """

    stylesheet = toolButtonStyleSheet

    def __init__(self, parent=None):
        """Construct a BrowseFolders Button Widget."""
        super().__init__(parent=parent)
        self.setText("...")
        self.window = parent
        self.setStyleSheet(self.stylesheet)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pressed.connect(self.browse)

    def browse(self, path=None):
        """
        browse Action performed when user presses button.

        Opens File/Folder Dialog.

        Returns:
            str: Path to file or folder to include in torrent.
        """
        caption = "Choose Root Directory"
        if not path:
            path = QFileDialog.getExistingDirectory(parent=self, caption=caption)
<<<<<<< HEAD
        if not path: return
        self.parent().searchInput.clear()
        self.parent().searchInput.setText(path)


class PlainTextEdit(QPlainTextEdit):

    stylesheet = textEditStyleSheet

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.setBackgroundVisible(True)
        self.setStyleSheet(self.stylesheet)
=======
        if not path:
            return
        path = os.path.realpath(path)
        self.inputWidget.clear()
        self.inputWidget.setText(path)
>>>>>>> 8b2985791de7cc1c6157fbed3d81351b671e0a99
