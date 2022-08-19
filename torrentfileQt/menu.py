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

import json
import os
import webbrowser

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QInputDialog, QMenu, QMenuBar


class MenuBar(QMenuBar):
    """Main menu bar for top level menu of program."""

    def __init__(self, parent=None):
        """
        Construct top level widgets.

        Parameters
        ----------
        parent : QWidget
            This widgets parent widget.
        """
        super().__init__(parent=parent)
        self.window = parent
        self.file_menu = FileMenu("File", self)
        self.help_menu = HelpMenu("Help", self)
        self.profile_menu = ProfileMenu("Profiles", self)
        self.addMenu(self.file_menu)
        self.addMenu(self.profile_menu)
        self.addMenu(self.help_menu)


class FileMenu(QMenu):
    """Menu for the file dropdown in menubar."""

    def __init__(self, title, parent):
        """
        Construct top level widgets.

        Parameters
        ----------
        title : str
            The menu bar categorie string.
        parent : QWidget
            This widgets parent widget.
        """
        super().__init__(title, parent)
        self.widget = parent
        self.window = parent.window
        self.actionExit = QAction(self.window)
        self.actionLightTheme = QAction(self.window)
        self.actionDarkTheme = QAction(self.window)
        self.actionFontPlus = QAction(self.window)
        self.actionFontMinus = QAction(self.window)
        self.addAction(self.actionExit)
        self.addAction(self.actionFontPlus)
        self.addAction(self.actionFontMinus)
        self.addAction(self.actionLightTheme)
        self.addAction(self.actionDarkTheme)
        self.actionFontPlus.setText("Font Size +")
        self.actionFontMinus.setText("Font Size -")
        self.actionDarkTheme.setText("Dark Theme")
        self.actionLightTheme.setText("Light Theme")
        self.actionExit.setText("Exit")
        self.actionFontPlus.triggered.connect(self.increaseFont)
        self.actionFontMinus.triggered.connect(self.decreaseFont)
        self.actionExit.triggered.connect(self.exit_app)
        self.actionLightTheme.triggered.connect(self.light_theme)
        self.actionDarkTheme.triggered.connect(self.dark_theme)
        self.actionFontPlus.setObjectName("actionIncreaseFont")
        self.actionFontMinus.setObjectName("actionDecreaseFont")
        self.actionExit.setObjectName("actionExit")
        self.actionLightTheme.setObjectName("actionLightTheme")
        self.actionDarkTheme.setObjectName("actiondDarkTheme")

    def exit_app(self):
        """Close application."""
        app = self.parent().window.app
        app.quit()  # pragma: nocover

    def light_theme(self):
        """Change the GUI theme for the application."""
        app = self.parent().window.app
        app.styleManager.set_theme_from_title("light_theme")

    def dark_theme(self):
        """Change the GUI application to dark theme."""
        app = self.parent().window.app
        app.styleManager.set_theme_from_title("dark_theme")

    def increaseFont(self):
        """Increase Font Size for all widgets with text."""
        app = self.parent().window.app
        app.styleManager.increase_font_size()

    def decreaseFont(self):
        """Decrease font size for all widgets with text."""
        app = self.parent().window.app
        app.styleManager.decrease_font_size()


class HelpMenu(QMenu):
    """Menu for the Help menu dropdown in menubar."""

    def __init__(self, title, parent):
        """
        Construct for top level widgets.

        Parameters
        ----------
        title : str
            The menu bar categorie string.
        parent : QWidget
            This widgets parent widget.
        """
        super().__init__(title, parent)
        self.widget = parent
        self.window = parent.window
        self.actionAbout = QAction(self.window)
        self.actionDocs = QAction(self.window)
        self.actionRepo = QAction(self.window)
        self.addAction(self.actionAbout)
        self.addAction(self.actionDocs)
        self.addAction(self.actionRepo)
        self.actionRepo.setText("Github Repository")
        self.actionAbout.setText("About")
        self.actionDocs.setText("Documentation")
        self.actionAbout.triggered.connect(self.about_qt)
        self.actionDocs.triggered.connect(self.documentation)
        self.actionRepo.triggered.connect(self.repository)
        self.actionDocs.setObjectName("actionDocs")
        self.actionAbout.setObjectName("actionAbout")

    def about_qt(self):
        """Open the about qt menu."""
        self.window.app.aboutQt()  # pragma: nocover

    @staticmethod
    def documentation():  # pragma: no cover
        """Open webbrowser to TorrentFileQt documentation."""
        webbrowser.open_new_tab("https://alexpdev.github.io/torrentfile")

    @staticmethod
    def repository():  # pragma: no cover
        """Open webbrowser to GitHub Repo."""
        webbrowser.open_new_tab("https://github.com/alexpdev/torrentfileQt")


class ProfileMenu(QMenu):
    """Menu for the Profile dropdown in menubar."""

    def __init__(self, title, parent):
        """
        Construct for top level widgets.

        Parameters
        ----------
        title : str
            The menu bar categorie string.
        parent : QWidget
            This widgets parent widget.
        """
        super().__init__(title, parent)
        self.widget = parent
        self.window = parent.window
        self.profile_actions = []
        self.home = os.path.join(os.path.expanduser("~"), ".torrentfileQt")
        self.profiles = os.path.join(self.home, "profiles.json")
        self.add_profile_actions()
        self.actionAddProfile = QAction(self.window)
        self.actionAddProfile.setText("Add Profile")
        self.actionAddProfile.setObjectName("actionAddProfile")
        self.addAction(self.actionAddProfile)
        self.actionAddProfile.triggered.connect(self.add_profile)

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
                    self.addAction(action)
                    self.profile_actions.append(profile_action)

    def add_profile(self, name=None):
        """Add a profile."""
        if not os.path.exists(self.home):
            os.mkdir(self.home)
        if not name:  # pragma: nocover
            name, result = QInputDialog.getText(self, "Add Profile",
                                                "Profile Name")
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
            "source": source,
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


class ProfileAction:
    """
    Store the name and action taken when this menu button is triggered.

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
        filename = os.path.join(self.parent.home, "profiles.json")
        with open(filename, "rt") as jsonfile:
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
