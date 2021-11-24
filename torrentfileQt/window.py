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
"""Graphical Extension for Users who prefer a GUI over CLI."""

import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QMainWindow, QStatusBar, QTabWidget,
                             QVBoxLayout)

from torrentfileQt.checkTab import CheckWidget
from torrentfileQt.createTab import CreateWidget
from torrentfileQt.editorTab import EditorWidget
from torrentfileQt.infoTab import InfoWidget
from torrentfileQt.menu import MenuBar
# from torrentfileQt.qss import (mainWindowSheet, statusBarSheet, tabBarSheet,
#                                tabSheet)
from torrentfileQt.qss import stylesheet


class Window(QMainWindow):
    """Window MainWindow of GUI extension interface.

    Subclass:
        QMainWindow (QWidget): PyQt6 QMainWindow
    """

    def __init__(self, parent=None, app=None):
        """Constructor for Window class.

        Args:
            parent (QWidget, optional): The current Widget's parent.
                Defaults to None.
            app (QApplication, optional): Controls the GUI application.
                Defaults to None.
        """
        super().__init__(parent=parent)
        self.app = app
        self.menubar = MenuBar(parent=self)
        self.statusbar = QStatusBar(parent=self)
        self.icon = QIcon("./assets/favicon.png")
        self.setObjectName("Mainwindow")
        self.setWindowTitle("Torrentfile Tools")
        self.setWindowIcon(self.icon)
        self.setMenuBar(self.menubar)
        self.setStatusBar(self.statusbar)
        # self.setStyleSheet(mainWindowSheet + statusBarSheet)
        self.setStyleSheet(stylesheet)
        self.resize(750, 650)
        self._setupUI()

    def _setupUI(self):
        """Internal function for setting up UI elements."""
        self.central = TabWidget(parent=self)
        self.centralLayout = QVBoxLayout()
        self.central.setLayout(self.centralLayout)
        self.setCentralWidget(self.central)
        self.statusbar.setObjectName("statusbar")
        self.menubar.setObjectName("menubar")
        self.central.setObjectName("centralTabWidget")
        self.centralLayout.setObjectName("centralLayout")


class TabWidget(QTabWidget):
    """Qt Widget subclass for the tab widget."""

    def __init__(self, parent=None):
        """Construct Tab Widget for MainWindow.

        Args:
            parent (`QWidget`, deault=None): QMainWindow
        """
        super().__init__(parent=parent)
        self.window = parent
        self.createWidget = CreateWidget(parent=self)
        self.checkWidget = CheckWidget(parent=self)
        self.infoWidget = InfoWidget(parent=self)
        self.editorWidget = EditorWidget(parent=self)
        # self.setStyleSheet(tabBarSheet + tabSheet)
        self.addTab(self.createWidget, "Create Torrent")
        self.addTab(self.checkWidget, "Re-Check Torrent")
        self.addTab(self.infoWidget, "Torrent Info")
        self.addTab(self.editorWidget, "Torrent Editor")
        self.createWidget.setObjectName("createTab")
        self.checkWidget.setObjectName("checkTab")
        self.infoWidget.setObjectName("infoTab")
        self.editorWidget.setObjectName("editorTab")


class Application(QApplication):
    """QApplication Widget."""

    def __init__(self, args=None):
        """Constructor for main application backend.

        Args:
            args (`list`, optional): argument list passed to window.
                Defaults to None.
        """
        self.args = args if args else sys.argv
        super().__init__(self.args)


def start():  # pragma: no cover
    """Entrypoint for program."""
    app = Application()
    window = Window(parent=None, app=app)
    window.show()
    sys.exit(app.exec())


def alt_start():
    """Entrypoint for testing scripts."""
    app = Application()
    window = Window(parent=None, app=app)
    window.show()
    return window, app


if __name__ == "__main__":
    start()  # pragma: no cover
