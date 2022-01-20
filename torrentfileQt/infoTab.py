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
"""Widgets and procedures for the "Torrent Info" tab."""

import math
import os
import re
from datetime import datetime
from pathlib import Path

import pyben
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QFileDialog, QGridLayout, QLabel, QLineEdit,
                               QPushButton, QTreeWidget, QTreeWidgetItem,
                               QWidget)

from torrentfileQt.qss import infoLineEdit

ASSETS = os.environ["ASSETS"]


class TreeWidget(QTreeWidget):
    """Tree view of the directory structure cataloged in .torrent file.

    Args:
        parent (`widget`, default=`None`): The widget containing this widget.
    """

    itemReady = Signal([str, str])

    def __init__(self, parent=None):
        """Constructor for tree widget."""
        super().__init__(parent=parent)
        self.window = parent.window
        self.widget = parent
        self.root = self.invisibleRootItem()
        header = self.header()
        header.setSectionResizeMode(0, header.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, header.ResizeMode.ResizeToContents)
        self.root.setChildIndicatorPolicy(
            self.root.ChildIndicatorPolicy.ShowIndicator
        )
        self.setIndentation(8)
        self.setEditTriggers(self.EditTrigger.NoEditTriggers)
        self.setHeaderHidden(True)
        self.setItemsExpandable(True)
        self.setColumnCount(2)
        self.itemtree = {"widget": self.root}
        self.itemReady.connect(self.apply_value)

    def apply_value(self, text, length):
        """Add path partials and file lengths to tree branches."""
        length = int(length)
        partials = Path(text).parts
        tree = self.itemtree
        for i, partial in enumerate(partials):
            if partial not in tree:
                item = TreeItem(0)
                if i + 1 == len(partials):
                    _, suffix = os.path.splitext(partial)
                    if suffix in [".mp4", ".mkv"]:
                        iconpath = os.path.join(ASSETS, "icons", "video.png")
                    elif suffix in [".rar", ".zip", ".7z", ".tar", ".gz"]:
                        iconpath = os.path.join(ASSETS, "icons", "archive.png")
                    elif re.match(r"\.r\d+", suffix):
                        iconpath = os.path.join(ASSETS, "icons", "archive.png")
                    elif suffix in [".wav", ".mp3", ".flac", ".m4a", ".aac"]:
                        iconpath = os.path.join(ASSETS, "icons", "music.png")
                    else:
                        iconpath = os.path.join(ASSETS, "icons", "file.png")
                    item.setLength(length)
                else:
                    iconpath = os.path.join(ASSETS, "icons", "folder.png")
                icon = QIcon(iconpath)
                item.setIcon(0, icon)
                item.setText(1, partial)
                tree["widget"].addChild(item)
                item.setExpanded(True)
                tree[partial] = {"widget": item}
            tree = tree[partial]


class TreeItem(QTreeWidgetItem):
    """Item widget for tree leaves and branches."""

    def __init__(self, group):
        """Constructor for tree item widget."""
        super().__init__(group)
        policy = self.ChildIndicatorPolicy.DontShowIndicatorWhenChildless
        self.setChildIndicatorPolicy(policy)

    def setLength(self, length):
        """Set length leaf for tree branches."""
        child = TreeItem(0)
        icon = QIcon(os.path.join(ASSETS, "icons", "scale.png"))
        child.setIcon(0, icon)
        child.setText(1, f"Size: {length} (bytes)")
        self.setExpanded(True)
        self.addChild(child)


class InfoWidget(QWidget):
    """Main parent widget for the Torrent Info tab."""

    def __init__(self, parent=None):
        """Construct and organize Torrent info tab."""
        super().__init__(parent=parent)
        self.window = parent.window
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Labels
        self.pathLabel = Label("Path: ", parent=self)
        self.nameLabel = Label("Name: ", parent=self)
        self.pieceLengthLabel = Label("Piece Length: ", parent=self)
        self.sizeLabel = Label("Total Size: ", parent=self)
        self.totalPiecesLabel = Label("Total Pieces: ", parent=self)
        self.trackerLabel = Label("Tracker: ", parent=self)
        self.privateLabel = Label("Private: ", parent=self)
        self.sourceLabel = Label("Source: ", parent=self)
        self.commentLabel = Label("Comment: ", parent=self)
        self.metaVersionLabel = Label("Meta-Version:", parent=self)
        self.dateCreatedLabel = Label("Creation Date: ", parent=self)
        self.createdByLabel = Label("Created By: ", parent=self)
        self.contentsLabel = Label("Contents: ", parent=self)
        self.contentsTree = TreeWidget(parent=self)
        self.sourceEdit = InfoLineEdit(parent=self)
        self.metaVersionEdit = InfoLineEdit(parent=self)
        self.pathEdit = InfoLineEdit(parent=self)
        self.nameEdit = InfoLineEdit(parent=self)
        self.pieceLengthEdit = InfoLineEdit(parent=self)
        self.sizeEdit = InfoLineEdit(parent=self)
        self.privateEdit = InfoLineEdit(parent=self)
        self.commentEdit = InfoLineEdit(parent=self)
        self.trackerEdit = InfoLineEdit(parent=self)
        self.totalPiecesEdit = InfoLineEdit(parent=self)
        self.dateCreatedEdit = InfoLineEdit(parent=self)
        self.createdByEdit = InfoLineEdit(parent=self)
        self.layout.addWidget(self.pathLabel, 0, 0, 1, 1)
        self.layout.addWidget(self.pathEdit, 0, 1, 1, -1)
        self.layout.addWidget(self.nameLabel, 1, 0, 1, 1)
        self.layout.addWidget(self.nameEdit, 1, 1, 1, -1)
        self.layout.addWidget(self.sizeLabel, 2, 0, 1, 1)
        self.layout.addWidget(self.sizeEdit, 2, 1, 1, -1)
        self.layout.addWidget(self.pieceLengthLabel, 3, 0, 1, 1)
        self.layout.addWidget(self.pieceLengthEdit, 3, 1, 1, -1)
        self.layout.addWidget(self.totalPiecesLabel, 4, 0, 1, 1)
        self.layout.addWidget(self.totalPiecesEdit, 4, 1, 1, -1)
        self.layout.addWidget(self.trackerLabel, 5, 0, 1, 1)
        self.layout.addWidget(self.trackerEdit, 5, 1, 1, -1)
        self.layout.addWidget(self.metaVersionLabel, 6, 0, 1, 1)
        self.layout.addWidget(self.metaVersionEdit, 6, 1, 1, -1)
        self.layout.addWidget(self.privateLabel, 7, 0, 1, 1)
        self.layout.addWidget(self.privateEdit, 7, 1, 1, -1)
        self.layout.addWidget(self.sourceLabel, 8, 0, 1, 1)
        self.layout.addWidget(self.sourceEdit, 8, 1, 1, -1)
        self.layout.addWidget(self.commentLabel, 9, 0, 1, 1)
        self.layout.addWidget(self.commentEdit, 9, 1, 1, -1)
        self.layout.addWidget(self.createdByLabel, 10, 0, 1, 1)
        self.layout.addWidget(self.createdByEdit, 10, 1, 1, -1)
        self.layout.addWidget(self.dateCreatedLabel, 11, 0, 1, 1)
        self.layout.addWidget(self.dateCreatedEdit, 11, 1, 1, -1)
        self.layout.addWidget(self.contentsLabel, 12, 0, 1, 1)
        self.layout.addWidget(self.contentsTree, 12, 1, 4, -1)
        self.selectButton = SelectButton("Select Torrent", parent=self)
        self.layout.addWidget(self.selectButton, 17, 0, -1, -1)
        self.pathLabel.setObjectName("pathLabel")
        self.pathEdit.setObjectName("pathEdit")
        self.nameLabel.setObjectName("nameLabel")
        self.nameEdit.setObjectName("nameEdit")
        self.sizeLabel.setObjectName("sizeLabel")
        self.sizeEdit.setObjectName("sizeEdit")
        self.pieceLengthLabel.setObjectName("pieceLengthLabel")
        self.pieceLengthEdit.setObjectName("pieceLengthEdit")
        self.totalPiecesLabel.setObjectName("totalPiecesLabel")
        self.totalPiecesEdit.setObjectName("totalPiecesEdit")
        self.trackerLabel.setObjectName("trackerLabel")
        self.trackerEdit.setObjectName("trackerEdit")
        self.metaVersionLabel.setObjectName("metaVersionLabel")
        self.metaVersionEdit.setObjectName("metaVersionEdit")
        self.privateLabel.setObjectName("privateLabel")
        self.privateEdit.setObjectName("privateEdit")
        self.sourceLabel.setObjectName("sourceLabel")
        self.sourceEdit.setObjectName("sourceEdit")
        self.commentLabel.setObjectName("commentLabel")
        self.commentEdit.setObjectName("commentEdit")
        self.createdByLabel.setObjectName("createdByLabel")
        self.createdByEdit.setObjectName("createdByEdit")
        self.dateCreatedLabel.setObjectName("dateCreatedLabel")
        self.dateCreatedEdit.setObjectName("dateCreatedEdit")
        self.contentsLabel.setObjectName("contentsLabel")
        self.contentsTree.setObjectName("contentsTree")

    def fill(self, **kws):
        """Fill all child widgets with collected information.

        Args:
            kws (`dict`): key, value dictionary with keys as field labels.
        """
        self.pathEdit.setText(kws["path"])
        self.nameEdit.setText(kws["name"])
        self.commentEdit.setText(kws["comment"])
        self.trackerEdit.setText("; ".join(kws["announce"]))
        self.sourceEdit.setText(kws["source"])
        self.dateCreatedEdit.setText(str(kws["creation_date"]))
        self.createdByEdit.setText(kws["created_by"])
        self.privateEdit.setText(kws["private"])
        self.metaVersionEdit.setText(str(kws["meta version"]))

        piece_length = kws["piece_length"]
        plength_str = (
            denom(piece_length) + " / (" + pretty_int(piece_length) + ")"
        )
        self.pieceLengthEdit.setText(plength_str)
        size = denom(kws["length"]) + " / (" + pretty_int(kws["length"]) + ")"
        self.sizeEdit.setText(size)
        total_pieces = math.ceil(kws["length"] / kws["piece_length"])
        self.totalPiecesEdit.setText(str(total_pieces))

        for path, size in kws["contents"].items():
            self.contentsTree.itemReady.emit(path, str(size))
        for widg in [
            self.pathEdit,
            self.nameEdit,
            self.trackerEdit,
            self.privateEdit,
            self.pieceLengthEdit,
            self.sizeEdit,
            self.totalPiecesEdit,
        ]:
            widg.setCursorPosition(0)


class SelectButton(QPushButton):
    """Button for choosing the torrent file."""

    def __init__(self, text, parent=None):
        """Constructor for select button."""
        super().__init__(text, parent=parent)
        self.pressed.connect(self.selectTorrent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def selectTorrent(self, path=None):
        """Collect torrent information and send to the screen for display."""
        if not path:  # pragma: no cover
            path, _ = QFileDialog.getOpenFileName(
                parent=self,
                caption="Select '.torrent' file",
                dir=str(Path.home()),
                filter="*.torrent",
                selectedFilter=None,
            )
        if path:
            meta = pyben.load(path)
            info = meta["info"]
            keywords = {}
            keywords["path"] = path
            keywords["piece_length"] = info["piece length"]

            # get meta version
            if "meta version" not in info:
                keywords["meta version"] = 1
            elif "pieces" in info:
                keywords["meta version"] = 3
            else:
                keywords["meta version"] = 2

            # extract creator
            if "created by" in meta:
                keywords["created_by"] = meta["created by"]
            else:
                keywords["created_by"] = ""

            # extract name comment and source
            for kw in ["name", "comment", "source"]:
                if kw in info:
                    keywords[kw] = info[kw]
                else:
                    keywords[kw] = ""

            # extract announce list
            if "announce-list" in meta:
                alst = [url for urlst in meta["announce-list"] for url in urlst]
                keywords["announce"] = alst + [meta["announce"]]
            else:
                keywords["announce"] = [meta["announce"]]

            # iterate through filelist
            size = 0
            if "files" in info:
                contents = {}
                for entry in info["files"]:
                    contents[
                        os.path.join(info["name"], *entry["path"])
                    ] = entry["length"]
                    size += entry["length"]
                keywords["contents"] = contents

            elif "file tree" in info:
                contents = {}
                for k, v in parse_filetree(info["file tree"]).items():
                    contents[os.path.join(info["name"], k)] = v
                    size += v
                keywords["contents"] = contents
            else:
                keywords["contents"] = {info["name"]: info["length"]}
                size = info["length"]

            keywords["length"] = size

            if "creation date" in meta:
                date = datetime.fromtimestamp(meta["creation date"])
                text = date.strftime("%B %d, %Y %H:%M")
                keywords["creation_date"] = text
            else:
                keywords["creation_date"] = ""

            if "private" in info:
                keywords["private"] = "True"
            else:
                keywords["private"] = "False"

            self.parent().fill(**keywords)


class Label(QLabel):
    """Label Identifier for Window Widgets."""

    def __init__(self, text, parent=None):
        """Constructor for Label Widget."""
        super().__init__(text, parent=parent)
        font = self.font()
        font.setBold(True)
        font.setPointSize(11)
        self.setFont(font)


class InfoLineEdit(QLineEdit):
    """Line Edit Widget."""

    def __init__(self, parent=None):
        """Constructor for line edit widget."""
        super().__init__(parent=parent)
        self.setReadOnly(True)
        self.setStyleSheet(infoLineEdit)
        self.setDragEnabled(True)


def denom(num):
    """Determine appropriate denomination for size of file."""
    txt = str(num)
    if int(num) < 1000:
        return txt
    if 1000 <= num <= 999999:
        return "".join([txt[:-3], ".", txt[-3], "KB"])
    if 1_000_000 <= num < 1_000_000_000:
        return "".join([txt[:-6], ".", txt[-6], "MB"])
    return "".join([txt[:-9], ".", txt[-9], "GB"])


def pretty_int(num):
    """Format integer."""
    text, seq = str(num), []
    digits, count = len(text) - 1, 0
    while digits >= 0:
        if count == 3:
            seq.insert(0, ",")
            count = 0
        seq.insert(0, text[digits])
        count += 1
        digits -= 1
    return "".join(seq) + " Bytes"


def parse_filetree(filetree):
    """Iterate through dictionary to create pathstrings."""
    paths = {}
    for key, value in filetree.items():
        if "" in value:
            paths[key] = value[""]["length"]
        else:
            out = parse_filetree(value)
            for k, v in out.items():
                paths[os.path.join(key, k)] = v
    return paths
