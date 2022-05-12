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
from copy import deepcopy
from pathlib import Path

import pyben
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from torrentfileQt.qss import table_styles


class EditorWidget(QWidget):
    """Main widget for the torrent editor tab."""

    def __init__(self, parent=None):
        """Construct editor tab widget.

        Args:
            parent (`QWidget`): parent widget of this widge.
        """
        super().__init__(parent=parent)
        self.window = parent.window
        self.counter = 0
        self.layout = QVBoxLayout()
        self.line = QLineEdit(parent=self)
        self.line.setStyleSheet("QLineEdit{margin-left: 15px;}")
        self.button = Button("Save", parent=self)
        self.fileButton = FileButton(parent=self)
        self.fileButton.setStyleSheet("QToolButton{margin-right: 10px;}")
        self.label = QLabel("Torrent File Editor", parent=self)
        self.label.setAlignment(Qt.AlignCenter)
        self.table = Table(parent=self)
        self.hlayout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.hlayout.addWidget(self.line)
        self.hlayout.addWidget(self.fileButton)
        self.layout.addLayout(self.hlayout)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.button)
        self.layout.setObjectName("Editor_layout")
        self.line.setObjectName("Editor_line")
        self.button.setObjectName("Editor_button")
        self.fileButton.setObjectName("Editor_fileButton")
        self.label.setObjectName("Editor_label")
        self.table.setObjectName("Editor_table")
        self.setLayout(self.layout)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        """Drag enter event for widget."""
        if event.mimeData().hasUrls:
            self.counter += 1
            event.accept()
            return True
        self.counter -= 1
        return event.ignore()

    def dragMoveEvent(self, event):
        """Drag Move Event for widgit."""
        if event.mimeData().hasUrls:
            self.counter -= 1
            event.accept()
            return True
        self.counter += 1
        return event.ignore()

    def dropEvent(self, event) -> bool:
        """Drag drop event for widgit."""
        urls = event.mimeData().urls()
        path = urls[0].toLocalFile()
        if os.path.exists(path):
            self.table.clear()
            self.line.setText(path)
            self.table.handleTorrent.emit(path)
            return True
        return False


class Button(QPushButton):
    """Button Widget for saving results to .torrent file."""

    def __init__(self, text: str, parent=None):
        """Constructor for the save button on torrent editor tab."""
        super().__init__(text, parent=parent)
        self.widget = parent
        self.clicked.connect(self.save)

    def save(self):
        """Save method for writing edit results to .torrent file."""
        table = self.widget.table
        text = self.widget.line.text()
        meta = table.original
        info = meta["info"]
        for row in range(table.rowCount()):
            label = table.item(row, 0).text()
            if label in ["url-list", "httpseeds", "announce-list"]:
                widget = table.cellWidget(row, 1)
                combo = widget.combo
                value = []
                for i in range(combo.count()):
                    txt = combo.itemText(i).strip(" ")
                    if txt:
                        value.append(txt)
                if label == "announce-list":
                    value = [value]
            else:
                value = table.item(row, 1).text().strip(" ")
            if not value:
                continue
            if label in ["piece length", "private", "creation date"]:
                value = int(value)
            if label in meta and meta[label] != value:
                meta[label] = value
            elif label in info and info[label] != value:
                info[label] = value  # pragma: no cover
        pyben.dump(meta, text)


class FileButton(QToolButton):
    """Tool Button for selecting a .torrent file to edit."""

    def __init__(self, parent=None):
        """Constructor for the FileDialog button on Torrent Editor tab."""
        super().__init__(parent=parent)
        self.widget = parent
        self.setText("Select File")
        self.window = parent.window
        self.clicked.connect(self.browse)

    def browse(self, path: str = None):
        """Browse method for finding the .torrent file user wishes to edit."""
        if not path:  # pragma: no coverage
            path, _ = QFileDialog.getOpenFileName(
                dir=str(Path.home()),
                caption="Select Torrent File",
                filter="*.torrent",
            )
        if path:
            self.widget.table.clear()
            self.widget.line.setText(path)
            self.widget.table.handleTorrent.emit(path)


class AddItemButton(QToolButton):
    """Button for editing adjacent ComboBox."""

    def __init__(self, parent):
        """Construct the Button."""
        super().__init__(parent)
        self.setStyleSheet(table_styles["button"])
        self.parent = parent
        self.setText("add")
        self.box = None
        self.clicked.connect(self.add_item)

    def add_item(self):
        """Take action when button is pressed."""
        items = [self.box.itemText(i) for i in range(self.box.count())]
        current = self.box.currentText().strip(" ")
        if current and current not in items:
            self.box.insertItem(0, current, 2)
        self.box.insertItem(0, "", 2)
        self.box.setCurrentIndex(0)
        self.parent.line_edit.setReadOnly(True)


class RemoveItemButton(QToolButton):
    """Button for editing adjacent ComboBox."""

    def __init__(self, parent):
        """Construct the Button."""
        super().__init__(parent)
        self.setStyleSheet(table_styles["button"])
        self.parent = parent
        self.setText("remove")
        self.box = None
        self.clicked.connect(self.remove_item)

    def remove_item(self):
        """Take action when button is pressed."""
        index = self.box.currentIndex()
        self.box.removeItem(index)
        self.parent.line_edit.setReadOnly(True)


class Table(QTableWidget):
    """Table widget for displaying editable information from .torrent file."""

    handleTorrent = Signal([str])

    def __init__(self, parent=None):
        """Constructor for the Table Widget on torrent editor tab."""
        super().__init__(parent=parent)
        self.info = {}
        self.window = parent.window
        self.original = None
        self.setColumnCount(2)
        self.setRowCount(0)
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        vheader = self.verticalHeader()
        vheader.setSectionResizeMode(vheader.ResizeMode.Stretch)
        vheader.setHidden(True)
        self.setHorizontalHeaderLabels(["Label", "Value"])
        self.handleTorrent.connect(self.export_data)

    def clear(self):
        """Remove any data previously added to table."""
        self.info = {}
        for row in range(self.rowCount()):
            self.removeRow(row)
        self.setRowCount(0)
        super().clear()

    def export_data(self, path):
        """Slot for the handleTorrent signal."""
        if not os.path.exists(path):  # pragma: no cover
            return
        data = pyben.load(path)
        self.original = deepcopy(data)
        self.flatten_data(data)
        counter = 0
        for k, v in sorted(self.info.items()):
            self.window.app.processEvents()
            self.setRowCount(self.rowCount() + 1)
            item = QTableWidgetItem(0)
            item.setText(str(k))
            item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
            self.setItem(counter, 0, item)
            if k in ["announce-list", "url-list", "httpseeds"]:
                widget = ComboCell(parent=self)
                self.setCellWidget(counter, 1, widget)
                widget.set_values(k, v)
            else:
                item2 = QTableWidgetItem(0)
                item2.setText(str(v))
                self.setItem(counter, 1, item2)
            counter += 1

    def flatten_data(self, data):
        """Flatten the meta dictionary found in the selected .torrent file."""
        fields = [
            "source",
            "private",
            "announce",
            "name",
            "comment",
            "creation date",
            "created by",
            "announce-list",
            "url-list",
            "httpseeds",
        ]
        info = data["info"]
        del data["info"]
        data.update(info)
        for field in fields:
            if field not in data:
                self.info[field] = ""
            else:
                self.info[field] = data[field]


class ComboCell(QWidget):
    """Widget used inside the cell of a Table Widget."""

    class Combo(QComboBox):
        """A Combo Box widget for inside table cells."""

        def __init__(self, parent=None):
            """Construct a combobox for table widget cell."""
            super().__init__(parent=parent)
            self.widget = parent
            self.setStyleSheet(table_styles["ComboBox"])
            self.setInsertPolicy(self.InsertPolicy.InsertAtBottom)
            self.setDuplicatesEnabled(False)
            self.widget.line_edit.setReadOnly(True)

        def focusOutEvent(self, _):
            """Add item when focus changes."""
            super().focusOutEvent(_)
            current = self.currentText().strip()
            items = [self.itemText(i) for i in range(self.count())]
            blanks = [i for i in range(len(items)) if not items[i].strip()]
            list(map(self.removeItem, blanks[::-1]))
            if current and current not in items:
                self.insertItem(0, current, 2)
            self.widget.line_edit.setReadOnly(True)

        def focusInEvent(self, _):
            """Make line edit widget active when clicking in to box."""
            super().focusInEvent(_)
            self.widget.line_edit.setReadOnly(False)

    def __init__(self, parent=None):
        """Construct the widget and it's sub widgets."""
        super().__init__(parent=parent)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.line_edit = QLineEdit(parent=self)
        self.line_edit.setStyleSheet(table_styles["LineEdit"])
        self.combo = self.Combo(parent=self)
        self.layout.addWidget(self.combo)
        self.combo.setLineEdit(self.line_edit)
        self.add_button = AddItemButton(self)
        self.add_button.box = self.combo
        self.remove_button = RemoveItemButton(self)
        self.remove_button.box = self.combo
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.remove_button)

    def set_values(self, key, val):
        """Fill in the values of pre-set urls for each list."""
        if val and isinstance(val, list):
            if key == "announce-list":
                lst = [k for j in val for k in j]
            else:
                lst = val
            for url in lst:
                self.combo.addItem(url, 2)
