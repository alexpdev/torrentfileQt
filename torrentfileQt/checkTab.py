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
from threading import Thread
from collections.abc import Sequence

from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QToolButton,
    QTreeWidget,
    QTreeWidgetItem,
    QPlainTextEdit,
    QProgressBar,
    QWidget,
)
from torrentfile.progress import CheckerClass


from torrentfileQt.qss import (
    pushButtonSheet,
    toolButtonSheet,
    treeSheet,
    logTextEditSheet,
    pushButtonSheet,
    toolButtonSheet,
    treeSheet,
    headerSheet,
)
from torrentfileQt.widgets import Label, LineEdit


class CheckWidget(QWidget):

    labelRole = QFormLayout.ItemRole.LabelRole
    fieldRole = QFormLayout.ItemRole.FieldRole
    spanRole = QFormLayout.ItemRole.SpanningRole

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.window = parent.window
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
        self.textEdit = LogTextEdit(parent=self)
        self.treeWidget = TreeWidget(parent=self)
        self.layout.setWidget(3, self.spanRole, self.textEdit)
        self.layout.setWidget(4, self.spanRole, self.treeWidget)
        self.layout.setWidget(5, self.spanRole, self.checkButton)

        self.layout.setObjectName("CheckWidget_layout")
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

    def __init__(self, text, parent=None):
        """Construct the CheckButton Widget."""
        super().__init__(text, parent=parent)
        self.pressed.connect(self.submit)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(pushButtonSheet)
        self.torrent = None
        self.folder = None

    def submit(self):
        self.widget = self.parent()
        textEdit = self.widget.textEdit
        treeWidget = self.widget.treeWidget
        func1 = textEdit.callback
        func2 = treeWidget.callback
        CheckerClass.register_callbacks(func1, func2)
        self.torrent = self.widget.fileInput.text()
        self.folder = self.widget.searchInput.text()
        self.widget.treeWidget.setRoot(self.folder)
        # thread = Thread(group=None, target=self.re_check_torrent)
        # thread.run()
        self.re_check_torrent()

    def re_check_torrent(self):
        checker = CheckerClass(self.torrent, self.folder)
        msg = f"Torrent Contents are {checker.result}% completely downloaded."
        self.widget.textEdit.insertPlainText(msg)
        self.widget.treeWidget.perform_action()


class BrowseTorrents(QToolButton):
    """BrowseButton ToolButton for activating filebrowser.

    Subclass of QToolButton

    Args:
        parent (`widget`): Parent widget.
    """

    def __init__(self, parent=None):
        """Construct Toolbar Button for selecting .torrentfile to check."""
        super().__init__(parent=parent)
        self.setText("...")
        self.window = parent
        self.setStyleSheet(toolButtonSheet)
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
            path = QFileDialog.getOpenFileName(
                parent=self, caption=caption, filter="*.torrent"
            )
        if not path:
            return
        if isinstance(path, Sequence):
            path = path[0]
        path = os.path.realpath(path)
        self.parent().fileInput.clear()
        self.parent().fileInput.setText(path)


class BrowseFolders(QToolButton):
    """Browse Folders ToolButton for activating filedialog.

    Args:
        parent (`QWidget`, default=None): Widget this widget is the child of.
    """

    def __init__(self, parent=None):
        """Construct a BrowseFolders Button Widget."""
        super().__init__(parent=parent)
        self.setText("...")
        self.window = parent
        self.setStyleSheet(toolButtonSheet)
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
        if not path:
            return
        self.parent().searchInput.clear()
        self.parent().searchInput.setText(path)


class ProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)


class TreePieceItem(QTreeWidgetItem):
    def __init__(self, type=0, tree=None):
        super().__init__(type=type)
        self.val = None
        self.setChildIndicatorPolicy(self.ChildIndicatorPolicy.ShowIndicator)
        self.data_role = Qt.ItemDataRole.UserRole
        self.tree = tree

    def set_top(self, path, icon):
        self.set_icon(icon)
        self.setText(1, path)

    def set_icon(self, path):
        icon = QIcon(path)
        self.setIcon(0, icon)

    def set_val(self, value):
        self.val = value
        self.set_icon("./assets/percentage.png")
        self.setText(1, f"Piece Patial Match: {value}")
        progressbar = Progress()
        progressbar.setRange(0,100)
        progressbar.setValue(value)
        self.tree.setItemWidget(self, 2, progressbar)


class Progress(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setRange(0, 100)
        self.setValue(0)
        # self.setStyleSheet(progr6essbarSheet)

class CallbackThread(QThread):
    callbackActivated = pyqtSignal()



class TreeWidget(QTreeWidget):
    """Tree Widget for the `Check` tab.

    Displays percentages for matching files and their progress.

    Args:
        parent(`QWidget`, default=None)
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.window = parent.window
        self.setStyleSheet(treeSheet + headerSheet)
        self.setColumnCount(3)
        self.setIndentation(10)
        header = self.header()
        header.setSectionResizeMode(0, header.ResizeMode.ResizeToContents)
        # self.setHeaderHidden(True)
        self.root = None
        self.total = None
        self.itemWidgets = {}

    def setRoot(self, root):
        self.root = os.path.split(root)[0]

    def perform_action(self):
        for _, value in self.itemWidgets.items():
            self.update_progress(value)

    def update_progress(self, value):
        widget = value["widget"]
        children = value["children"]
        tally = total = 0
        for child in children:
            tally += child.val
            total += 100
        percent = int((tally / total) * 100)
        self.removeItemWidget(widget, 2)
        progressbar = Progress(parent=None)
        progressbar.setValue(percent)
        self.setItemWidget(widget, 2, progressbar)

    def add_top_item(self, path):
        item = TreePieceItem(type=0, tree=self)
        item.set_top(path, "./assets/file.png")
        self.itemWidgets[path] = {"widget": item, "children": []}
        self.addTopLevelItem(item)
        progressbar = Progress()
        self.setItemWidget(item, 2, progressbar)

    def callback(self, response, path, size, total):
        if path.startswith(self.root):
            path = path.strip(self.root)
        if self.total is None:
            self.total = total
        if path not in self.itemWidgets:
            self.add_top_item(path)
        item = self.itemWidgets[path]["widget"]
        children = self.itemWidgets[path]["children"]
        item2 = TreePieceItem(type=0, tree=self)
        item.addChild(item2)
        if not response:
            amount = 0
        else:
            amount = 100
        item2.set_val(amount)
        children.append(item2)
        self.window.update()
        self.window.repaint()



class LogTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.setBackgroundVisible(True)
        font = self.font()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setPointSize(11)
        self.setFont(font)
        self.setStyleSheet(logTextEditSheet)

    def callback(self, msg):
        self.insertPlainText(msg)
        self.insertPlainText("\n\n")
