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

import webbrowser

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QMenuBar

from .qss import menuSheet


class Menu(QMenu):
    def __init__(self, text, parent=None):
        super().__init__(text, parent=parent)
        self.menubar = parent
        self.txt = text
        font = self.font()
        self.setObjectName(text)
        font.setPointSize(12)
        self.setFont(font)


class MenuBar(QMenuBar):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        self.args = args
        self.window = parent
        self.kwargs = kwargs
        self.setStyleSheet(menuSheet)
        self.file_menu = Menu("File")
        self.help_menu = Menu("Help")
        self.addMenu(self.file_menu)
        self.addMenu(self.help_menu)
        self.actionExit = QAction(self.window)
        self.actionAbout = QAction(self.window)
        self.actionDocs = QAction(self.window)
        self.actionRepo = QAction(self.window)
        self.actionRepo.setText("Github Repository")
        self.actionExit.setText("Exit")
        self.actionAbout.setText("About")
        self.actionDocs.setText("Documentation")
        self.file_menu.addAction(self.actionExit)
        self.help_menu.addAction(self.actionAbout)
        self.help_menu.addAction(self.actionDocs)
        self.help_menu.addAction(self.actionRepo)
        self.actionExit.triggered.connect(self.exit_app)
        self.actionAbout.triggered.connect(self.about_qt)
        self.actionDocs.triggered.connect(self.documentation)
        self.actionRepo.triggered.connect(self.repository)
        self.actionDocs.setObjectName("actionDocs")
        self.actionExit.setObjectName("actionExit")
        self.actionAbout.setObjectName("actionAbout")

    def documentation(self):
        webbrowser.open_new_tab("https://alexpdev.github.io/torrentfile")

    def repository(self):
        webbrowser.open_new_tab("https://github.com/torrentfileQt")

    def about_qt(self):
        self.window.app.aboutQt()

    def exit_app(self):
        self.parent().app.quit()
