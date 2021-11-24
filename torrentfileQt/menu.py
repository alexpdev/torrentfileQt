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
"""Module for the menu bar."""

import os
import webbrowser
from pathlib import Path

import pyben
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QFileDialog, QMenu, QMenuBar

# from .qss import menuSheet


class Menu(QMenu):
    """Menu item for MenuBar widget."""

    def __init__(self, text, parent=None):
        """Constructor for Menu Widget."""
        super().__init__(text, parent=parent)
        self.menubar = parent
        self.txt = text
        font = self.font()
        self.setObjectName(text)
        font.setPointSize(12)
        self.setFont(font)


class MenuBar(QMenuBar):
    """Main menu bar for top level menu of program."""

    def __init__(self, parent=None):
        """Constructor for top level widgets."""
        super().__init__(parent=parent)
        self.window = parent
        # self.setStyleSheet(menuSheet)
        self.file_menu = Menu("File")
        self.help_menu = Menu("Help")
        self.addMenu(self.file_menu)
        self.addMenu(self.help_menu)
        self.actionExport = QAction(self.window)
        self.actionExit = QAction(self.window)
        self.actionAbout = QAction(self.window)
        self.actionDocs = QAction(self.window)
        self.actionRepo = QAction(self.window)
        self.actionRepo.setText("Github Repository")
        self.actionExit.setText("Exit")
        self.actionAbout.setText("About")
        self.actionDocs.setText("Documentation")
        self.actionExport.setText("Save to")
        self.file_menu.addAction(self.actionExit)
        self.file_menu.addAction(self.actionExport)
        self.help_menu.addAction(self.actionAbout)
        self.help_menu.addAction(self.actionDocs)
        self.help_menu.addAction(self.actionRepo)
        self.actionExit.triggered.connect(self.exit_app)
        self.actionAbout.triggered.connect(self.about_qt)
        self.actionExport.triggered.connect(self.export)
        self.actionDocs.triggered.connect(documentation)
        self.actionRepo.triggered.connect(repository)
        self.actionDocs.setObjectName("actionDocs")
        self.actionExit.setObjectName("actionExit")
        self.actionAbout.setObjectName("actionAbout")
        self.actionExport.setObjectName("actionExport")

    def export(self, path=None):
        """Export data from info widget to file."""
        home = str(Path.home())
        if path:
            filename = path
        else:  # pragma: no cover
            filename = QFileDialog.getSaveFileName(
                caption="Save location:", directory=home
            )
        if os.path.exists(os.path.dirname(filename)):
            widget = self.window.central.infoWidget
            path = widget.pathEdit.text()
            if os.path.exists(path):
                data = pyben.load(path)
                with open(filename, "wt") as fd:
                    fd.write(str(data))

    def about_qt(self):
        """Open the about qt menu."""
        self.window.app.aboutQt()  # pragma: nocover

    def exit_app(self):
        """Close application."""
        self.parent().app.quit()  # pragma: nocover


def documentation():  # pragma: no cover
    """Open webbrowser to TorrentFileQt documentation."""
    webbrowser.open_new_tab("https://alexpdev.github.io/torrentfile")


def repository():  # pragma: no cover
    """Open webbrowser to GitHub Repo."""
    webbrowser.open_new_tab("https://github.com/alexpdev/torrentfileQt")
