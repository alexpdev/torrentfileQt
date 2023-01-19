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

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFileDialog, QGridLayout,
                               QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
                               QPushButton, QRadioButton, QSizePolicy,
                               QSpacerItem, QWidget)
from torrentfile.torrent import TorrentFile, TorrentFileHybrid, TorrentFileV2
from torrentfile.utils import path_piece_length

from torrentfileQt.utils import browse_files, browse_folder, get_icon


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
        self.content_dir = None
        self.outpath = None
        self.window = parent.window
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.hlayout1 = QHBoxLayout()
        self.hlayout2 = QHBoxLayout()
        self.hlayout3 = QHBoxLayout()
        self.hlayout0 = QHBoxLayout()

        self.path_label = QLabel("Path: ", parent=self)
        self.output_label = QLabel("Save To: ", parent=self)
        self.version_label = QLabel("Version: ", parent=self)
        self.comment_label = QLabel("Comment: ", parent=self)
        self.announce_label = QLabel("Trackers: ", parent=self)
        self.web_seed_label = QLabel("Web-Seeds: ", parent=self)
        self.source_label = QLabel("Source: ", parent=self)
        self.piece_length_label = QLabel("Piece Size: ", parent=self)

        self.path_input = QLineEdit(parent=self)
        self.output_input = QLineEdit(parent=self)
        self.source_input = QLineEdit(parent=self)
        self.comment_input = QLineEdit(parent=self)

        self.announce_input = QPlainTextEdit(parent=self)
        self.web_seed_input = QPlainTextEdit(parent=self)
        self.piece_length = ComboBox.piece_length(parent=self)
        self.private = QCheckBox("Private", parent=self)
        self.submit_button = SubmitButton("Create Torrent", parent=self)
        self.browse_dir_button = BrowseDirButton(parent=self)
        self.browse_file_button = BrowseFileButton(parent=self)
        self.output_button = OutButton(parent=self)
        self.v1button = QRadioButton("v1 (default)", parent=self)
        self.v1button.setChecked(True)

        self.v2button = QRadioButton("v2", parent=self)
        self.hybridbutton = QRadioButton("v1+2 (hybrid)", parent=self)
        self.spacer1 = QSpacerItem(150, 0)
        self.spacer2 = QSpacerItem(70, 0)

        sizePolicy = self.path_input.sizePolicy()
        sizePolicy.setHorizontalPolicy(QSizePolicy.Policy.MinimumExpanding)

        self.announce_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.web_seed_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.path_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.path_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.path_input.setSizePolicy(sizePolicy)
        self.output_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.output_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.source_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.source_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.comment_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.comment_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.piece_length_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.hlayout1.addWidget(self.path_input)
        self.hlayout0.addWidget(self.v1button)
        self.hlayout0.addWidget(self.v2button)
        self.hlayout0.addWidget(self.hybridbutton)
        self.hlayout1.addWidget(self.browse_dir_button)
        self.hlayout1.addWidget(self.browse_file_button)
        self.hlayout2.addWidget(self.piece_length)
        self.hlayout2.addItem(self.spacer1)
        self.hlayout2.addWidget(self.private)
        self.hlayout2.addItem(self.spacer2)
        self.hlayout3.addWidget(self.output_input)
        self.hlayout3.addWidget(self.output_button)

        self.layout.addWidget(self.path_label, 0, 0, 1, 1)
        self.layout.addLayout(self.hlayout1, 0, 1, 1, 3)
        self.layout.addWidget(self.output_label, 1, 0, 1, 1)
        self.layout.addLayout(self.hlayout3, 1, 1, 1, 3)
        self.layout.addWidget(self.source_label, 2, 0, 1, 1)
        self.layout.addWidget(self.source_input, 2, 1, 1, 3)
        self.layout.addWidget(self.comment_label, 3, 0, 1, 1)
        self.layout.addWidget(self.comment_input, 3, 1, 1, 3)
        self.layout.addWidget(self.announce_label, 4, 0, 1, 1)
        self.layout.addWidget(self.announce_input, 4, 1, 1, 3)
        self.layout.addWidget(self.web_seed_label, 5, 0, 1, 1)
        self.layout.addWidget(self.web_seed_input, 5, 1, 1, 3)
        self.layout.addWidget(self.piece_length_label, 6, 0, 1, 1)
        self.layout.addWidget(self.version_label, 7, 0, 1, 1)
        self.layout.addLayout(self.hlayout2, 6, 1, 1, 3)
        self.layout.addLayout(self.hlayout0, 7, 1, 1, 3)
        self.layout.addWidget(self.submit_button, 8, 0, 1, 4)
        for i in range(1, self.layout.columnCount()):
            self.layout.setColumnStretch(i, 1)
        self.layout.setObjectName("createWidget_formLayout")
        self.hlayout2.setObjectName("createWidget_hlayout2")
        self.submit_button.setObjectName("createWidget_submit_button")
        self.private.setObjectName("createWidget_private")
        self.path_label.setObjectName("createWidget_path_label")
        self.path_input.setObjectName("createWidget_path_input")
        self.piece_length.setObjectName("createWidget_piece_length")
        self.piece_length_label.setObjectName("createWidgetPiece_lengthLabel")
        self.source_label.setObjectName("createWidget_source_label")
        self.source_input.setObjectName("createWidget_source_input")
        self.announce_input.setObjectName("createWidget_announce_input")
        self.announce_label.setObjectName("createWidget_announce_label")
        self.comment_input.setObjectName("createWidget_comment_input")
        self.comment_label.setObjectName("createWidget_comment_label")
        self.browse_dir_button.setObjectName("createWidget_browsedir_button")
        self.browse_file_button.setObjectName("createWidget_browsefile_button")


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
        self.window = parent.window
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
        self.window.statusBar().showMessage("Processing", 3000)

    def updateStatusBarEnd(self):
        """Update the status bar when torrent creation is complete."""
        self.window.statusBar().showMessage("Completed", 3000)


class OutButton(QPushButton):
    """Button widget."""

    def __init__(self, parent=None):
        """Construct for file picker for outfile button."""
        super().__init__(parent=parent)
        self.window = parent.window
        self.widget = parent
        self.setText("File")
        self.setProperty("createButton", "true")
        self.setIcon(QIcon(get_icon("browse_file")))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.output)

    def output(self, outpath=None):
        """Assign output path for created torrent file."""
        if not outpath:  # pragma: no cover
            outpath, _ = QFileDialog.getSaveFileName(
                parent=self,
                caption="Save as...",
                dir=str(Path.home()),
                filter="*.torrent",
                selectedFilter="",
            )
        if outpath:
            self.widget.output_input.clear()
            self.parent().output_input.setText(outpath)
            self.parent().outpath = outpath


class BrowseFileButton(QPushButton):
    """Button widget for browse."""

    def __init__(self, parent=None):
        """Public constructor for browsebutton class."""
        super().__init__(parent)
        self.setProperty("createButton", "true")
        self.setIcon(QIcon(get_icon("browse_file")))
        self.setText("File")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.browse)
        self.window = parent

    def browse(self, paths=None):
        """
        Browse performed when user presses button.

        Opens File/Folder Dialog.
        """
        paths = browse_files(self, paths)
        if not paths:
            return  # pragma: nocover
        self.window.path_input.clear()
        self.window.output_input.clear()
        self.window.path_input.setText(paths[0])
        self.window.output_input.setText(paths[0] + ".torrent")
        piece_length = path_piece_length(paths[0])
        if piece_length < (2**20):
            val = f"{piece_length//(2**10)} KiB"
        else:
            val = f"{piece_length//(2**20)} MiB"  # pragma: nocover
        for i in range(self.window.piece_length.count()):
            if self.window.piece_length.itemText(i) == val:
                self.window.piece_length.setCurrentIndex(i)
                break


class BrowseDirButton(QPushButton):
    """Browse filesystem folders for path."""

    def __init__(self, parent=None):
        """Construct for folder browser button."""
        super().__init__(parent=parent)
        self.setText("Folder")
        self.setIcon(QIcon(get_icon("browse_folder")))
        self.window = parent
        self.setProperty("createButton", "true")
        self.clicked.connect(self.browse)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def browse(self, path=None):
        """
        Browse action performed when user presses button.

        Opens File/Folder Dialog.
        """
        path = browse_folder(self, path)
        if not path:
            return  # pragma: nocover
        self.window.path_input.clear()
        self.window.output_input.clear()
        self.window.path_input.setText(path)
        self.window.output_input.insert(path + ".torrent")
        piece_length = path_piece_length(path)
        if piece_length < (2**20):
            val = f"{piece_length//(2**10)} KiB"
        else:  # pragma: no cover
            val = f"{piece_length//(2**20)} MiB"
        for i in range(self.window.piece_length.count()):
            if self.window.piece_length.itemText(i) == val:
                self.window.piece_length.setCurrentIndex(i)
                break


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
