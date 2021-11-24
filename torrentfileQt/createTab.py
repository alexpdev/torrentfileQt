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
import shutil
import subprocess  # nosec

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QCheckBox, QComboBox, QFileDialog, QGridLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
                             QPushButton, QRadioButton, QSpacerItem,
                             QToolButton, QWidget)
from torrentfile.utils import path_stat

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

        self.path_label = Label("Path: ", parent=self)
        self.output_label = Label("Save Path: ", parent=self)
        self.version_label = Label("Meta Version: ", parent=self)
        self.comment_label = Label("Comment: ", parent=self)
        self.announce_label = Label("Trackers: ", parent=self)
        self.source_label = Label("Source: ", parent=self)
        self.piece_length_label = Label("Piece Length: ", parent=self)

        self.path_input = LineEdit(parent=self)
        self.output_input = LineEdit(parent=self)
        self.source_input = LineEdit(parent=self)
        self.comment_input = LineEdit(parent=self)

        self.announce_input = PlainTextEdit(parent=self)
        self.piece_length = ComboBox(parent=self)
        self.private = CheckBox("Private", parent=self)
        self.submit_button = SubmitButton("Create Torrent", parent=self)
        self.browse_dir_button = BrowseDirButton(parent=self)
        self.browse_file_button = BrowseFileButton(parent=self)
        self.output_button = OutButton(parent=self)
        self.v1button = QRadioButton("v1 (default)", parent=self)
        self.v1button.setChecked(True)

        self.v2button = QRadioButton("v2", parent=self)
        self.hybridbutton = QRadioButton("v1+2 (hybrid)", parent=self)
        self.spacer = QSpacerItem(50, 0)

        self.path_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.path_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.output_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.output_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.source_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.source_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.comment_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.comment_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.announce_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.piece_length_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.hlayout0.addWidget(self.v1button)
        self.hlayout0.addWidget(self.v2button)
        self.hlayout0.addWidget(self.hybridbutton)
        self.hlayout1.addWidget(self.browse_dir_button)
        self.hlayout1.addWidget(self.browse_file_button)
        self.hlayout2.addWidget(self.piece_length)
        self.hlayout2.addItem(self.spacer)
        self.hlayout2.addWidget(self.private)
        self.hlayout3.addWidget(self.output_input)
        self.hlayout3.addWidget(self.output_button)

        self.layout.addWidget(self.path_label, 0, 0, 2, 1)
        self.layout.addWidget(self.path_input, 0, 1, 1, 3)
        self.layout.addLayout(self.hlayout1, 1, 1, 1, 3)
        self.layout.addWidget(self.version_label, 4, 0, 1, 1)
        self.layout.addLayout(self.hlayout0, 4, 1, 1, 3)
        self.layout.addWidget(self.piece_length_label, 3, 0, 1, 1)
        self.layout.addLayout(self.hlayout2, 3, 1, 1, 3)
        self.layout.addWidget(self.output_label, 2, 0, 1, 1)
        self.layout.addLayout(self.hlayout3, 2, 1, 1, 3)
        self.layout.addWidget(self.source_label, 5, 0, 1, 1)
        self.layout.addWidget(self.source_input, 5, 1, 1, 3)
        self.layout.addWidget(self.comment_label, 6, 0, 1, 1)
        self.layout.addWidget(self.comment_input, 6, 1, 1, 3)
        self.layout.addWidget(self.announce_label, 7, 0, 1, 1)
        self.layout.addWidget(self.announce_input, 7, 1, 1, 3)
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


def torrentfile_create(args, obj):  # pragma: no cover
    """
    Create new .torrent file in a seperate thread.

    Args:
        args ([`dict`]): keyword arguements for the torrent creator.
        obj ([`torrentfile.MetaBase`]): The procedure class for creating file.
    """
    tfile = obj(**args)
    tfile.write()


def create_torrent(args):
    """Create torrent file in seperate process."""
    tfexe = shutil.which("torrentfile")
    result = subprocess.run([tfexe, *args])  # nosec
    return result


class SubmitButton(QPushButton):
    """Button widget."""

    def __init__(self, text, parent=None):
        """Public Constructor for Submit Button.

        Args:
            text (str): Text displayed on the button itself.
            parent (QWidget, optional): This Widget's parent. Defaults None.
        """
        super().__init__(text, parent=parent)
        self._text = text
        self.widget = parent
        self.window = parent.window
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setText(text)
        self.pressed.connect(self.submit)

    def submit(self):
        """Submit Action performed when user presses Submit Button."""
        # Gather Information from other Widgets.
        args = []
        if self.widget.private.isChecked():
            args.append("--private")

        # add source to metadata
        sourcetext = self.widget.source_input.text()
        if sourcetext:
            args.extend(["--source", sourcetext])

        # add comments to metadata
        commenttext = self.widget.comment_input.text()
        if commenttext:
            args.extend(["--comment", commenttext])

        # at least 1 tracker input is required
        announce = self.widget.announce_input.toPlainText()
        announce = [i for i in announce.split("\n") if i]
        if announce:
            args.append("-a")
            args.extend(announce)

        # Calculates piece length if not specified by user.
        outtext = os.path.realpath(self.widget.output_input.text())
        if outtext:
            args.extend(["-o", outtext])

        current = self.widget.piece_length.currentIndex()
        if current:
            piece_length_index = self.widget.piece_length.currentIndex()
            piece_length = self.widget.piece_length.itemData(piece_length_index)
            args.extend(["--piece-length", str(piece_length)])

        if self.widget.hybridbutton.isChecked():
            args.extend(["--meta-version", "3"])
        elif self.widget.v2button.isChecked():
            args.extend(["--meta-version", "2"])

        path = self.widget.path_input.text()
        args.append(path)
        result = create_torrent(args)
        if result:
            self.window.statusBar().showMessage("Success")


class OutButton(QToolButton):
    """Button widget."""

    def __init__(self, parent=None):
        """Constructor for file picker for outfile button."""
        super().__init__(parent=parent)
        self.window = parent
        self.setText("...")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pressed.connect(self.output)

    def output(self, outpath=None):
        """Assign output path for created torrent file."""
        caption = "Select Output Directory"
        if not outpath:  # pragma: no cover
            outpath = QFileDialog.getExistingDirectory(
                parent=self, caption=caption
            )
        if outpath:
            self.window.output_input.clear()
            self.parent().output_input.insert(outpath)
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
        self.pressed.connect(self.browse)

    def browse(self, path=None):
        """Browse Action performed when user presses button.

        Opens File/Folder Dialog.

        Returns:
            str: Path to file or folder to include in torrent.
        """
        caption = "Choose File"
        if not path:  # pragma: no cover
            path = QFileDialog.getOpenFileName(parent=self, caption=caption)
        if not isinstance(path, str):  # pragma: no cover
            path = os.path.normpath(path[0])
        else:
            path = os.path.normpath(path)
        self.window.path_input.clear()
        self.window.path_input.insert(path)
        self.window.output_input.clear()
        outdir = os.path.dirname(str(path))
        txt = os.path.split(str(path))[-1]
        outfile = os.path.splitext(txt)[0] + ".torrent"
        outpath = os.path.realpath(os.path.join(outdir, outfile))
        self.window.output_input.insert(outpath)
        _, size, piece_length = path_stat(path)
        if piece_length < (2 ** 20):
            val = f"{piece_length//(2**10)}KB"
        else:
            val = f"{piece_length//(2**20)}MB"  # pragma: no cover
        for i in range(self.window.piece_length.count()):
            if self.window.piece_length.itemText(i) == val:
                self.window.piece_length.setCurrentIndex(i)
                break
        return size


class BrowseDirButton(QPushButton):
    """Browse filesystem folders for path."""

    def __init__(self, parent=None):
        """Constructor for folder browser button."""
        super().__init__(parent=parent)
        self.setText("Select Folder")
        self.window = parent
        self.setStyleSheet(pushButtonEdit)
        self.pressed.connect(self.browse)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def browse(self, filename=None):
        """Browse action performed when user presses button.

        Opens File/Folder Dialog.

        Returns:
            str: Path to file or folder to include in torrent.
        """
        caption = "Choose Root Directory"
        if not filename:  # pragma: no cover
            filename = QFileDialog.getExistingDirectory(
                parent=self, caption=caption
            )
        if filename:
            filename = os.path.realpath(filename)
            self.window.path_input.clear()
            self.window.path_input.insert(filename)
            self.window.output_input.clear()
            outdir = os.path.dirname(str(filename))
            outfile = (
                os.path.splitext(os.path.split(str(filename))[-1])[0]
                + ".torrent"
            )
            outpath = os.path.realpath(os.path.join(outdir, outfile))
            self.window.output_input.insert(outpath)
            try:
                _, _, piece_length = path_stat(filename)
            except PermissionError:  # pragma: no cover
                return
            if piece_length < (2 ** 20):
                val = f"{piece_length//(2**10)}KB"
            else:  # pragma: no cover
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
        # self.setStyleSheet(comboBoxSheet)
        self.addItem("")
        for exp in range(14, 24):
            if exp < 20:
                item = str((2 ** exp) // (2 ** 10)) + "KB"
            else:
                item = str((2 ** exp) // (2 ** 20)) + "MB"
            self.addItem(item, 2 ** exp)
        self.setEditable(False)


class CheckBox(QCheckBox):
    """Checkbox widget."""

    def __init__(self, label, parent=None):
        """Constructor for check box widgit."""
        super().__init__(label, parent=parent)
        # self.setStyleSheet(checkBoxSheet)


class PlainTextEdit(QPlainTextEdit):
    """Text edit widget for trackers."""

    def __init__(self, parent=None):
        """Constructor for plain text edit."""
        super().__init__(parent=parent)
        self.setBackgroundVisible(True)
        # self.setStyleSheet(textEditSheet)


class Label(QLabel):
    """Label Identifier for Window Widgets.

    Subclass: QLabel
    """

    def __init__(self, text, parent=None):
        """Constructor for label widgit."""
        super().__init__(text, parent=parent)
        # self.setStyleSheet(labelSheet)
        font = self.font()
        font.setBold(True)
        font.setPointSize(12)
        self.setFont(font)


class LineEdit(QLineEdit):
    """Line edit widget for input fields."""

    def __init__(self, parent=None):
        """Constructor for line edit widget."""
        super().__init__(parent=parent)
        self.window = parent.window
        # self.setStyleSheet(createLineEditSheet)
        font = self.font()
        font.setPointSize(11)
        self.setFont(font)
