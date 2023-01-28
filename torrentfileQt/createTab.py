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
"""
Tab Widget containing all controls for creating a new .torrent file.

User must provide the path to the directory containing the what the
.torrent file will be created from.
"""
import os
from copy import deepcopy
from pathlib import Path

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFileDialog,
                               QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
                               QPushButton, QRadioButton, QSpacerItem, QWidget)
from torrentfile.torrent import TorrentFile, TorrentFileHybrid, TorrentFileV2
from torrentfile.utils import path_piece_length

from torrentfileQt.utils import browse_files, browse_folder, get_icon
from torrentfileQt.widgets import DropGroupBox


class CreateWidget(QWidget):
    """
    CreateWidget contains all controls for creating a new .torrent file.

    Parameters
    ----------
    parent : QWidget
        Parent class to CreateWidget.
    """

    def __init__(self, parent=None):
        """
        Construct for Create Widget.

        Parameters
        ----------
        parent : QWidget
            Parent Widget. Defaults to None.
        """
        super().__init__(parent=parent)
        self.setObjectName("createTab")
        self.setAcceptDrops(True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.centralLayout = QVBoxLayout(self)
        self.centralWidget = QWidget()
        self.centralWidget.setObjectName("CreateCentralWidget")
        self.centralLayout.addWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)


        versionBox = QGroupBox()
        versionBox.setTitle("Torrent Version")
        hlayout0 = QHBoxLayout(versionBox)
        self.v1button = QRadioButton("v1 (default)", parent=self)
        self.v1button.setChecked(True)
        self.v2button = QRadioButton("v2", parent=self)
        self.hybridbutton = QRadioButton("v1+2 (hybrid)", parent=self)
        hlayout0.addWidget(self.v1button)
        hlayout0.addWidget(self.v2button)
        hlayout0.addWidget(self.hybridbutton)

        self.path_group = DropGroupBox(parent=self)
        self.path_dir_button = BrowseDirButton(parent=self)
        self.path_file_button = BrowseFileButton(parent=self)
        self.path_group.addButton(self.path_dir_button)
        self.path_group.addButton(self.path_file_button)
        self.path_group.setTitle("Content Path")
        self.path_group.setLabelText("Drop File/Folder Here")
        self.path_dir_button.folderSelected.connect(self.setPath)
        self.path_file_button.fileSelected.connect(self.setPath)
        self.path_group.pathSelected.connect(self.setPath)

        output_label = QLabel("Save Path", parent=self)
        output_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hlayout3 = QHBoxLayout()
        self.output_path_edit = QLineEdit(parent=self)
        self.output_button = OutButton(parent=self)
        hlayout3.addWidget(self.output_path_edit)
        hlayout3.addWidget(self.output_button)

        source_label = QLabel("Source", parent=self)
        source_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.source_edit = QLineEdit(parent=self)

        comment_label = QLabel("Comment", parent=self)
        comment_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.comment_edit = QLineEdit(parent=self)

        announce_label = QLabel("Trackers: ", parent=self)
        announce_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.announce_input = QPlainTextEdit(parent=self)
        self.announce_input.setMaximumHeight(150)

        web_seed_label = QLabel("Web-Seeds: ", parent=self)
        web_seed_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.web_seed_input = QPlainTextEdit(parent=self)
        self.web_seed_input.setMaximumHeight(150)

        hlayout2 = QHBoxLayout()
        piece_length_label = QLabel("Torrent Piece Length", parent=self)
        self.piece_length_combo = ComboBox.piece_length(parent=self)
        self.private = QCheckBox("Private", parent=self)
        spacer1 = QSpacerItem(150, 0)
        spacer2 = QSpacerItem(70, 0)
        hlayout2.addWidget(piece_length_label)
        hlayout2.addWidget(self.piece_length_combo)
        hlayout2.addItem(spacer1)
        hlayout2.addWidget(self.private)
        hlayout2.addItem(spacer2)

        self.submit_button = SubmitButton("Create Torrent", parent=self)

        self.layout.addWidget(self.path_group)
        self.layout.addWidget(output_label)
        self.layout.addLayout(hlayout3)
        self.layout.addLayout(hlayout2)
        self.layout.addWidget(versionBox)
        self.layout.addWidget(source_label)
        self.layout.addWidget(self.source_edit)
        self.layout.addWidget(comment_label)
        self.layout.addWidget(self.comment_edit)
        self.layout.addWidget(announce_label)
        self.layout.addWidget(self.announce_input)
        self.layout.addWidget(web_seed_label)
        self.layout.addWidget(self.web_seed_input)
        self.layout.addWidget(self.submit_button)


    def setPath(self, path):
        piece_length = path_piece_length(path)
        if piece_length < (2**20):
            val = f"{piece_length//(2**10)} KiB"
        else:
            val = f"{piece_length//(2**20)} MiB"
        self.path_group.setLabelText(path)
        self.piece_length_combo.setValue(val)
        self.output_input.setText(path + ".torrent")


class TorrentFileCreator(QThread):
    """
    Torrentfile creation class.

    Takes arguments provided by the GUI, and uses the internal
    torrentfile cli to create the torrent.

    Parameters
    ----------
    args : dict
        keyword arguments from the GUI fields
    creator : type
        Which version of torrent file creator
    name : list
        container to add return values to
    """

    created = Signal()

    def __init__(self, args, creator):
        """Construct the new thread."""
        super().__init__()
        self.args = args
        self.creator = creator

    def run(self):
        """Create a torrent file and emit it's path."""
        args = deepcopy(self.args)
        torrent = self.creator(**args)
        _, _ = torrent.write()
        self.created.emit()


class SubmitButton(QPushButton):
    """Button widget."""

    def __init__(self, text, parent=None):
        """
        Construct the submit button.

        Parameters
        ----------
        text : `str`
            Text displayed on the button itself.
        parent : QWidget
            The tab widget parent.
        """
        super().__init__(text, parent=parent)
        self.thread = None
        self._text = text
        self.widget = parent
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setText(text)
        self.clicked.connect(self.submit)

    def submit(self):
        """Submit Action performed when user presses Submit Button."""
        # Gather Information from other Widgets.
        args = {}
        if self.widget.private.isChecked():
            args["private"] = 1

        # add source to metadata
        sourcetext = self.widget.source_input.text()
        if sourcetext:
            args["source"] = sourcetext

        # add comments to metadata
        commenttext = self.widget.comment_input.text()
        if commenttext:
            args["comment"] = commenttext

        # at least 1 tracker input is required
        announce = self.widget.announce_input.toPlainText()
        announce = [i for i in announce.split("\n") if i]
        if announce:
            args["announce"] = announce

        url_list = self.widget.web_seed_input.toPlainText()
        url_list = [i for i in url_list.split("\n") if i]
        if url_list:
            args["url_list"] = url_list

        # Calculates piece length if not specified by user.
        outtext = os.path.realpath(self.widget.output_input.text())
        if outtext:
            args["outfile"] = outtext

        current = self.widget.piece_length.currentIndex()
        if current:
            piece_length_index = self.widget.piece_length.currentIndex()
            piece_length = self.widget.piece_length.itemData(
                piece_length_index)
            args["piece_length"] = piece_length

        if self.widget.hybridbutton.isChecked():
            creator = TorrentFileHybrid
        elif self.widget.v2button.isChecked():
            creator = TorrentFileV2
        else:
            creator = TorrentFile

        path = self.widget.path_input.text()
        args["path"] = path
        self.thread = TorrentFileCreator(args, creator)
        self.thread.created.connect(self.updateStatusBarEnd)
        self.thread.started.connect(self.updateStatusBarBegin)
        self.thread.start()

    def updateStatusBarBegin(self):
        """Update the status bar when torrent creation is complete."""
        self.window().statusBar().showMessage("Processing", 3000)

    def updateStatusBarEnd(self):
        """Update the status bar when torrent creation is complete."""
        self.window().statusBar().showMessage("Completed", 3000)


class OutButton(QPushButton):
    """Button widget."""

    savePathSelected = Signal(str)

    def __init__(self, parent=None):
        """Construct for file picker for outfile button."""
        super().__init__(parent=parent)
        self.setText("File")
        self.setIcon(get_icon("browse_file"))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.output)

    def output(self):
        """Assign output path for created torrent file."""
        outpath, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save as",
            dir=str(Path.home()),
            filter="*.torrent",
            selectedFilter="",
        )
        if outpath:
            self.savePathSelected.emit(outpath)


class BrowseFileButton(QPushButton):
    """Button widget for browse."""

    fileSelected = Signal(str)

    def __init__(self, parent=None):
        """Public constructor for browsebutton class."""
        super().__init__(parent)
        self.setObjectName("CreateFileButton")
        self.setIcon(get_icon("browse_file"))
        self.setText("Select File")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.browse)

    def browse(self):
        """
        Browse performed when user presses button.

        Opens File/Folder Dialog.
        """
        path = browse_files(self)
        if path:
            self.fileSelected.emit(path)


class BrowseDirButton(QPushButton):
    """Browse filesystem folders for path."""

    folderSelected = Signal(str)

    def __init__(self, parent=None):
        """Construct for folder browser button."""
        super().__init__(parent=parent)
        self.setObjectName("CreateFolderButton")
        self.setIcon(get_icon("browse_folder"))
        self.setText("Select Folder")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.browse)

    def browse(self, path=None):
        """
        Browse action performed when user presses button.

        Opens File/Folder Dialog.
        """
        path = browse_folder(self, path)
        if path:
            self.folderSelected.emit(path)


class ComboBox(QComboBox):
    """Combo box options for selecting piece length."""

    def __init__(self, parent=None):
        """Construct for ComboBox."""
        super().__init__(parent=parent)
        self.addItem("")
        self.setEditable(False)
        self.profile_data = None

    @classmethod
    def piece_length(cls, parent=None):
        """Create a piece_length combobox."""
        box = cls(parent=parent)
        for exp in range(14, 25):
            if exp < 20:
                item = str((2**exp) // (2**10)) + " KiB"
            else:
                item = str((2**exp) // (2**20)) + " MiB"
            box.addItem(item, 2**exp)
        return box

    def setValue(self, val):
        """Set the current value to val."""
        for i in range(self.count()):
            if self.itemText(i) == val:
                self.setCurrentIndex(i)
                break
