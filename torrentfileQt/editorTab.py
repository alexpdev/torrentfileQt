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

import os
# from collections.abc import Mapping, Sequence
from pathlib import Path

import pyben
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QToolButton, QTreeWidget,
                             QTreeWidgetItem, QVBoxLayout, QWidget)

from torrentfileQt.qss import (headerSheet, labelSheet, lineEditSheet,
                               pushButtonSheet, toolButtonSheet, treeSheet)


class EditorWidget(QWidget):
    """Check tab widget for QMainWindow."""

    def __init__(self, parent=None):
        """Constructor for check tab."""
        super().__init__(parent=parent)
        self.window = parent.window
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)

        self.hlayout1 = QHBoxLayout()
        self.hlayout2 = QHBoxLayout()
        self.label = Label("Torrent File: ", parent=self)
        self.line = LineEdit(parent=self)
        self.treeWidget = TreeWidget(parent=self)
        self.browseButton = BrowseFolders.create(
            parent=self, text="...", mode=1
        )
        self.hlayout1.addWidget(self.label)
        self.hlayout1.addWidget(self.line)
        self.hlayout1.addWidget(self.browseButton)
        self.vlayout.addLayout(self.hlayout1)
        self.vlayout.addWidget(self.treeWidget)
        self.doneButton = DoneButton("Done", parent=self)
        self.vlayout.addWidget(self.doneButton)
        self.hlayout1.setObjectName("CheckWidget_hlayout1")


class DoneButton(QPushButton):
    """Button Widget for validating torrent files against downloaded contents.

    Args:
        text (`str`): The text displayed on the button itself.
        parent (`QWidget`, default=None): This widgets parent widget.
    """

    def __init__(self, text, parent=None):
        """Construct the CheckButton Widget."""
        super().__init__(text, parent=parent)
        self.widget = parent
        self.window = parent.window
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(pushButtonSheet)


class BrowseFolders(QToolButton):
    """Browse Folders ToolButton for activating filedialog.

    Args:
        parent (`QWidget`, default=None): Widget this widget is the child of.
    """

    modes = {
        0: {
            "func": QFileDialog.getExistingDirectory,
            "caption": "Select Contents Folder...",
            "directory": str(Path.home()),
        },
        1: {
            "func": QFileDialog.getOpenFileName,
            "caption": "Select Contents File...",
            "directory": str(Path.home()),
        },
    }

    def __init__(self, parent=None):
        """Construct a BrowseFolders Button Widget."""
        super().__init__(parent=parent)
        self.tree = parent.treeWidget
        self.setStyleSheet(toolButtonSheet)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mode = None
        self.pressed.connect(self.browse)

    @classmethod
    def create(cls, parent=None, text=None, mode=None):
        """Create new instance of button with mode."""
        btn = cls(parent=parent)
        btn.setText(text)
        btn.mode = mode
        return btn

    def browse(self, path=None):
        """Browse Action performed when user presses button.

        Returns:
            `str`: Path to file or folder to include in torrent.
        """
        if not path:  # pragma: no cover
            mode = self.modes[self.mode]
            path = mode["func"](
                directory=mode["directory"],
                parent=self,
                caption=mode["caption"],
            )
        if not path:
            return  # pragma: no cover
        path = os.path.normpath(path[0])
        self.tree.handleTorrent.emit(path)


class LineEdit(QLineEdit):
    """Line edit widget."""

    def __init__(self, parent=None):
        """Constructor for line edit widget."""
        super().__init__(parent=parent)
        self.setStyleSheet(lineEditSheet)
        font = self.font()
        font.setPointSize(11.5)
        self.setFont(font)


class Label(QLabel):
    """Label Identifier for Window Widgets.

    Subclass: QLabel
    """

    def __init__(self, text, parent=None):
        """Constructor for Label."""
        super().__init__(text, parent=parent)
        font = self.font()
        self.setStyleSheet(labelSheet)
        font.setBold(True)
        font.setPointSize(12)
        self.setFont(font)


class FieldItem(QTreeWidgetItem):
    """Item Widgets that are leafs to Tree Widget branches."""

    def __init__(self, type=0, tree=None):
        """Constructor for tree widget items."""
        super().__init__(type=type)
        policy = self.ChildIndicatorPolicy.DontShowIndicatorWhenChildless
        self.setChildIndicatorPolicy(policy)
        self.tree = tree
        self._value = None
        self.window = tree.window
        font = self.font(0)
        font.setPointSize(11)
        self.setFont(0, font)
        self.setFont(1, font)

    def setValue(self, val):
        """Set current items data to value."""
        self._value = val

    def value(self):
        """Current value in python version data."""
        return self._value

    def addChild(self, child):
        """Add a new child item."""
        super().addChild(child)
        self.tree.window.app.processEvents()

    @classmethod
    def create(cls, meta, tree=None):
        """Create item for tree."""
        item = cls(type=0, tree=tree)
        item.setValue(meta)
        if isinstance(meta, (bytes, bytearray)):
            item.setText(0, meta.hex())
        elif isinstance(meta, str):
            item.setText(0, meta)
        elif isinstance(meta, (int, float, bool)):
            item.setText(0, str(meta))
        return item


class TreeWidget(QTreeWidget):
    """Tree Widget for the `Check` tab.

    Displays percentages for matching files and their progress.

    Args:
        parent(`QWidget`, default=None)
    """

    handleTorrent = pyqtSignal([str])

    def __init__(self, parent=None):
        """Constructor for Tree Widget."""
        super().__init__(parent=parent)
        self.window = parent.window
        self.setStyleSheet(treeSheet + headerSheet)
        self.setColumnCount(2)
        self.setIndentation(10)
        self.setEditTriggers(
            self.EditTrigger.DoubleClicked
            | self.EditTrigger.EditKeyPressed
            | self.EditTrigger.SelectedClicked
        )
        # header = self.header()
        # header.setSectionResizeMode(0, header.ResizeMode.ResizeToContents)
        # header.setSectionResizeMode(1, header.ResizeMode.ResizeToContents)
        # self.setHeaderHidden(True)
        self.handleTorrent.connect(self.showTorrent)

    def showTorrent(self, path):
        """Display inforrmation contained in torrentfile."""
        try:
            meta = pyben.load(path)
        except PermissionError:
            self.window.statusbar.showMessage("Access Denied")
            return
        self.meta = meta
        root_item = FieldItem(type=0, tree=self)
        name = os.path.basename(path)
        root_item.setText(0, name)
        self.addTopLevelItem(root_item)
        self.traverse_meta(meta, root_item)

    def traverse_meta(self, meta, parent):
        """Traverse dictionary to create items for tree."""
        print(meta, parent, self)

    def clear(self):
        """Remove any objects from Tree Widget."""
        super().clear()
        self.item_tree = {"widget": self.invisibleRootItem()}
        self.itemWidgets = {}
        self.paths = []
        self.root = None
