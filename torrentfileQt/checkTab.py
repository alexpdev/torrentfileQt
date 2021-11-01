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

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidget,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QToolButton,
    QTreeWidget,
    QTreeWidgetItem,
)
from torrentfile.progress import CheckerClass


from torrentfileQt.qss import (
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
        self.widget = parent
        self.pressed.connect(self.submit)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(pushButtonSheet)
        self.torrent = None
        self.folder = None


    @property
    def textEdit(self):
        return self.widget.textEdit

    @property
    def treeWidget(self):
        return self.widget.treeWidget


    def submit(self):
        self.treeWidget.clear()
        self.textEdit.clear()
        func1 = self.textEdit.callback
        func2 = self.treeWidget.callback
        CheckerClass.register_callbacks(func1, func2)
        self.torrent = self.widget.fileInput.text()
        self.folder = self.widget.searchInput.text()
        self.widget.treeWidget.setRoot(self.folder)
        thread = Thread(group=None, target=self.re_check_torrent)
        thread.run()
        # self.re_check_torrent()

    def re_check_torrent(self):
        checker = CheckerClass(self.torrent, self.folder)
        msg = f"Torrent Contents are {checker.result}% completely downloaded."
        self.textEdit.insertPlainText(msg)
        if self.treeWidget.paths:
            last_path = self.treeWidget.paths[-1]
            value = self.treeWidget.itemWidgets[last_path]
            widget = value["widget"]
            children = value["children"]
            tally = total = 0
            for child in children:
                tally += child.val
                total += 100
            percent = int((tally / total) * 100)
            self.treeWidget.removeItemWidget(widget, 2)
            progressbar = Progress(parent=None)
            progressbar.setValue(percent)
            self.treeWidget.setItemWidget(widget, 2, progressbar)


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
        path = os.path.normpath(path)
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
        path = os.path.normpath(path)
        self.parent().searchInput.clear()
        self.parent().searchInput.setText(path)


class ProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)


class TreePieceItem(QTreeWidgetItem):
    def __init__(self, type=0, tree=None):
        super().__init__(type=type)
        self.val = None
        self.setChildIndicatorPolicy(
            self.ChildIndicatorPolicy.DontShowIndicatorWhenChildless
            )
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

    def __repr__(self):
        return f"<TreeItem: {self.val}>"


class Progress(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setRange(0, 100)
        self.setValue(0)


class TreeWidget(QTreeWidget):
    """Tree Widget for the `Check` tab.

    Displays percentages for matching files and their progress.

    Args:
        parent(`QWidget`, default=None)
    """
    callback_activated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.window = parent.window
        self.setStyleSheet(treeSheet + headerSheet)
        self.setColumnCount(3)
        self.setIndentation(10)
        header = self.header()
        header.setSectionResizeMode(0, header.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, header.ResizeMode.ResizeToContents)
        self.setHeaderHidden(True)
        self.root = None
        self.itemWidgets = {}
        self.paths = []
        self.item_tree = {"widget" : self.invisibleRootItem()}
        self.callback_activated.connect(self.performAction)

    def clear_data(self):
        self.clear()
        self.item_tree = {"widget" : self.invisibleRootItem()}
        self.itemWidgets = {}
        self.paths = []
        self.root = None

    def performAction(self):
        if self.paths:
            last_path = self.paths[-1]
            value = self.itemWidgets[last_path]
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


    def callback(self, response, path, size, total):
        if path.startswith(self.root):
            path = path.strip(self.root)
        if path not in self.itemWidgets:
            temp, partials = path, []
            while True:
                root, base = os.path.split(temp)
                if not base:
                    break
                partials.insert(0,base)
                temp = root
                self.callback_activated.emit()
            item_tree = self.item_tree
            for i, partial in enumerate(partials):
                if partial in item_tree:
                    item_tree = item_tree[partial]
                    continue
                widget = item_tree["widget"]
                item = TreePieceItem(type=0, tree=self)
                item.set_top(partial, "./assets/folder.png")
                widget.addChild(item)
                item_tree[partial] = {"widget": item}
                if i == len(partials) - 1:
                    progressbar = Progress()
                    self.setItemWidget(item, 2, progressbar)
                    self.itemWidgets[path] = {"children": [], "widget": item}
                item_tree = item_tree[partial]
            self.paths.append(path)
        children = self.itemWidgets[path]["children"]
        widget = self.itemWidgets[path]["widget"]
        item2 = TreePieceItem(type=0, tree=self)
        widget.addChild(item2)
        amount = 0 if not response else 100
        item2.set_val(amount)
        children.append(item2)
        self.window.update()
        self.window.repaint()

    def setRoot(self, root):
        self.root = os.path.split(root)[0]



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

    def clear_data(self):
        self.clear()

    def callback(self, msg):
        self.insertPlainText(msg)
        self.insertPlainText("\n\n")
