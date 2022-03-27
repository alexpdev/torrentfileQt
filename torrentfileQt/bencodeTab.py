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
"""Widgets and procedures for the "Torrent Editor" tab."""

import os
from pathlib import Path

import pyben
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QToolButton, QTreeWidget,
                               QTreeWidgetItem, QVBoxLayout, QWidget)

from torrentfileQt.qss import bencode_editor


class BencodeWidget(QWidget):
    """Top level widget for Bencode Editor."""

    def __init__(self, parent=None):
        """Construct bencode editing widget.

        Args:
            parent (`QWidget`): parent widget of this widge.
        """
        super().__init__(parent=parent)
        self.window = parent.window
        self.layout = QVBoxLayout()
        self.line = QLineEdit(parent=self)
        self.line.setDisabled(True)
        self.button = Button("Save", parent=self)
        self.fileButton = FileButton(parent=self)
        self.label = QLabel("Torrent File:", parent=self)
        self.tree = BencodeTree(parent=self)
        self.addButton = AddButton("Add", parent=self)
        self.removeButton = RemoveButton("Remove", parent=self)
        self.hlayout = QHBoxLayout()
        self.hlayout2 = QHBoxLayout()
        self.hlayout2.addWidget(self.addButton)
        self.hlayout2.addWidget(self.removeButton)
        self.hlayout.addWidget(self.label)
        self.hlayout.addWidget(self.line)
        self.hlayout.addWidget(self.fileButton)
        self.layout.addLayout(self.hlayout)
        self.layout.addWidget(self.tree)
        self.layout.addLayout(self.hlayout2)
        self.layout.addWidget(self.button)
        self.layout.setObjectName("Editor_layout")
        self.line.setObjectName("Editor_line")
        self.button.setObjectName("Editor_button")
        self.fileButton.setObjectName("Editor_fileButton")
        self.label.setObjectName("Editor_label")
        self.tree.setObjectName("Editor_tree")
        self.setLayout(self.layout)


class Button(QPushButton):
    """Button Widget for saving results to .torrent file."""

    def __init__(self, text, parent=None):
        """Constructor for the save button on torrent bencode tab."""
        super().__init__(text, parent=parent)
        self.widget = parent
        self.clicked.connect(self.save)

    def save(self):
        """Save method for writing editet results to .torrent file."""
        tree = self.widget.tree
        text = self.widget.line.text()
        meta = tree.original
        for i in range(tree.topLevelItemCount()):
            child = tree.topLevelItem(i)
            if child.field not in meta:
                meta[child.field] = None
            new_meta = self.gather_children(child, meta[child.field])
            meta[child.field] = new_meta
        try:
            pyben.dump(meta, text)
        except:
            return

    def gather_children(self, parent, meta):
        """Recursive add values to fields."""
        values = []
        for i in range(parent.childCount()):
            child = parent.child(i)
            if child.field and child.field in meta:
                val = self.gather_children(child, meta[child.field])
                meta[parent.field] = val
            elif child.index and not child.value:
                val = self.gather_children(child, meta[child.index])
                values.append(val)
            elif child.index and child.value:
                values.append(child.value)
            else:
                if not child.edited:
                    return child.value
                try:
                    if isinstance(child.value, (str, int)):
                        value = type(child.value)(child.text(0))
                    elif isinstance(child.value, bytes):
                        value = bytes.fromhex(child.text(0))
                    return value
                except:
                    return child.text(0)
        if values:
            return values
        return meta


class FileButton(QToolButton):
    """Tool Button for selecting a .torrent file to edit."""

    def __init__(self, parent=None):
        """Constructor for the FileDialog button on Torrent Editor tab."""
        super().__init__(parent=parent)
        self.widget = parent
        self.setText("...")
        self.window = parent.window
        self.clicked.connect(self.browse)

    def browse(self, path=None):
        """Browse method for finding the .torrent file user wishes to edit."""
        if not path:  # pragma: no coverage
            path, _ = QFileDialog.getOpenFileName(
                dir=str(Path.home()),
                caption="Select Torrent File",
                filter="*.torrent",
            )
        if path:
            self.widget.tree.clear()
            self.widget.line.setText(path)
            self.widget.tree.handleTorrent.emit(path)


class TreeItem(QTreeWidgetItem):
    """Tree item."""

    def __init__(self, parent, type_):
        """Create tree item constructor."""
        super().__init__(parent, type_)
        self.widget = parent
        self.field = None
        self.value = None
        self.is_end = False
        self.index = None
        self.is_top = False
        self.edited = False
        font = self.font(0)
        font.setPointSize(12)
        self.setFont(0, font)


class BencodeTree(QTreeWidget):
    """Tree Widget that displays and can edit fields in bencode information."""

    handleTorrent = Signal([str])

    def __init__(self, parent=None):
        """Create tree widget constructor."""
        super().__init__(parent=parent)
        self.setStyleSheet(bencode_editor)
        self.window = parent.window
        self.setHeaderHidden(True)
        font = self.font()
        font.setPointSize(12)
        self.setFont(font)
        self.handleTorrent.connect(self.extract)
        self.original = None
        self.setColumnCount(1)

    def mouseDoubleClickEvent(self, *args):
        """Process event that occurs when item is double clicked."""
        item = self.currentItem()
        if not item.is_end:
            super().mouseDoubleClickEvent(*args)
            return
        if item.value and isinstance(item.value, bytes):
            item.setText(0, item.value.hex())
        super().mouseDoubleClickEvent(*args)
        item.edited = True

    def extract(self, path):
        """Extract data from a .torrent file."""
        if os.path.exists(path):
            try:
                data = pyben.load(path)
            except pyben.DecodeError:
                return
            self.original = data
            for key, value in data.items():
                item = TreeItem(self, 0)
                item.is_top = True
                item.field = key
                item.setText(0, key)
                self.addTopLevelItem(item)
                self.apply_values(item, value)

    def apply_values(self, parent, value, isfield=False):
        """Add torrent file fields to tree widget."""
        if isinstance(value, (str, int, bytes)):
            item = TreeItem(parent, 0)
            item.value = value
            if isinstance(value, bytes):
                text = repr(value)
                mn = min(len(text), 75)
                item.setText(0, text[2:mn])
            else:
                item.setText(0, str(value))
            item.is_end = True
            f = Qt.ItemFlag
            if not isfield:
                item.setFlags(
                    f.ItemIsSelectable | f.ItemIsEditable | f.ItemIsEnabled
                )
            parent.addChild(item)
            return item
        if isinstance(value, list):
            for i, elem in enumerate(value):
                if isinstance(elem, (str, int, bytes)):
                    item = self.apply_values(parent, elem)
                    item.index = i
                else:
                    item = TreeItem(parent, 0)
                    item.index = i
                    item.setText(0, f"i[{i}]")
                    self.apply_values(item, elem)
        elif isinstance(value, dict):
            for key, val in value.items():
                item = self.apply_values(parent, key, isfield=True)
                item.field = key
                self.apply_values(item, val)
        return item


class RemoveButton(QPushButton):
    """Remove branch from tree widget."""

    def __init__(self, text, parent=None):
        """Constructor for the save button on torrent editor tab."""
        super().__init__(text, parent=parent)
        self.widget = parent
        self.clicked.connect(self.send_signal)

    def send_signal(self):
        """Perform action when button is pressed."""
        tree = self.widget.tree
        tree_item = tree.currentItem()
        tree_item.parent().removeChild(tree_item)


class AddButton(QPushButton):
    """Add branch to Tree Widget."""

    def __init__(self, text, parent=None):
        """Constructor for the save button on torrent editor tab."""
        super().__init__(text, parent=parent)
        self.widget = parent
        self.clicked.connect(self.send_signal)

    def send_signal(self):
        """Perform action when button is pressed."""
        tree = self.widget.tree
        tree_item = tree.currentItem()
        item = TreeItem(tree_item, 0)
        tree_item.addChild(item)
        f = Qt.ItemFlag
        item.setFlags(f.ItemIsSelectable | f.ItemIsEditable | f.ItemIsEnabled)
        item.setText("")
