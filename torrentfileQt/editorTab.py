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

import datetime
from copy import deepcopy

import pyben
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QCheckBox, QComboBox, QGroupBox, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QSizePolicy,
                               QTableWidget, QTableWidgetItem, QVBoxLayout,
                               QWidget)

from torrentfileQt.utils import DropGroupBox, browse_torrent, get_icon


class EditorWidget(QWidget):
    """Main widget for the torrent editor tab."""

    def __init__(self, parent=None):
        """
        Construct editor tab widget.

        Parameters
        ----------
        parent : QWidget
            parent widget of this widge.
        """
        super().__init__(parent=parent)
        self.setObjectName("editTab")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.centralWidget = QWidget()
        self.centralWidget.setObjectName("EditCentralWidget")
        self.centralLayout = QVBoxLayout(self)
        mainLabel = QLabel("Edit Torrent File")
        mainLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLabel.setObjectName("editorMainLabel")
        self.centralLayout.addWidget(mainLabel)
        self.centralLayout.addWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        self.filegroup = DropGroupBox(parent=self)
        self.filegroup.setObjectName("EditDropGroup")
        self.filegroup.setTitle("Torrent Path")
        self.fileButton = FileButton(parent=self)
        self.filegroup.addButton(self.fileButton)
        self.filegroup.setLabelText("drag & drop torrent file here or ...")
        self.layout.addWidget(self.filegroup)
        self.fileButton.fileSelected.connect(self.editTorrent)
        self.filegroup.pathSelected.connect(self.editTorrent)

        self.table = Table(parent=self)
        self.layout.addWidget(self.table)

        self.save_button = SaveEditButton("Save", parent=self)
        self.layout.addWidget(self.save_button)

    def editTorrent(self, path: str) -> None:
        """Drag drop event for widgit."""
        self.filegroup.setPath(path)
        self.table.clear()
        self.table.handleTorrent.emit(path)


class SaveEditButton(QPushButton):
    """Button Widget for saving results to .torrent file."""

    def __init__(self, text: str, parent=None):
        """Construct for the save button on torrent editor tab."""
        super().__init__(text, parent=parent)
        self.setObjectName("EditSaveButton")
        self.setText("Save Torrent")
        self.clicked.connect(self.save)
        self._parent = parent

    def save(self):
        """Save method for writing edit results to .torrent file."""
        table: QTableWidget = self._parent.table
        text = self._parent.filegroup.getPath()
        meta = table.original
        info = meta["info"]

        for row in range(table.rowCount()):
            label = table.item(row, 0).text()
            value = None

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

            elif label == "creation date":
                value = table.item(row, 1).text().strip(" ")

            elif label == "private":
                widget = table.cellWidget(row, 1)
                value = 1 if widget.isChecked() else 0

            if not value:
                continue

            if label in meta:
                if meta[label] != value:
                    meta[label] = value

            elif label in info:
                if info[label] != value:
                    info[label] = value  # pragma: nocover

            elif label in ["comment", "source", "private"]:
                info[label] = value  # pragma: nocover

            else:
                meta[label] = value

        pyben.dump(meta, text)


class FileButton(QPushButton):
    """Tool Button for selecting a .torrent file to edit."""

    fileSelected = Signal(str)

    def __init__(self, parent=None):
        """Construct for the FileDialog button on Torrent Editor tab."""
        super().__init__(parent=parent)
        self.setIcon(get_icon("browse_file"))
        self.setText("Select Torrent File")
        self.clicked.connect(self.browse)
        self._parent = parent

    def browse(self):
        """Browse method for finding the .torrent file user wishes to edit."""
        path = browse_torrent(self)
        if path:
            self.fileSelected.emit(path)


class AddItemButton(QPushButton):
    """Button for editing adjacent ComboBox."""

    def __init__(self, parent: QWidget):
        """Construct the Button."""
        super().__init__(parent)
        self.setIcon(get_icon("plus"))
        self.setText("Add")
        self.clicked.connect(self.add_item)
        self._parent = parent

    def add_item(self):
        """Take action when button is pressed."""
        combo = self._parent.combo
        items = [combo.itemText(i) for i in range(combo.count())]
        current = combo.currentText().strip(" ")
        if current and current not in items:
            combo.insertItem(0, current, 2)
        combo.insertItem(0, "", 2)
        combo.setCurrentIndex(0)


class RemoveItemButton(QPushButton):
    """Button for editing adjacent ComboBox."""

    def __init__(self, parent):
        """Construct the Button."""
        super().__init__(parent)
        self.setText("Remove")
        self.setIcon(get_icon("minus"))
        self.clicked.connect(self.remove_item)
        self._parent = parent

    def remove_item(self):
        """Take action when button is pressed."""
        index = self._parent.combo.currentIndex()
        self._parent.combo.removeItem(index)
        self._parent.line_edit.setReadOnly(True)


class Table(QTableWidget):
    """Table widget for displaying editable information from .torrent file."""

    handleTorrent = Signal(str)

    def __init__(self, parent=None):
        """Construct for the Table Widget on torrent editor tab."""
        super().__init__(parent=parent)
        self.setColumnCount(2)
        self.setRowCount(0)
        self.setObjectName("EditTable")

        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        self.setHorizontalHeaderLabels(["Field", "Value"])

        vheader = self.verticalHeader()
        vheader.setSectionResizeMode(vheader.ResizeMode.Stretch)
        vheader.setHidden(True)

        self.info = {}
        self.original = None
        self.handleTorrent.connect(self.export_data)

    def clear(self) -> None:
        """Remove any data previously added to table."""
        self.info = {}
        for row in range(self.rowCount()):
            self.removeRow(row)
        self.setRowCount(0)
        super().clear()
        self.setHorizontalHeaderLabels(["Field", "Value"])

    def export_data(self, path: str) -> None:
        """Export slot for the handleTorrent signal."""
        data = pyben.load(path)
        self.original = deepcopy(data)
        self.flatten_data(data)

        for k, v in sorted(self.info.items()):
            index = self.rowCount()
            self.insertRow(index)
            item = QTableWidgetItem(0)
            item.setText(str(k))
            item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
            self.setItem(index, 0, item)

            if k in ["announce-list", "url-list", "httpseeds"]:
                widget = EditGroupBox(parent=self)
                self.setCellWidget(index, 1, widget)
                widget.set_values(k, v)

            elif k == "private":
                v = v if v else 0
                widget = QCheckBox(parent=self)
                widget.setChecked(v)
                self.setCellWidget(index, 1, widget)

            elif k == "creation date":
                item2 = QTableWidgetItem(0)
                item2._data = str(v)
                value = datetime.datetime.fromtimestamp(v)
                text_value = datetime.datetime.isoformat(value)
                item2.setText(text_value)
                self.setItem(index, 1, item2)

            else:
                item2 = QTableWidgetItem(0)
                item2.setText(str(v))
                self.setItem(index, 1, item2)

    def flatten_data(self, data) -> dict:
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


class Combo(QComboBox):
    """A Combo Box widget for inside table cells."""

    def __init__(self, parent=None):
        """Construct a combobox for table widget cell."""
        super().__init__(parent=parent)
        self.widget = parent
        self.sizePolicy().setVerticalPolicy(QSizePolicy.Minimum)
        self.setMinimumContentsLength(48)
        self.sizePolicy().setHorizontalPolicy(QSizePolicy.Minimum)
        self.setInsertPolicy(self.InsertPolicy.InsertAtBottom)
        self.setDuplicatesEnabled(False)


class EditGroupBox(QGroupBox):
    """Toolbar for the combobox and buttons."""

    def __init__(self, parent=None):
        """Construct the toolbar instance."""
        super().__init__(parent=parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setObjectName("EditGroupBox")
        self.line_edit = QLineEdit(parent=self)
        self.combo = Combo(self)
        self.layout.addWidget(self.combo)
        self.layout.setSpacing(0)
        self.combo.setLineEdit(self.line_edit)
        self.add_button = AddItemButton(self)
        self.remove_button = RemoveItemButton(self)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.remove_button)

    def set_values(self, key, val):
        """Fill in the values of pre-set urls for each list."""
        if val and isinstance(val, list):
            if key == "announce-list":
                lst = [k for j in val for k in j]
            else:
                lst = val  # pragma: nocover
            for url in lst:
                self.combo.addItem(url, 2)
