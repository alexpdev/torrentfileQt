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
from PySide6.QtGui import QIcon, QTextOption
from PySide6.QtWidgets import (QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPlainTextEdit, QProgressBar, QPushButton,
                               QSplitter, QTreeWidget, QTreeWidgetItem,
                               QVBoxLayout, QWidget)
from torrentfile.recheck import Checker

from torrentfileQt.utils import (browse_files, browse_folder, browse_torrent,
                                 get_icon)


class CheckWidget(QWidget):
    """Check tab widget for QMainWindow."""

    def __init__(self, parent=None):
        """Construct for check tab."""
        super().__init__(parent=parent)
        self.window = parent.window
        self.vlayout = QVBoxLayout()
        self.layout = QFormLayout()
        self.setLayout(self.vlayout)
        self.vlayout.addLayout(self.layout)
        self.splitter = QSplitter(parent=self)
        self.vlayout.addWidget(self.splitter)

        self.hlayout1 = QHBoxLayout()
        self.hlayout2 = QHBoxLayout()

        self.fileLabel = QLabel("Torrent File", parent=self)
        self.fileLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.fileInput = QLineEdit(parent=self)
        self.browseButton1 = BrowseTorrents(parent=self)

        self.searchLabel = QLabel("Search Path", parent=self)
        self.searchLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.searchInput = QLineEdit(parent=self)
        self.browseButton2 = BrowseFolders(parent=self)
        self.browseButton3 = BrowseFiles(parent=self)
        self.checkButton = ReCheckButton("Check", parent=self)

        self.hlayout1.addWidget(self.fileInput)
        self.hlayout1.addWidget(self.browseButton1)
        self.hlayout2.addWidget(self.searchInput)
        self.hlayout2.addWidget(self.browseButton2)
        self.hlayout2.addWidget(self.browseButton3)

        labelRole = QFormLayout.ItemRole.LabelRole
        fieldRole = QFormLayout.ItemRole.FieldRole
        self.layout.setWidget(1, labelRole, self.fileLabel)
        self.layout.setLayout(1, fieldRole, self.hlayout1)
        self.layout.setWidget(2, labelRole, self.searchLabel)
        self.layout.setLayout(2, fieldRole, self.hlayout2)
        self.textEdit = LogTextEdit(parent=self)
        self.treeWidget = TreeWidget(parent=self)
        self.splitter.addWidget(self.treeWidget)
        self.splitter.addWidget(self.textEdit)
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.vlayout.addWidget(self.checkButton)

        self.layout.setObjectName("CheckWidget_layout")
        self.hlayout1.setObjectName("CheckWidget_hlayout1")
        self.hlayout2.setObjectName("CheckWidget_hlayout2")
        self.browseButton2.setObjectName("CheckWidget_browseButton2")
        self.browseButton1.setObjectName("CheckWidget_browseButton1")
        self.fileLabel.setObjectName("CheckWidget_fileLabel")
        self.searchLabel.setObjectName("CheckWidget_searchLabel")
        self.fileInput.setObjectName("CheckWidget_fileInput")
        self.searchInput.setObjectName("CheckWidget_searchInput")
        self.textEdit.setObjectName("CheckWidget_textEdit")
        self.treeWidget.setObjectName("CheckWidget_treeWidget")
        self.splitter.setObjectName("CheckWidget_splitter")


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
        self.widget = parent
        self.window = parent.window
        self.clicked.connect(self.submit)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def submit(self):
        """Submit data to piece hasher."""
        tree = self.widget.treeWidget
        tree.clear()
        textEdit = self.widget.textEdit
        textEdit.clear()
        searchInput = self.widget.searchInput
        fileInput = self.widget.fileInput
        metafile = fileInput.text()
        content = searchInput.text()
        if os.path.exists(metafile):
            Checker.register_callback(textEdit.callback)
            logging.debug("Registering Callback, setting root")
            tree.reChecking.emit(metafile, content)


class BrowseTorrents(QPushButton):
    """
    BrowseButton ToolButton for activating filebrowser.

    Parameters
    ----------
    parent : widget
        Parent widget.
    """

    def __init__(self, parent=None):
        """Construct Toolbar Button for selecting .torrentfile to check."""
        super().__init__(parent=parent)
        self.setText("File")
        self.setIcon(QIcon(get_icon("browse_file")))
        self.window = parent
        self.setProperty("createButton", "true")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.browse)

    def browse(self, path=None):
        """
        Browse action performed when user presses button.

        Returns
        -------
        path : str
            Path to file or folder to include in torrent.
        """
        path = browse_torrent(self, path)
        self.parent().fileInput.clear()
        self.parent().fileInput.setText(path)


class BrowseFolders(QPushButton):
    """
    Browse Folders ToolButton for activating filedialog.

    Parameters
    ----------
    parent : QWidget
        Widget this widget is the child of.
    """

    def __init__(self, parent=None):
        """Construct a BrowseFolders Button Widget."""
        super().__init__(parent=parent)
        self.window = parent.window
        self.widget = parent
        self.setText("Folder")
        self.setProperty("createButton", "true")
        self.setIcon(QIcon(get_icon("browse_folder")))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.browse_folders)

    def browse_folders(self, path=None):
        """
        Browse Action performed when user presses button.
        """
        path = browse_folder(self, path)
        self.widget.searchInput.clear()
        self.widget.searchInput.setText(path)


class BrowseFiles(QPushButton):
    """Browse file system to find the correct file."""

    def __init__(self, parent=None):
        """Construct a BrowseFolders Button Widget."""
        super().__init__(parent=parent)
        self.window = parent.window
        self.widget = parent
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setText("File")
        self.setProperty("createButton", "true")
        self.setIcon(QIcon(get_icon("browse_file")))
        self.clicked.connect(self.browse_files)

    def browse_files(self, path=None):  # pragma: nocover
        """
        Browse Action performed when user presses button.
        """
        path = browse_files(self, path)
        self.widget.searchInput.clear()
        self.widget.searchInput.setText(path)


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
        self.setChildIndicatorPolicy(policy)
        self.tree = tree
        self.window = tree.window
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
        self.window.app.processEvents()
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

    valueChanged = Signal([int])

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
            val = val // (2**20)
        elif self.total > 10_000:
            val = val // (2**10)
        return val

    def addValue(self, value):
        """Increase value of progressbar."""
        self.blockSignals(True)
        currentvalue = self.value()
        out = self.normalize(value)
        addedVal = currentvalue + out
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

    addPathChild = Signal([str, str])
    reChecking = Signal([str, str])
    addValue = Signal([str, int])
    addCount = Signal([str, int])

    def __init__(self, parent=None):
        """Construct for Tree Widget."""
        super().__init__(parent=parent)
        self.window = parent.window
        self.setColumnCount(2)
        self.setIndentation(12)
        self.item = self.invisibleRootItem()
        self.item.setExpanded(True)
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
        self.item_tree = {"widget": self.item}
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
                    fileicon = QIcon(get_icon("video"))
                elif path.suffix in [".rar", ".zip", ".7z", ".tar", ".gz"]:
                    fileicon = QIcon(get_icon("archive"))
                elif re.match(r"\.r\d+$", path.suffix):
                    fileicon = QIcon(get_icon("archive"))
                elif path.suffix in [".mp3", ".wav", ".flac", ".m4a"]:
                    fileicon = QIcon(get_icon("music"))
                else:
                    fileicon = QIcon(get_icon("file"))
                progressBar = ProgressBar(parent=None, size=size)
                self.setItemWidget(item, 1, progressBar)
                item.progbar = progressBar
                self.itemWidgets[str(path)] = item
            else:
                fileicon = QIcon(get_icon("folder"))
            item.setIcon(0, fileicon)
            item.setText(0, partial)
            item_tree = item_tree[partial]
            self.window.app.processEvents()
        self.paths.append(path)


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
