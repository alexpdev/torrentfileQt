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
import math
import os
import re
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QTextOption
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPlainTextEdit,
                               QProgressBar, QPushButton, QSplitter,
                               QTreeWidget, QTreeWidgetItem, QVBoxLayout,
                               QWidget)
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
        mainLabel = QLabel("Torrent Checker")
        mainLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLabel.setObjectName("checkMainLabel")
        self.centralLayout.addWidget(mainLabel)
        self.centralLayout.addWidget(self.centralWidget)
        self.centralWidget.setObjectName("CheckCentralWidget")
        self.layout = QVBoxLayout(self.centralWidget)
        self.hlayout = QHBoxLayout()

        self.file_group = DropGroupBox(parent=self)
        self.file_group.setLabelText("drag & drop torrent file here or...")
        self.file_group.setTitle("Torrent File")
        self.file_button = BrowseTorrents(parent=self)
        self.file_button.torrentSelected.connect(self.setTorrent)
        self.file_group.addButton(self.file_button)
        self.file_group.pathSelected.connect(self.setTorrent)
        self.hlayout.addWidget(self.file_group)
        self.layout.addLayout(self.hlayout)

        self.content_group = DropGroupBox(parent=self)
        self.content_group.setLabelText("drag & drop search folder here or...")
        self.content_group.setTitle("Content Search Folder")
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
        self.checkButton.ready.connect(self.populate_tree)
        self.layout.addWidget(self.checkButton)

    def setPath(self, path):
        self.content_group.setPath(path)

    def setTorrent(self, path):
        self.file_group.setPath(path)

    def populate_tree(self, metafile, content):
        self.thread = RecheckThread(metafile, content)
        base = self.content_group.getPath()
        self.thread.finished.connect(self.thread.deleteLater)
        self.treeWidget.set_thread_info(self.thread, base)
        self.thread.start()


class RecheckThread(QThread):
    """Piece Hasher class for iterating through captured torrent pieces."""

    path_ready = Signal(str, int)
    finished = Signal()
    progress_update = Signal(str, int)

    def __init__(self, metafile, content):
        """Construct for PieceHasher class."""
        super().__init__()
        self.metafile = metafile
        self.content = content
        self.current = 0

    def get_path_information(self, fileinfo, pathlist):
        """Add tree widgets items to tree widget."""
        for _, val in fileinfo.items():
            if val["path"] == self.root:
                relpath = os.path.dirname(self.root)
            else:
                relpath = os.path.relpath(val["path"], self.root)
            length = val["length"]
            self.path_ready.emit(relpath, length)

    def iter_hashes(self, checker):
        """Iterate through hashes and compare to torrentfile hashes."""
        for actual, expected, path, size in checker.iter_hashes():
            if checker.meta_version == 1:
                self.process_v1_hash(actual, expected, path, size)
            else:
                if actual == expected:
                    self.progress_update.emit(path, size)
                else:
                    self.progress_update.emit(path, size)

    def process_v1_hash(self, actual, expected, path, size):
        while size > 0:
            if self.current >= len(self.pathlist):
                return
            current = self.pathlist[self.current]
            current_length = self.fileinfo.get(current)["length"]
            if current_length == 0:
                self.current += 1
                continue
            if size > current_length:
                size -= current_length
                self.fileinfo[current]["length"] = 0
                if actual == expected:
                    self.progress_update.emit(current, current_length)
            else:
                if actual == expected:
                    self.progress_update.emit(current, size)
                self.fileinfo[current]["length"] -= size
                size = 0

    def run(self):
        checker = Checker(self.metafile, self.content)
        self.root = os.path.dirname(checker.root)
        fileinfo = checker.fileinfo
        self.pathlist = checker.paths
        self.fileinfo = {v["path"]: v for v in fileinfo.values()}
        self.get_path_information(fileinfo, self.pathlist)
        self.iter_hashes(checker)


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

    ready = Signal(str, str)

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
        metafile = parent.file_group.getPath()
        content = parent.content_group.getPath()
        if os.path.exists(metafile):
            if not os.path.isfile(metafile):
                self.window().statusBar().showMessage(
                    "Error: Torrent File cannot be a directory.", 8000)
                return
            parent.treeWidget.clear()
            parent.textEdit.clear()
            Checker.register_callback(parent.textEdit.callback)
            self.ready.emit(metafile, content)
        else:
            self.window().statusBar().showMessage(
                "Error: Torrent File Not Found.", 3000)


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
        path = browse_torrent(self)
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

    def browse_files(self):
        """
        Browse Action performed when user presses button.
        """
        path = browse_files(self)
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


class TreeWidget(QTreeWidget):
    """
    Tree Widget for the `Check` tab.

    Displays percentages for matching files and their progress.

    Parameters
    ----------
    parent : QWidget
        this widgets parent.
    """

    def __init__(self, parent=None):
        """Construct for Tree Widget."""
        super().__init__(parent=parent)
        self.setObjectName("checkTree")
        self.setColumnCount(2)
        self.setIndentation(12)
        header = self.header()
        header.setSizeAdjustPolicy(header.SizeAdjustPolicy.AdjustToContents)
        header.setSectionResizeMode(0, header.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)
        self.setHeaderLabels(["Path", "Progress"])
        self.setHeaderHidden(False)
        self.rootitem = self.invisibleRootItem()
        self.rootitem.setExpanded(True)
        self.progbars = []
        self.thread = None
        self.icons = {
            "video": get_icon("video"),
            "archive": get_icon("archive"),
            "file": get_icon("file"),
            "music": get_icon("music"),
            "folder": get_icon("folder"),
        }
        self.registry = {}

    def set_thread_info(self, thread, base):
        self.thread = thread
        self.base = os.path.dirname(base)
        self.thread.path_ready.connect(self.setup_path_item)
        self.thread.progress_update.connect(self.update_progress)

    def clear(self):
        """Remove any objects from Tree Widget."""
        super().clear()
        self.root = None

    def new_item(self, text, icon, parent):
        item = QTreeWidgetItem()
        item.setText(0, text)
        item.setIcon(0, icon)
        parent.addChild(item)
        parent.setExpanded(True)
        return item

    def setup_path_item(self, path, size):
        """Add branch to tree."""
        parts = list(Path(path).parts)
        root = self.rootitem
        part = parts.pop(0)
        subpath = part
        while subpath in self.registry:
            part = parts.pop(0)
            root = subpath
            subpath = os.path.join(subpath, part)
        root = root if root == self.rootitem else self.registry[root]
        while parts:
            item = self.new_item(part, self.icons["folder"], root)
            self.registry[subpath] = item
            root = item
            part = parts.pop(0)
            subpath = os.path.join(subpath, part)
        fileicon = self.match_suffix_to_icon(Path(path))
        item = self.new_item(part, fileicon, root)
        self.registry[subpath] = item
        progressBar = QProgressBar(self)
        if size < 1 << 30:
            progressBar._total = size
            progressBar._divisor = 1
            progressBar._max = size
        else:
            progressBar._total = size
            progressBar._divisor = 1 << 10
            progressBar._max = progressBar._total // progressBar._divisor
        progressBar.setRange(0, progressBar._max - 1)
        item.progbar = progressBar
        self.progbars.append(progressBar)
        self.setItemWidget(item, 1, progressBar)

    def match_suffix_to_icon(self, path):
        if path.suffix in [".avi", ".mp4", ".mkv", ".mov"]:
            fileicon = self.icons["video"]
        elif path.suffix in [".rar", ".zip", ".7z", ".tar", ".gz"]:
            fileicon = self.icons["archive"]
        elif re.match(r"\.r\d+$", path.suffix):
            fileicon = self.icons["archive"]
        elif path.suffix in [".mp3", ".wav", ".flac", ".m4a"]:
            fileicon = self.icons["music"]
        else:
            fileicon = self.icons["file"]
        return fileicon

    def update_progress(self, path, amount):
        relpath = os.path.relpath(path, self.base)
        item = self.registry[relpath]
        prog = self.itemWidget(item, 1)
        value = prog.value()
        divisor = prog._divisor
        increment = math.ceil(amount / divisor)
        if value + increment > prog._max:
            increment -= prog._max - value + increment
        prog.setValue(value + increment)
