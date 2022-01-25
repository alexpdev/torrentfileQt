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
from PySide6.QtWidgets import QMenu, QMenuBar, QInputDialog


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


class ProfileAction:
    """Store the name and action taken when this menu button is triggered.

    Parameters
    ----------
    name : `str`
        name of the profile and menubutton
    action : `QAction`
        Action associated with the name
    parent : `QMenu`
        the menu which holds the action
    """

    def __init__(self, name, action, parent):
        """Initialize ProfileAction class."""
        self.name = name
        self.action = action
        self.parent = parent
        self.action.triggered.connect(self.trigger)

    def trigger(self):
        """Fill the create tab with saved values in profile."""
        with open(self.parent.profiles, "rt") as jsonfile:
            profiles = json.load(jsonfile)
        profile = profiles[self.name]
        tab = self.parent.window.central.createWidget
        tab.source_input.setText(profile["source"])
        tab.announce_input.insertPlainText("\n".join(profile["trackers"]))
        tab.web_seed_input.insertPlainText("\n".join(profile["web_seeds"]))
        if profile["version"] == 3:
            tab.hybridbutton.click()
        elif profile["version"] == 2:
            tab.v2button.click()
        else:
            tab.v1button.click()
        if profile["private"]:
            tab.private.click()
        if profile["piece_length"]:
            for i in range(tab.piece_length.count()):
                if tab.piece_length.itemData(i) == profile["piece_length"]:
                    tab.piece_length.setCurrentIndex(i)
                    break


class MenuBar(QMenuBar):
    """Main menu bar for top level menu of program."""

    def __init__(self, parent=None):
        """Constructor for top level widgets."""
        super().__init__(parent=parent)
        self.window = parent
        self.profile_actions = []
        self.home = os.path.join(os.path.expanduser("~"), ".torrentfileQt")
        self.profiles = os.path.join(self.home, "profiles.json")
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
        self.add_profile_actions()
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

    def add_profile_actions(self):
        """Add action class for each profile found in profiles."""
        if os.path.exists(self.home):
            if os.path.exists(self.profiles):
                with open(self.profiles, "rt") as jsonfile:
                    try:
                        profiles = json.load(jsonfile)
                    except json.JSONDecodeError:  # pragma: nocover
                        profiles = {}
                for profile in profiles:
                    action = QAction(self.window)
                    action.setText(profile)
                    profile_action = ProfileAction(profile, action, self)
                    self.profile_menu.addAction(action)
                    self.profile_actions.append(profile_action)

    def add_profile(self, name=None):
        """Add a profile."""
        if not os.path.exists(self.home):
            os.mkdir(self.home)
        if not name:  # pragma: nocover
            name, result = QInputDialog.getText(self, "Add Profile", "Profile Name")
            if not result:
                return
        tab = self.window.central.createWidget
        source = tab.source_input.text()
        trackers = tab.announce_input.toPlainText().split("\n")
        webseeds = tab.web_seed_input.toPlainText().split("\n")
        piece_length_index = tab.piece_length.currentIndex()
        piece_length = tab.piece_length.itemData(piece_length_index)
        if tab.hybridbutton.isChecked():
            version = 3
        elif tab.v2button.isChecked():
            version = 2
        else:
            version = 1
        private = False
        if tab.private.isChecked():
            private = True
        attributes = {
            "version": version,
            "private": private,
            "piece_length": piece_length,
            "trackers": trackers,
            "web_seeds": webseeds,
            "source": source
        }
        if not os.path.exists(self.profiles):
            with open(self.profiles, "wt") as jsonfile:
                json.dump({name: attributes}, jsonfile)
        else:
            with open(self.profiles, "rt") as jsonfile:
                try:
                    profiles = json.load(jsonfile)
                except json.JSONDecodeError:  # pragma: nocover
                    profiles = {}
            profiles[name] = attributes
            with open(self.profiles, "wt") as jsonfile:
                json.dump(profiles, jsonfile)

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
