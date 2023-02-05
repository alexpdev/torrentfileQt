#! /usr/bin/python3
# -_- coding: utf-8 -_-

##############################################################################
# Copyright 2020 AlexPDev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# <http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################
"""Rebuild module."""

import os

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
                               QPushButton, QTextBrowser, QVBoxLayout, QWidget)
from torrentfile.rebuild import Assembler

from torrentfileQt.utils import (browse_folder, browse_torrent, clean_list,
                                 get_icon, torrent_filter)


class RebuildWidget(QWidget):
    """Rebuild Tab widget."""

    def __init__(self, parent=None):
        """Rebuild a torrent file contents."""
        super().__init__(parent=parent)
        self.centralWidget = QWidget(self)
        self.centralLayout = QVBoxLayout(self)
        mainLabel = QLabel("Rebuild Torrents")
        mainLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLabel.setObjectName("rebuildMainLabel")
        self.centralLayout.addWidget(mainLabel)
        self.centralLayout.addWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        self.setObjectName("rebuildTab")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.torrent_label = QLabel("Torrent File(s)/Folder(s)", self)
        self.torrent_file_button = QPushButton("Select File(s)", self)
        self.torrent_folder_button = QPushButton("Select Folder(s)", self)
        self.torrent_folder_button.setIcon(get_icon("browse_folder"))
        self.torrent_file_button.setIcon(get_icon("browse_file"))
        self.torrent_edit = QPlainTextEdit(parent=self)
        self.torrent_edit.setFixedHeight(85)
        self.content_label = QLabel("Content Path(s)")
        self.content_folder_button = QPushButton("Select Folder(s)", self)
        self.content_folder_button.setIcon(get_icon("browse_folder"))
        self.content_edit = QPlainTextEdit(parent=self)
        self.content_edit.setFixedHeight(85)
        self.dest_label = QLabel("Destination Path")
        self.dest_line_edit = QLineEdit(parent=self)
        self.dest_line_edit.setProperty("infoLine", True)
        self.dest_folder_button = QPushButton("Select Folder", self)
        self.dest_folder_button.setIcon(get_icon("browse_folder"))
        self.submit_button = QPushButton("Rebuild", self)
        self.hlayout1 = QHBoxLayout()
        self.hlayout2 = QHBoxLayout()
        self.hlayout3 = QHBoxLayout()
        self.vlayout1 = QVBoxLayout()
        self.vlayout2 = QVBoxLayout()
        self.hlayout1.addWidget(self.torrent_label)
        self.hlayout1.addWidget(self.torrent_file_button)
        self.hlayout1.addWidget(self.torrent_folder_button)
        self.hlayout2.addWidget(self.content_label)
        self.hlayout2.addWidget(self.content_folder_button)
        self.vlayout1.addLayout(self.hlayout1)
        self.vlayout1.addWidget(self.torrent_edit)
        self.vlayout2.addLayout(self.hlayout2)
        self.vlayout2.addWidget(self.content_edit)
        self.hlayout3.addWidget(self.dest_label)
        self.hlayout3.addWidget(self.dest_line_edit)
        self.hlayout3.addWidget(self.dest_folder_button)
        self.textBrowser = QTextBrowser(parent=self)
        self.layout.addLayout(self.vlayout1)
        self.layout.addLayout(self.vlayout2)
        self.layout.addLayout(self.hlayout3)
        self.layout.addWidget(self.textBrowser)
        self.layout.addWidget(self.submit_button)
        self.torrent_file_button.clicked.connect(self.torrent_file_click)
        self.torrent_folder_button.clicked.connect(self.torrent_folder_click)
        self.content_folder_button.clicked.connect(self.content_folder_click)
        self.dest_folder_button.clicked.connect(self.dest_folder_click)
        self.submit_button.clicked.connect(self.rebuild_click)

    def torrent_file_click(self, paths=None):  # pragma: nocover
        """Browse for for files paths for torrents."""
        paths = torrent_filter(browse_torrent(self))
        current = self.torrent_edit.toPlainText().split("\n")
        output = "\n".join(clean_list(current + paths))
        self.torrent_edit.setPlainText(output)

    def torrent_folder_click(self, path=None):  # pragma: nocover
        """Browse for for folder paths for torrents."""
        path = browse_folder(self)
        paths = [os.path.join(path, x) for x in os.listdir(path)]
        current = self.torrent_edit.toPlainText().split("\n")
        output = "\n".join(clean_list(torrent_filter(paths) + current))
        self.torrent_edit.setPlainText(output)

    def content_folder_click(self, path=None):  # pragma: nocover
        """Browse for for folder paths for torrent contents."""
        path = browse_folder(self)
        current = self.content_edit.toPlainText().split("\n")
        output = "\n".join(clean_list(current + [path]))
        self.content_edit.setPlainText(output)

    def dest_folder_click(self, path=None):  # pragma: nocover
        """Browse for for destination destination folder path."""
        path = browse_folder(self)
        self.dest_line_edit.setText(path)

    def log_message(self, text: str):  # pragma: nocover
        """Post log message to the textbrowser."""
        current = self.textBrowser.toPlainText()
        current += "\n" + text
        self.textBrowser.setPlainText(current)

    def rebuild_click(self):  # pragma: nocover
        """Submit the data and start the Assembler."""
        torrent_paths = self.torrent_edit.toPlainText().split("\n")
        content_paths = self.content_edit.toPlainText().split("\n")
        target_path = self.dest_line_edit.text().strip()
        self.thread = Thread(torrent_paths, content_paths, target_path)
        self.thread.messageLogged.connect(self.log_message)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()


class Thread(QThread):
    """Rebuild assembler thread."""

    messageLogged = Signal(str)

    def __init__(self, metafiles, contents, dest):  # pragma: nocover
        """Build the thread object for the torrent rebuild assembler."""
        super().__init__()
        self.metafiles = metafiles
        self.contents = contents
        self.dest = dest

    def callback(self, message: str):  # pragma: nocover
        """Send signal containing messages from the assembler."""
        self.messageLogged.emit(message)

    def run(self):  # pragma: nocover
        """Run the assembler."""
        Assembler.set_callback(self.callback)
        self.assembler = Assembler(self.metafiles, self.contents, self.dest)
        self.assembler.assemble_torrents()
