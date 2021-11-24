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
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QToolButton, QVBoxLayout, QWidget)

# from torrentfileQt.qss import (labelSheet, lineEditSheet, pushButtonSheet,
#                                tableSheet, toolButtonSheet)


class EditorWidget(QWidget):
    """Main widget for the torrent editor tab."""

    def __init__(self, parent=None):
        """Construct editor tab widget.

        Args:
            parent (`QWidget`): parent widget of this widge.
        """
        super().__init__(parent=parent)
        self.window = parent.window
        self.layout = QVBoxLayout()
        self.line = LineEdit(parent=self)
        self.button = Button("Save", parent=self)
        self.fileButton = FileButton(parent=self)
        self.label = QLabel("Torrent File:", parent=self)
        # self.label.setStyleSheet(labelSheet)
        self.table = Table(parent=self)
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.label)
        self.hlayout.addWidget(self.line)
        self.hlayout.addWidget(self.fileButton)
        self.layout.addLayout(self.hlayout)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)


class LineEdit(QLineEdit):
    """Line edit class from QLineEdit."""

    def __init__(self, parent=None):
        """Constructor for the LineEdit on torrent editor tab."""
        super().__init__(parent=parent)
        # self.setStyleSheet(lineEditSheet)
        self.setDisabled(True)
        self.widget = parent
        self.window = parent.window


class Button(QPushButton):
    """Button Widget for saving results to .torrent file."""

    def __init__(self, text, parent=None):
        """Constructor for the save button on torrent editor tab."""
        super().__init__(text, parent=parent)
        # self.setStyleSheet(pushButtonSheet)
        self.widget = parent
        self.pressed.connect(self.save)

    def save(self):
        """Save method for writing edit results to .torrent file."""
        table = self.widget.table
        text = self.widget.line.text()
        meta = table.original
        info = meta["info"]
        for row in range(table.rowCount()):
            label = table.item(row, 0).text()
            value = table.item(row, 1).text()
            if label in ["piece length", "private", "creation date"]:
                value = int(value)
            if label in meta and meta[label] != value:
                meta[label] = value
            elif label in info and info[label] != value:
                info[label] = value
        pyben.dump(meta, text)


class FileButton(QToolButton):
    """Tool Button for selecting a .torrent file to edit."""

    def __init__(self, parent=None):
        """Constructor for the FileDialog button on Torrent Editor tab."""
        super().__init__(parent=parent)
        self.widget = parent
        self.setText("...")
        self.window = parent.window
        # self.setStyleSheet(toolButtonSheet)
        self.pressed.connect(self.browse)

    def browse(self, path=None):
        """Browse method for finding the .torrent file user wishes to edit."""
        if not path:  # pragma: no coverage
            path = QFileDialog.getOpenFileName(
                directory=str(Path().home),
                caption="Select Torrent File",
                filter="*.torrent",
            )[0]
        self.widget.table.clear()
        self.widget.line.setText(path)
        self.widget.table.handleTorrent.emit(path)


class Table(QTableWidget):
    """Table widget for displaying editable information from .torrent file."""

    handleTorrent = pyqtSignal([str])

    def __init__(self, parent=None):
        """Constructor for the Table Widget on torrent editor tab."""
        super().__init__(parent=parent)
        # self.setStyleSheet(tableSheet)
        self.info = {}
        self.window = parent.window
        self.original = None
        self.setColumnCount(2)
        self.setRowCount(0)
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        vheader = self.verticalHeader()
        vheader.setSectionResizeMode(vheader.ResizeMode.Stretch)
        self.setHorizontalHeaderLabels(["Label", "Value"])
        self.handleTorrent.connect(self.export_data)

    def clear(self):
        """Remove any data previously added to table."""
        self.info = {}
        self.setRowCount(0)
        super().clear()

    def export_data(self, path):
        """Slot for the handleTorrent signal."""
        if not os.path.exists(path):  # pragma: no cover
            return
        self.original = pyben.load(path)
        self.flatten_data(self.original)
        counter = 0
        for k, v in self.info.items():
            self.window.app.processEvents()
            self.setRowCount(self.rowCount() + 1)
            item = QTableWidgetItem(0)
            item.setText(str(k))
            item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
            self.setItem(counter, 0, item)
            item2 = QTableWidgetItem(0)
            item2.setText(str(v))
            self.setItem(counter, 1, item2)
            counter += 1

    def flatten_data(self, data):
        """Flatten the meta dictionary found in the selected .torrent file."""
        for k, v in data.items():
            if k in [
                "source",
                "private",
                "announce",
                "name",
                "piece length",
                "comment",
                "creation date",
                "created by",
                "announce list",
            ]:
                self.info[k] = v
            elif k == "info":
                self.flatten_data(v)
