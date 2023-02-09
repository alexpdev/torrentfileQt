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
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFileDialog, QGridLayout,
                               QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                               QPlainTextEdit, QProgressBar, QPushButton,
                               QRadioButton, QSplitter, QTableWidget,
                               QTableWidgetItem, QVBoxLayout, QWidget)
from torrentfile.torrent import TorrentFile, TorrentFileHybrid, TorrentFileV2
from torrentfile.utils import path_piece_length

from torrentfileQt.utils import (DropGroupBox, browse_files, browse_folder,
                                 get_icon)


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
        self.centralLayout.setContentsMargins(0, 1, 0, 1)
        self.centralWidget = QWidget()
        self.centralWidget.setAcceptDrops(True)
        self.centralWidget.setAttribute(Qt.WA_StyledBackground, True)
        self.centralWidget.setObjectName("CreateCentralWidget")
        mainLabel = QLabel("Torrent Creator")
        mainLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLabel.setObjectName("createMainLabel")
        self.centralLayout.addWidget(mainLabel)
        self.layout = QVBoxLayout(self.centralWidget)

        self.path_group = DropGroupBox(parent=self)
        self.path_group.setObjectName("CreatePathGroup")
        self.path_group.setTitle("Content")
        self.path_group.setLabelText("drag & drop file/folder here or ...")
        self.path_dir_button = BrowseDirButton(parent=self)
        self.path_dir_button.folderSelected.connect(self.setPath)
        self.path_file_button = BrowseFileButton(parent=self)
        self.path_file_button.fileSelected.connect(self.setPath)
        self.path_group.addButton(self.path_dir_button)
        self.path_group.addButton(self.path_file_button)
        self.path_group.pathSelected.connect(self.setPath)

        versionBox = QGroupBox(self)
        versionBox.setObjectName("CreateVersionBox")
        piece_length_box = QGroupBox(self)
        piece_length_box.setObjectName("CreatePieceLength")
        piece_length_box.setTitle("Torrent Piece Length")
        versionBox.setTitle("Version/Private/Piece Length")
        self.v1button = QRadioButton("v1 (default)", parent=self)
        self.v1button.setChecked(True)
        self.v2button = QRadioButton("v2", parent=self)
        self.hybridbutton = QRadioButton("v1+2 (hybrid)", parent=self)
        self.piece_length_combo = ComboBox.piece_length(parent=self)
        self.private = QCheckBox("Private", parent=self)

        versionBox.setToolTip("These controls may be ignored if you do not"
                              " have a specific need to adjust them.")

        layout0 = QGridLayout(versionBox)
        layout0.addWidget(self.v1button, 0, 0)
        layout0.addWidget(self.v2button, 1, 0)
        layout0.addWidget(self.hybridbutton, 2, 0)
        layout0.addWidget(self.private, 0, 1)
        layout0.addWidget(piece_length_box, 1, 1, 2, 1)

        vlayout4 = QVBoxLayout(piece_length_box)
        vlayout4.addWidget(self.piece_length_combo)

        hlayout0 = QHBoxLayout()
        hlayout0.addWidget(self.path_group)
        hlayout0.addWidget(versionBox)

        output_label = QLabel("Save Path", parent=self)
        output_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.output_path_edit = QLineEdit(parent=self)
        self.output_button = OutButton(parent=self)
        hlayout3 = QHBoxLayout()
        hlayout3.addWidget(self.output_path_edit)
        hlayout3.addWidget(self.output_button)

        source_label = QLabel("Source", parent=self)
        source_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.source_edit = QLineEdit(parent=self)
        self.source_edit.setToolTip(
            "Leave empty unless you have a need to fill it.")

        comment_label = QLabel("Comment", parent=self)
        comment_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.comment_edit = QLineEdit(parent=self)

        hlayout1 = QHBoxLayout()
        vlayout0 = QVBoxLayout()
        vlayout1 = QVBoxLayout()
        vlayout0.addWidget(source_label)
        vlayout0.addWidget(self.source_edit)
        vlayout1.addWidget(comment_label)
        vlayout1.addWidget(self.comment_edit)
        hlayout1.addLayout(vlayout0)
        hlayout1.addLayout(vlayout1)

        announce_label = QLabel("Trackers: ", parent=self)
        announce_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.announce_input = QPlainTextEdit(parent=self)
        self.announce_input.setToolTip(
            "One per line - Examples: \nhttp://example1.net/announce\nhttp://"
            "example2.org/announce")

        web_seed_label = QLabel("Web-Seeds: ", parent=self)
        web_seed_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.web_seed_input = QPlainTextEdit(parent=self)
        self.web_seed_input.setToolTip(
            "One per line - Examples: \nftp://example1.net/path/to/"
            "content\nhttp://example2.org/path/to/content")

        hlayout2 = QHBoxLayout()
        vlayout2 = QVBoxLayout()
        vlayout3 = QVBoxLayout()
        vlayout2.addWidget(announce_label)
        vlayout2.addWidget(self.announce_input)
        vlayout3.addWidget(web_seed_label)
        vlayout3.addWidget(self.web_seed_input)
        hlayout2.addLayout(vlayout2)
        hlayout2.addLayout(vlayout3)

        self.submit_button = SubmitButton("Create Torrent", parent=self)
        self.submit_button.dataCollected.connect(self.write_torrent)
        self.submit_button.setObjectName("CreateSubmitButton")

        self.bottomCentral = QWidget()
        self.bottomLayout = QVBoxLayout(self.bottomCentral)
        self.progress_tree = ProgressTable(self)
        self.bottomLayout.addWidget(self.progress_tree)
        self.layout.addLayout(hlayout0)
        self.layout.addWidget(output_label)
        self.layout.addLayout(hlayout3)
        self.layout.addLayout(hlayout1)
        self.layout.addLayout(hlayout2)
        self.layout.addWidget(self.submit_button)
        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.centralWidget)
        self.splitter.addWidget(self.bottomCentral)
        self.centralLayout.addWidget(self.splitter)

    def setPath(self, path: str):
        """Set the path of the torrent content."""
        piece_length = path_piece_length(path)
        if piece_length < (2**20):
            val = f"{piece_length//(2**10)} KiB"
        else:
            val = f"{piece_length//(2**20)} MiB"  # pragma: nocover
        self.path_group.setPath(path)
        self.piece_length_combo.setValue(val)
        self.output_path_edit.setText(path + ".torrent")

    def write_torrent(self, args, creator):
        """
        Start the torrent creator.
        """
        self._thread = TorrentFileCreator(args, creator)
        self._thread.created.connect(self.updateStatusBarEnd)
        self._thread.prog_start_signal.connect(self.progress_tree.prog_start)
        self._thread.prog_update_signal.connect(self.progress_tree.prog_update)
        self._thread.start()

    def updateStatusBarEnd(self):
        """Update the status bar when torrent creation is complete."""
        self.window().statusBar().showMessage("Completed", 3000)
        self._thread.deleteLater()


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
    prog_start_signal = Signal(list)
    prog_update_signal = Signal(int, str)
    prog_close_signal = Signal()

    def __init__(self, args, creator):
        """Construct the new thread."""
        super().__init__()
        self.args = args
        self.creator = creator
        self.creator.hasher.prog_start = self.prog_start
        self.creator.hasher.prog_update = self.prog_update
        self.creator.hasher.prog_close = self.prog_close
        self.current = None

    def prog_start(self, total, path, **_):
        """
        Progress start signal.
        """
        self.current = path
        self.prog_start_signal.emit([total, path])

    def prog_update(self, val):
        """
        Progress update signal.
        """
        self.prog_update_signal.emit(val, self.current)

    def prog_close(self):
        """
        Progress stopped signal.
        """
        self.prog_close_signal.emit()

    def run(self):
        """Create a torrent file and emit it's path."""
        args = deepcopy(self.args)
        torrent = self.creator(**args)
        _, _ = torrent.write()
        self.created.emit()


class SubmitButton(QPushButton):
    """Button widget."""

    dataCollected = Signal(dict, object)

    def __init__(self, text: str, parent: QWidget = None) -> None:
        """
        Construct the submit button.

        Parameters
        ----------
        text : str
            Text displayed on the button itself.
        parent : QWidget
            The tab widget parent. default = None
        """
        super().__init__(text, parent=parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("CreateSubmitButton")
        self.setText(text)
        self.clicked.connect(self.submit)
        self._parent = parent
        self.thread = None

    def submit(self):
        """Submit Action performed when user presses Submit Button."""
        parent = self._parent
        # Gather Information from other Widgets.
        args = {}
        if parent.private.isChecked():
            args["private"] = 1

        # add source to metadata
        sourcetext = parent.source_edit.text()
        if sourcetext:
            args["source"] = sourcetext

        # add comments to metadata
        commenttext = parent.comment_edit.text()
        if commenttext:
            args["comment"] = commenttext

        # at least 1 tracker input is required
        announce = parent.announce_input.toPlainText()
        announce = [i.strip() for i in announce.split("\n") if i]
        if announce:
            args["announce"] = announce

        url_list = parent.web_seed_input.toPlainText()
        url_list = [i.strip() for i in url_list.split("\n") if i]
        if url_list:
            args["url_list"] = url_list

        # Calculates piece length if not specified by user.
        outtext = os.path.realpath(parent.output_path_edit.text())
        if outtext:
            args["outfile"] = outtext

        current = parent.piece_length_combo.currentIndex()
        if current:
            piece_length = parent.piece_length_combo.itemData(current)
            args["piece_length"] = piece_length

        if parent.hybridbutton.isChecked():
            creator = TorrentFileHybrid
        elif parent.v2button.isChecked():
            creator = TorrentFileV2
        else:
            creator = TorrentFile

        args["path"] = parent.path_group.getPath()
        tree = parent.progress_tree
        tree.add_args(args)
        self.dataCollected.emit(args, creator)


class OutButton(QPushButton):
    """Button widget."""

    savePathSelected = Signal(str)

    def __init__(self, parent=None):
        """Construct for file picker for outfile button."""
        super().__init__(parent=parent)
        self.setText("Select Save Path")
        self.setIcon(get_icon("browse_file"))
        self.setObjectName("CreateOutButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.output)

    def output(self):  # pragma: nocover
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

    def browse(self):
        """
        Browse action performed when user presses button.

        Opens File/Folder Dialog.
        """
        path = browse_folder(self)
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


class ProgressTable(QTableWidget):
    """
    Table widget that keep track of torrent creation process.
    """

    def __init__(self, parent=None):
        """
        Construc the table widget.
        """
        super().__init__(parent=parent)
        self.setColumnCount(2)
        self.verticalHeader().setHidden(True)
        self.setHorizontalHeaderLabels(["Path", "Progress"])
        self.setObjectName("CreateProgressTable")
        self.max_chars = 70
        hheader = self.horizontalHeader()
        hheader.setSectionResizeMode(0, hheader.ResizeMode.ResizeToContents)
        hheader.setSectionResizeMode(1, hheader.ResizeMode.Stretch)
        hheader.setSectionsClickable(False)

    def add_args(self, args):
        """
        Add arguments needed for tracking creation process.
        """
        self.path = args["path"]

    def prog_start(self, values):
        """
        Create the path and progress bar.
        """
        total, path = values
        index = self.rowCount()
        self.insertRow(index)
        item = QTableWidgetItem()
        item._path = path
        if len(path) > self.max_chars:
            path = "..." + path[-self.max_chars:]
        item.setText(path)
        progbar = QProgressBar()
        if total < 1 << 30:
            progbar._total = total
            progbar._divisor = 1
            progbar._max = total
        else:  # pragma: nocover
            progbar._total = total
            progbar._divisor = 2 << 10
            progbar._max = total // (2 << 10)
        progbar.setRange(0, progbar._max - 1)
        self.setItem(index, 0, item)
        self.setCellWidget(index, 1, progbar)
        self.scrollToBottom()

    def prog_update(self, value, path):
        """Update the progress bar."""
        i = self.rowCount() - 1
        while i >= 0:
            if self.item(i, 0)._path == path:
                progbar = self.cellWidget(i, 1)
                current = progbar.value()
                increment = value // progbar._divisor
                progbar.setValue(current + increment)
                return
            i -= 1  # pragma: nocover
