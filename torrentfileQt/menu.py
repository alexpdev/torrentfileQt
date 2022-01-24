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
import json
import webbrowser

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QMenuBar


class Menu(QMenu):
    """Menu item for MenuBar widget."""

    def __init__(self, text, parent=None):
        """Constructor for Menu Widget."""
        super().__init__(text, parent=parent)
        self.menubar = parent
        self.txt = text
        font = self.font()
        self.setObjectName(text + "MenuObject")
        font.setPointSize(10)
        self.setFont(font)


class MenuBar(QMenuBar):
    """Main menu bar for top level menu of program."""

    def __init__(self, parent=None):
        """Constructor for top level widgets."""
        super().__init__(parent=parent)
        self.window = parent
        self.file_menu = Menu("File")
        self.help_menu = Menu("Help")
        self.profile_menu = Menu("Profiles")
        self.addMenu(self.file_menu)
        self.addMenu(self.help_menu)
        self.addMenu(self.profile_menu)
        self.actionExit = QAction(self.window)
        self.actionAbout = QAction(self.window)
        self.actionDocs = QAction(self.window)
        self.actionRepo = QAction(self.window)
        self.actionAddProfile = QAction(self.window)
        self.actionRepo.setText("Github Repository")
        self.actionExit.setText("Exit")
        self.actionAbout.setText("About")
        self.actionDocs.setText("Documentation")
        self.actionAddProfile.setText("Add Profile")
        self.home = os.path.join(os.path.expanduser("~"), ".torrentfileQt")
        self.profile_actions = []
        if os.path.exists(self.home):
            profiles_path = os.path.join(self.home, "profiles.json")
            if os.path.exists(profiles_path):
                with open(profiles_path, "rt") as jsonfile:
                    profiles = json.load(jsonfile)
                for profile in profiles:
                    action = QAction(self.window)
                    action.setText(profile)
                    action.name = profile
                    self.profile_menu.addAction(action)
                    self.profile_actions.append(action)
        self.file_menu.addAction(self.actionExit)
        self.help_menu.addAction(self.actionAbout)
        self.help_menu.addAction(self.actionDocs)
        self.help_menu.addAction(self.actionRepo)
        self.profile_menu.addAction(self.actionAddProfile)
        self.actionExit.triggered.connect(self.exit_app)
        self.actionAbout.triggered.connect(self.about_qt)
        self.actionDocs.triggered.connect(documentation)
        self.actionRepo.triggered.connect(repository)
        self.actionAddProfile.triggered.connect(self.add_profile)
        self.actionDocs.setObjectName("actionDocs")
        self.actionAddProfile.setObjectName("actionAddProfile")
        self.actionExit.setObjectName("actionExit")
        self.actionAbout.setObjectName("actionAbout")

    def about_qt(self):
        """Open the about qt menu."""
        self.window.app.aboutQt()  # pragma: nocover

    def exit_app(self):
        """Close application."""
        self.parent().app.quit()  # pragma: nocover

    def add_profile(self):
        """Add a profile."""


def documentation():  # pragma: no cover
    """Open webbrowser to TorrentFileQt documentation."""
    webbrowser.open_new_tab("https://alexpdev.github.io/torrentfile")


def repository():  # pragma: no cover
    """Open webbrowser to GitHub Repo."""
    webbrowser.open_new_tab("https://github.com/alexpdev/torrentfileQt")
