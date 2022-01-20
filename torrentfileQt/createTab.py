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
# import json
import os
from pathlib import Path
from threading import Thread

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFileDialog, QGridLayout,
                               QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
                               QPushButton, QRadioButton, QSpacerItem,
                               QToolButton, QWidget)
from torrentfile import TorrentFile, TorrentFileHybrid, TorrentFileV2
from torrentfile.utils import path_piece_length

from torrentfileQt.qss import pushButtonEdit


class CreateWidget(QWidget):
    """CreateWidget contains all controls for creating a new .torrent file.

    Args:
        QWidget (`QObject`): Parent class to CreateWidget.
    """

    def __init__(self, parent=None):
        """
        Constructor for Create Widget.

        Args:
            parent ([`QWidget`], optional): Parent Widget. Defaults to None.
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
        # self.hlayout4 = QHBoxLayout()

        self.path_label = QLabel("Path: ", parent=self)
        self.output_label = QLabel("Save To: ", parent=self)
        self.version_label = QLabel("Meta Version: ", parent=self)
        self.comment_label = QLabel("Comment: ", parent=self)
        self.announce_label = QLabel("Tracker URLs: ", parent=self)
        # self.profile_label = QLabel("Profile: ", parent=self)
        self.web_seed_label = QLabel("Web-seed URLs:")
        self.source_label = QLabel("Source: ", parent=self)
        self.piece_length_label = QLabel("Piece Size: ", parent=self)

        self.path_input = QLineEdit(parent=self)
        self.output_input = QLineEdit(parent=self)
        self.source_input = QLineEdit(parent=self)
        self.comment_input = QLineEdit(parent=self)

        # self.profile_input = ComboBox.profiles(parent=self)
        self.announce_input = QPlainTextEdit(parent=self)
        self.web_seed_input = QPlainTextEdit(parent=self)
        self.piece_length = ComboBox.piece_length(parent=self)
        self.private = QCheckBox("Private", parent=self)
        self.submit_button = SubmitButton("Create Torrent", parent=self)
        self.browse_dir_button = BrowseDirButton(parent=self)
        self.browse_file_button = BrowseFileButton(parent=self)
        self.output_button = OutButton(parent=self)
        # self.profile_button = ProfileButton(parent=self)
        self.v1button = QRadioButton("v1 (default)", parent=self)
        self.v1button.setChecked(True)

        self.v2button = QRadioButton("v2", parent=self)
        self.hybridbutton = QRadioButton("v1+2 (hybrid)", parent=self)
        self.spacer1 = QSpacerItem(150, 0)
        self.spacer2 = QSpacerItem(70, 0)

        # self.profile_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.path_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.path_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.output_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.output_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.source_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.source_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.comment_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.comment_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.piece_length_label.setAlignment(Qt.AlignmentFlag.AlignRight)

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
        # self.hlayout4.addWidget(self.profile_input)
        # self.hlayout4.addWidget(self.profile_button)

        # self.layout.addWidget(self.profile_label,0,0,1,1)
        # self.layout.addLayout(self.hlayout4,0,1,1,1)
        self.layout.addWidget(self.path_label, 1, 0, 2, 1)
        self.layout.addWidget(self.path_input, 1, 1, 1, 3)
        self.layout.addLayout(self.hlayout1, 2, 1, 1, 3)
        self.layout.addWidget(self.version_label, 5, 0, 1, 1)
        self.layout.addLayout(self.hlayout0, 5, 1, 1, 3)
        self.layout.addWidget(self.piece_length_label, 4, 0, 1, 1)
        self.layout.addLayout(self.hlayout2, 4, 1, 1, 3)
        self.layout.addWidget(self.output_label, 3, 0, 1, 1)
        self.layout.addLayout(self.hlayout3, 3, 1, 1, 3)
        self.layout.addWidget(self.source_label, 9, 0, 1, 1)
        self.layout.addWidget(self.source_input, 9, 1, 1, 3)
        self.layout.addWidget(self.comment_label, 8, 0, 1, 1)
        self.layout.addWidget(self.comment_input, 8, 1, 1, 3)
        self.layout.addWidget(self.announce_label, 6, 0, 1, 1)
        self.layout.addWidget(self.announce_input, 6, 1, 1, 3)
        self.layout.addWidget(self.web_seed_label, 7, 0, 1, 1)
        self.layout.addWidget(self.web_seed_input, 7, 1, 1, 3)
        self.layout.addWidget(self.submit_button, 10, 0, 1, 4)
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


def torrentfile_create(args, creator, name):  # pragma: no cover
    """Create new .torrent file in a seperate thread.

    Parameters
    ----------
    args : `dict`
        keyword arguements for the torrent creator.
    creator : `type`
        The procedure class for creating file.
    name : `list`
        container to add return values to.

    Returns
    -------
    `list`
        container for path to created torrent file.
    """
    torrent = creator(**args)
    outfile, _ = torrent.write()
    name.append(outfile)
    return name


class SubmitButton(QPushButton):
    """Button widget."""

    def __init__(self, text, parent=None):
        """Public Constructor for Submit Button.

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

        # Calculates piece length if not specified by user.
        outtext = os.path.realpath(self.widget.output_input.text())
        if outtext:
            args["outfile"] = outtext

        current = self.widget.piece_length.currentIndex()
        if current:
            piece_length_index = self.widget.piece_length.currentIndex()
            piece_length = self.widget.piece_length.itemData(piece_length_index)
            args["piece_length"] = piece_length

        if self.widget.hybridbutton.isChecked():
            creator = TorrentFileHybrid
        elif self.widget.v2button.isChecked():
            creator = TorrentFileV2
        else:
            creator = TorrentFile

        path = self.widget.path_input.text()
        args["path"] = path
        name = []
        self.thread = Thread(
            group=None, target=torrentfile_create, args=(args, creator, name)
        )
        self.thread.start()
        return self

    def join(self):
        """Join the thread until it completes."""
        self.thread.join()


class OutButton(QToolButton):
    """Button widget."""

    def __init__(self, parent=None):
        """Constructor for file picker for outfile button."""
        super().__init__(parent=parent)
        self.window = parent.window
        self.widget = parent
        self.setText("...")
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
        super().__init__(parent=parent)
        self.setText("Select File")
        self.window = parent
        self.setStyleSheet(pushButtonEdit)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.browse)

    def browse(self, path=None):
        """Browse Action performed when user presses button.

        Opens File/Folder Dialog.

        Returns:
            str: Path to file or folder to include in torrent.
        """
        caption = "Select file..."
        if not path:  # pragma: no cover
            path, _ = QFileDialog.getOpenFileName(
                parent=self, caption=caption, dir=str(Path.home())
            )
        if path != "":
            path = os.path.normpath(path)
            self.window.path_input.clear()
            self.window.output_input.clear()
            self.window.path_input.setText(path)
            self.window.output_input.setText(path + ".torrent")
            piece_length = path_piece_length(path)
            if piece_length < (2 ** 20):
                val = f"{piece_length//(2**10)}KB"
            else:
                val = f"{piece_length//(2**20)}MB"
            for i in range(self.window.piece_length.count()):
                if self.window.piece_length.itemText(i) == val:
                    self.window.piece_length.setCurrentIndex(i)
                    break


# class ProfileButton(QPushButton):
#     """Save the current fields values as a profile."""

#     def __init__(self, parent=None):
#         """Save current fields as a profile."""
#         super().__init__(parent=parent)
#         self.setText("Save Profile")


class BrowseDirButton(QPushButton):
    """Browse filesystem folders for path."""

    def __init__(self, parent=None):
        """Constructor for folder browser button."""
        super().__init__(parent=parent)
        self.setText("Select Folder")
        self.window = parent
        self.setStyleSheet(pushButtonEdit)
        self.clicked.connect(self.browse)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def browse(self, path=None):
        """Browse action performed when user presses button.

        Opens File/Folder Dialog.

        Returns:
            str: Path to file or folder to include in torrent.
        """
        caption = "Select contents folder..."
        if not path:  # pragma: no cover
            path = QFileDialog.getExistingDirectory(
                parent=self, caption=caption, dir=str(Path.home())
            )
        if path:
            path = os.path.realpath(path)
            self.window.path_input.clear()
            self.window.output_input.clear()
            self.window.path_input.setText(path)
            self.window.output_input.insert(path + ".torrent")
            try:
                piece_length = path_piece_length(path)
            except PermissionError:  # pragma: no cover
                return
            if piece_length < (2 ** 20):
                val = f"{piece_length//(2**10)}KB"
            else:
                val = f"{piece_length//(2**20)}MB"
            for i in range(self.window.piece_length.count()):
                if self.window.piece_length.itemText(i) == val:
                    self.window.piece_length.setCurrentIndex(i)
                    break
        return


class ComboBox(QComboBox):
    """Combo box options for selecting piece length."""

    def __init__(self, parent=None):
        """Constructor for ComboBox."""
        super().__init__(parent=parent)
        self.addItem("")
        self.setEditable(False)
        self.profile_data = None

    # @classmethod
    # def profiles(cls, parent=None):
    #     """Create a profiles combobox."""
    #     box = cls(parent=parent)
    #     if os.path.exists(os.path.join(os.getcwd(), "profiles.json")):
    #         with open("profiles.json", "rt") as js:
    #             profs = json.load(js)
    #             box.profile_data = profs
    #             for name in profs:
    #                 box.addItem(name)
    #     return box

    @classmethod
    def piece_length(cls, parent=None):
        """Create a piece_length combobox."""
        box = cls(parent=parent)
        for exp in range(14, 26):
            if exp < 20:
                item = str((2 ** exp) // (2 ** 10)) + "KB"
            else:
                item = str((2 ** exp) // (2 ** 20)) + "MB"
            box.addItem(item, 2 ** exp)
        return box
