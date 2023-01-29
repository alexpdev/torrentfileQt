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
"""Module for the Check Tab Widget."""

import logging
import os
import re
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QTextOption
from PySide6.QtWidgets import (QPlainTextEdit, QProgressBar, QPushButton,
                               QSplitter, QTreeWidget, QTreeWidgetItem,
                               QVBoxLayout, QWidget, QHBoxLayout, QApplication)
from torrentfile.recheck import Checker

from torrentfileQt.utils import (browse_files, browse_folder, browse_torrent,
                                 get_icon)

from torrentfileQt.widgets import DropGroupBox

class CheckWidget(QWidget):
    """Check tab widget for QMainWindow."""

    def __init__(self, parent=None):
        """Construct for check tab."""
        super().__init__(parent=parent)
        self.setObjectName("checkTab")
        self.setAcceptDrops(True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.centralWidget = QWidget(parent=self)
        self.centralLayout = QVBoxLayout(self)
        self.centralLayout.addWidget(self.centralWidget)
        self.centralWidget.setObjectName("CheckCentralWidget")
        self.layout = QVBoxLayout(self.centralWidget)
        self.hlayout = QHBoxLayout()

        self.file_group = DropGroupBox(parent=self)
        self.file_group.setLabelText("drop torrent file here")
        self.file_button = BrowseTorrents(parent=self)
        self.file_button.torrentSelected.connect(self.setTorrent)
        self.file_group.addButton(self.file_button)
        self.file_group.pathSelected.connect(self.setTorrent)
        self.hlayout.addWidget(self.file_group)
        self.layout.addLayout(self.hlayout)

        self.content_group = DropGroupBox(parent=self)
        self.content_group.setLabelText("drop search folder here")
        self.content_folders = BrowseFolders(parent=self)
        self.content_folders.folderSelected.connect(self.setPath)
        self.content_files = BrowseFiles(parent=self)
        self.content_files.filesSelected.connect(self.setPath)
        self.content_group.addButton(self.content_files)
        self.content_group.addButton(self.content_folders)
        self.content_group.pathSelected.connect(self.setPath)
        self.hlayout.addWidget(self.content_group)

        self.treeWidget = TreeWidget(parent=self)
        self.textEdit = LogTextEdit(parent=self)
        self.splitter = QSplitter(parent=self)
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.addWidget(self.treeWidget)
        self.splitter.addWidget(self.textEdit)
        self.layout.addWidget(self.splitter)

        self.checkButton = ReCheckButton("Check", parent=self)
        self.layout.addWidget(self.checkButton)

    def setPath(self, path):
        self.content_group.setLabelText(path)

    def setTorrent(self, path):
        self.file_group.setLabelText(path)


class ReCheckButton(QPushButton):
    """
    Button Widget for validating torrent files against downloaded contents.

    Parameters
    ----------
    text : str
        The text displayed on the button itself.
    parent : QWidget
        This widgets parent widget.
    """

    process = None

    def __init__(self, text, parent=None):
        """Construct the CheckButton Widget."""
        super().__init__(text, parent=parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("RecheckButton")
        self._parent = parent
        self.clicked.connect(self.submit)

    def submit(self):
        """Submit data to piece hasher."""
        parent = self._parent
        parent.treeWidget.clear()
        parent.textEdit.clear()
        QApplication.instance().processEvents()
        metafile = parent.file_group.getLabelText()
        content = parent.content_group.getLabelText()
        self.window().statusBar().showMessage("Checking...", 3000)
        if os.path.exists(metafile):
            Checker.register_callback(parent.textEdit.callback)
            logging.debug("Registering Callback, setting root")
            parent.treeWidget.reChecking.emit(metafile, content)


class BrowseTorrents(QPushButton):
    """
    BrowseButton ToolButton for activating filebrowser.

    Parameters
    ----------
    parent : widget
        Parent widget.
    """

    torrentSelected = Signal(str)

    def __init__(self, parent=None):
        """Construct Toolbar Button for selecting .torrentfile to check."""
        super().__init__(parent=parent)
        self.setText("Select Torrent File")
        self.setIcon(get_icon("browse_file"))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.browse)

    def browse(self):
        """
        Browse action performed when user presses button.

        Returns
        -------
        path : str
            Path to file or folder to include in torrent.
        """
        path = browse_torrent(self, path)
        self.torrentSelected.emit(path)


class BrowseFolders(QPushButton):
    """
    Browse Folders ToolButton for activating filedialog.

    Parameters
    ----------
    parent : QWidget
        Widget this widget is the child of.
    """

    folderSelected = Signal(str)

    def __init__(self, parent=None):
        """Construct a BrowseFolders Button Widget."""
        super().__init__(parent=parent)
        self.setText("Select Folder")
        self.setIcon(get_icon("browse_folder"))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.browse_folders)

    def browse_folders(self):
        """
        Browse Action performed when user presses button.
        """
        path = browse_folder(self)
        self.folderSelected.emit(path)


class BrowseFiles(QPushButton):
    """Browse file system to find the correct file."""

    filesSelected = Signal(str)

    def __init__(self, parent=None):
        """Construct a BrowseFolders Button Widget."""
        super().__init__(parent=parent)
        self.setText("Select File")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setIcon(get_icon("browse_file"))
        self.clicked.connect(self.browse_files)

    def browse_files(self, paths=None):  # pragma: nocover
        """
        Browse Action performed when user presses button.
        """
        path = browse_files(self, paths)
        self.filesSelected.emit(path)


class LogTextEdit(QPlainTextEdit):
    """Text Edit widget for check tab."""

    def __init__(self, parent=None):
        """Construct for LogTextEdit."""
        super().__init__(parent=parent)
        self._parent = parent
        self.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
        self.setBackgroundVisible(True)
        font = self.font()
        font.setFamily("Consolas")
        font.setBold(True)
        self.setFont(font)

    def clear_data(self):
        """Remove any text."""
        self.clear()

    def callback(self, msg):
        """Invoke function for CheckerClass."""
        self.insertPlainText(msg)
        self.insertPlainText("\n")
        vertscroll = self.verticalScrollBar()
        vertscroll.triggerAction(vertscroll.SliderAction.SliderToMaximum)

    def sizeHint(self):
        """Return the widget's size hint."""
        hint = super().sizeHint()
        hint.setHeight(hint.height() // 4)
        return hint


class TreePieceItem(QTreeWidgetItem):
    """Item Widgets that are leafs to Tree Widget branches."""

    def __init__(self, type=0, tree=None):
        """Construct for tree widget items."""
        super().__init__(type=type)
        policy = self.ChildIndicatorPolicy.DontShowIndicatorWhenChildless
        self.app = QApplication.instance()
        self.setChildIndicatorPolicy(policy)
        self.tree = tree
        self.counted = self.value = 0
        self.progbar = None

    @property
    def total(self):
        """Return current value of progress bar."""
        return self.progbar.total

    @property
    def left(self):
        """Discard amount of data left to check."""
        return self.progbar.total - self.counted

    def addProgress(self, value):
        """Increase progress bar value."""
        if self.counted + value > self.total:
            consumed = self.total - self.value  # pragma: no cover
        else:
            consumed = value
        self.value += consumed
        self.counted += consumed
        self.progbar.valueChanged.emit(consumed)
        self.app.processEvents()
        return consumed

    def count(self, value):
        """Increase count without increasing value."""
        if self.counted + value > self.total:
            consumed = self.total - self.value
            self.counted += consumed
            return consumed
        self.counted += value
        return value


class ProgressBar(QProgressBar):
    """Progress Bar Widget."""

    valueChanged = Signal(int)

    def __init__(self, parent=None, size=0):
        """Construct for the progress bar widget."""
        super().__init__(parent=parent)
        self.total = size
        self.setValue(0)
        size = self.normalize(size)
        self.setRange(0, size)
        self.valueChanged.connect(self.addValue)

    def normalize(self, val):
        """Convert larger values into smaller increments."""
        if self.total > 10_000_000:
            val = val / (2**20)
        elif self.total > 10_000:
            val = val / (2**10)
        return val

    def addValue(self, value):
        """Increase value of progressbar."""
        self.blockSignals(True)
        currentvalue = self.value()
        out = self.normalize(value)
        addedVal = currentvalue + value
        self.setValue(addedVal)
        self.blockSignals(False)


class TreeWidget(QTreeWidget):
    """
    Tree Widget for the `Check` tab.

    Displays percentages for matching files and their progress.

    Parameters
    ----------
    parent : QWidget
        this widgets parent.
    """

    addPathChild = Signal(str, str)
    reChecking = Signal(str, str)
    addValue = Signal(str, int)
    addCount = Signal(str, int)

    def __init__(self, parent=None):
        """Construct for Tree Widget."""
        super().__init__(parent=parent)
        self.app = QApplication.instance()
        self.setColumnCount(2)
        self.setIndentation(12)
        self.rootitem = self.invisibleRootItem()
        self.rootitem.setExpanded(True)
        header = self.header()
        header.setSizeAdjustPolicy(header.SizeAdjustPolicy.AdjustToContents)
        header.setSectionResizeMode(0, header.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, header.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)
        self.setHeaderLabels(["Path", "Progress"])
        self.setHeaderHidden(False)
        self.itemWidgets = {}
        self.paths = []
        self.total = 0
        self.root = None
        self.piece_length = None
        self.item_tree = {"widget": self.rootitem}
        self.addPathChild.connect(self.add_path_child)
        self.reChecking.connect(self.get_hashes)
        self.addValue.connect(self.setItemValue)
        self.addCount.connect(self.setItemCount)

    def setItemValue(self, path, val):
        """Set child widgets value to val."""
        widget = self.itemWidgets[path]
        widget.addProgress(val)

    def setItemCount(self, path, val):
        """Set child widgets count to val."""
        widget = self.itemWidgets[path]
        widget.count(val)

    def get_hashes(self, metafile, contents):
        """Fill tree widget with contents of torrentfile."""
        phashes = PieceHasher(metafile, contents, self)
        phashes.addTreeWidgets()
        phashes.iter_hashes()
        self.window().statusBar().showMessage("Complete", 2000)

    def clear(self):
        """Remove any objects from Tree Widget."""
        super().clear()
        self.item_tree = {"widget": self.invisibleRootItem()}
        self.itemWidgets = {}
        self.paths = []
        self.root = None

    def add_path_child(self, path, size):
        """Add branch to tree."""
        path = Path(path)
        size = int(size)
        partials = path.parts
        item, item_tree = None, self.item_tree
        for i, partial in enumerate(partials):
            if partial in item_tree:
                item_tree = item_tree[partial]
                continue
            parent = item_tree["widget"]
            item = TreePieceItem(0, tree=self)
            parent.addChild(item)
            parent.setExpanded(True)
            item_tree[partial] = {"widget": item}
            if i == len(partials) - 1:
                if path.suffix in [".avi", ".mp4", ".mkv", ".mov"]:
                    fileicon = get_icon("video")
                elif path.suffix in [".rar", ".zip", ".7z", ".tar", ".gz"]:
                    fileicon = get_icon("archive")
                elif re.match(r"\.r\d+$", path.suffix):
                    fileicon = get_icon("archive")
                elif path.suffix in [".mp3", ".wav", ".flac", ".m4a"]:
                    fileicon = get_icon("music")
                else:
                    fileicon = get_icon("file")
                progressBar = ProgressBar(parent=None, size=size)
                self.setItemWidget(item, 1, progressBar)
                item.progbar = progressBar
                self.itemWidgets[str(path)] = item
            else:
                fileicon = get_icon("folder")
            item.setIcon(0, fileicon)
            item.setText(0, partial)
            item_tree = item_tree[partial]
            self.app.processEvents()
        self.paths.append(path)
        self.window().statusBar().showMessage("Checking...")



class PieceHasher:
    """Piece Hasher class for iterating through captured torrent pieces."""

    def __init__(self, metafile, content, tree):
        """Construct for PieceHasher class."""
        self.metafile = metafile
        self.content = content
        self.tree = tree
        self.checker = Checker(metafile, content)
        self.root = os.path.dirname(self.checker.root)
        self.fileinfo = self.checker.fileinfo
        self.pathlist = self.checker.paths
        self.current = 0

    def addTreeWidgets(self):
        """Add tree widgets items to tree widget."""
        for _, val in self.fileinfo.items():
            if val["path"] == self.root:
                relpath = os.path.dirname(self.root)  # pragma: no cover
            else:
                relpath = os.path.relpath(val["path"], self.root)
            length = val["length"]
            self.tree.addPathChild.emit(relpath, str(length))

    def iter_hashes(self):
        """Iterate through hashes and compare to torrentfile hashes."""
        for actual, expected, path, size in self.checker.iter_hashes():
            if self.checker.meta_version == 1:
                while size > 0:
                    if self.current >= len(self.pathlist):
                        break  # pragma: no cover
                    current = self.pathlist[self.current]
                    relpath = os.path.relpath(current, self.root)
                    widget = self.tree.itemWidgets[relpath]
                    if widget.left == 0:
                        self.current += 1
                        continue
                    left, amount = widget.left, None
                    if actual == expected:
                        amount = left if left < size else size
                        self.tree.addValue.emit(relpath, amount)
                    else:
                        amount = left if left < size else size
                        self.tree.addCount.emit(relpath, amount)
                    size -= amount
            else:
                if path == self.root:
                    relpath = os.path.dirname(self.root)  # pragma: no cover
                else:
                    relpath = os.path.relpath(path, self.root)
                if actual == expected:
                    self.tree.addValue.emit(relpath, size)
                else:
                    self.tree.addCount.emit(relpath, size)
