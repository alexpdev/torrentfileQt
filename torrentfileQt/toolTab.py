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
"""Magnet Widget containing Testing creation of Magnet URIs."""

import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QComboBox, QGroupBox, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QVBoxLayout, QWidget)
from torrentfile import magnet
from torrentfile.utils import path_stat

from torrentfileQt.utils import (browse_files, browse_folder, browse_torrent,
                                 get_icon)


class ToolWidget(QWidget):
    """Tab for creating magnet URL's and downloading torrentfiles from them."""

    def __init__(self, parent=None):
        """Initialize the widget for creating magnet URI's from a metafile."""
        super().__init__(parent=parent)
        self.centralWidget = QWidget()
        self.centralLayout = QVBoxLayout(self)
        self.setObjectName("toolTab")
        self.centralLayout.addWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)
        self.magnetgroup = MagnetGroup(self)
        self.layout.addWidget(self.magnetgroup)
        self.piece_length_calculator = PieceLengthCalculator()
        self.layout.addWidget(self.piece_length_calculator)


class SubmitButton(QPushButton):
    """Submit current information to be processed into a megnet URI."""

    def __init__(self, parent=None):
        """Initialize the button for magnet creation."""
        super().__init__(parent=parent)
        self.widget = parent
        self.setText("Create Magnet")
        self.clicked.connect(self.magnet)

    def magnet(self):
        """Create a magnet URI from information contained in form."""
        fd = self.widget.pathEdit.text()
        if os.path.exists(fd):
            uri = magnet(fd)
            self.widget.magnetEdit.setText(uri)


class MetafileButton(QPushButton):
    """
    Find a .torrent file in native file browser button actions.

    Perameters
    ----------
    parent : `QWidget`
        This widgets parent.
    """

    def __init__(self, parent=None):
        """Initialize the metafile button."""
        super().__init__(parent=parent)
        self.window = parent.window
        self.widget = parent
        self.setText("Select Torrent File")
        self.setIcon(get_icon("browse_file"))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pressed.connect(self.select_metafile)

    def select_metafile(self):
        """Find metafile in file browser."""
        path = browse_torrent(self)
        self.widget.pathEdit.setText(path if path else "")


class MagnetGroup(QGroupBox):
    """
    Group Box for calculating magnet uri's.

    Paramters
    ---------
    parent : QWidget
        the parent to this widget
    """

    def __init__(self, parent=None):
        """Create the Magnet group box widget."""
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.setObjectName("MagnetGroup")
        self.setTitle("Create Magnet URI")
        self.metafilebutton = MetafileButton(self)
        self.submit_button = SubmitButton(self)
        self.pathEdit = QLineEdit(self)
        self.magnetEdit = QLineEdit(self)
        self.pathLabel = QLabel("Path: ")
        self.magnetLabel = QLabel("Magnet URI: ")
        self.layout.addWidget(self.pathLabel)
        self.layout.addWidget(self.pathEdit)
        self.layout.addWidget(self.magnetLabel)
        self.layout.addWidget(self.magnetEdit)
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.metafilebutton)
        self.hlayout.addWidget(self.submit_button)
        self.layout.addLayout(self.hlayout)


class PieceLengthBox(QComboBox):
    """
    Combo box for the piece length options.

    Parameters
    ----------
    parent : QWidget
        the parent to this widget
    """

    def __init__(self, parent=None):
        """Create the piece length combo box widget."""
        super().__init__(parent)
        self.setEditable(False)
        self.__data = {}
        self.loadItems()

    def get_value(self):  # pragma: nocover
        """
        Get the current text's corresponding value.
        """
        text = self.currentText()
        return self.__data[text]

    def loadItems(self):
        """
        Load the options into the list for selection.
        """
        for i in range(14, 26):
            value = 2**i
            if i < 20:
                text = f"{value // 2**10} KiB"
            else:
                text = f"{value // 2**20} MiB"
            self.__data[text] = value
            self.addItem(text)

    def set_item(self, value):
        """
        Set the current text based on the value provided.

        Parameter
        ---------
        value : int
            The value that matches the key text to select as current.
        """
        self.blockSignals(True)
        for k, v in self.__data.items():
            if v == value:
                self.setCurrentText(k)
                break
        self.blockSignals(False)


class PieceLengthCalculator(QGroupBox):
    """
    Group box for calculating ideal piece length.

    Parameters
    ----------
    parent : QWidget
        the parent to this widget
    """

    def __init__(self, parent=None):
        """Create the piece length calculator widget."""
        super().__init__(parent=parent)
        self.setObjectName("PieceLengthCalculator")
        self.setTitle("Piece Length Calculator")
        self.layout = QVBoxLayout(self)
        icon = get_icon("browse_file")
        icon2 = get_icon("browse_folder")
        self.fileButton = QPushButton(icon, "Select File", self)
        self.folderButton = QPushButton(icon2, "Select Folder", self)
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.fileButton)
        self.hlayout.addWidget(self.folderButton)
        self.path_label = QLabel("Path: ", self)
        self.path_line = QLineEdit(self)
        self.size_label = QLabel("Size: ", self)
        self.file_count_label = QLabel("File Count: ")
        self.piece_length_label = QLabel("Piece Length: ", self)
        self.piece_count_label = QLabel("Total Pieces: ", self)
        self.file_count_line = QLineEdit()
        self.size_line = QLineEdit()
        self.piece_count_line = QLineEdit()
        self.piece_length_combo = PieceLengthBox(self)
        self.layout.addWidget(self.path_label)
        self.layout.addWidget(self.path_line)
        self.layout.addWidget(self.size_label)
        self.layout.addWidget(self.size_line)
        self.layout.addWidget(self.piece_length_label)
        self.layout.addWidget(self.piece_length_combo)
        self.layout.addWidget(self.piece_count_label)
        self.layout.addWidget(self.piece_count_line)
        self.layout.addWidget(self.file_count_label)
        self.layout.addWidget(self.file_count_line)
        self.layout.addLayout(self.hlayout)
        self.fileButton.clicked.connect(self.browse_files)
        self.folderButton.clicked.connect(self.browse_folders)
        self.piece_length_combo.currentTextChanged.connect(
            self.calculate_piece_length)

    def calculate_piece_length(self):
        """
        Calculate the piece length based on the current text of the combo box.
        """
        size = self.size_line.text()
        if size:
            size = int(size)
            plength = self.piece_length_combo.get_value()
            val = size / plength
            if int(val) == val:  # pragma: nocover
                self.piece_count_line.setText(str(int(val)))
            else:
                self.piece_count_line.setText(str(int(val + 1)))

    def calculate(self, path):
        """
        Calculate all the fields based on the path selected by user.

        Parameters
        ----------
        path : str
            the path selected by the user by browsing the file system
        """
        self.path_line.setText(path if path else "")
        if path:
            file_list, size, piece_length = path_stat(path)
            self.piece_length_combo.set_item(piece_length)
            self.size_line.setText(str(size))
            total_pieces = size / piece_length
            if total_pieces == size // piece_length:  # pragma: nocover
                self.piece_count_line.setText(str(int(total_pieces)))
            else:
                self.piece_count_line.setText(str(int(total_pieces + 1)))
            self.file_count_line.setText(str(len(file_list)))

    def browse_files(self):
        """Browse for files for caluclating ideal piece lengths."""
        path = browse_files(self)
        self.calculate(path)

    def browse_folders(self):
        """Browse for folders for calculating ideal piece lengths."""
        path = browse_folder(self)
        self.calculate(path)
