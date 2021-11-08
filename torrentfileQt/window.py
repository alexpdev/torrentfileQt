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

import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
)

from torrentfileQt.checkTab import CheckWidget
from torrentfileQt.createTab import CreateWidget
from torrentfileQt.infoTab import InfoWidget
from torrentfileQt.menu import MenuBar
from torrentfileQt.qss import mainWindowSheet, statusBarSheet, tabBarSheet, tabSheet

"""Graphical Extension for Users who prefer a GUI over CLI."""


class Window(QMainWindow):
    """Window MainWindow of GUI extension interface.

    Subclass:
        QMainWindow (QWidget): PyQt6 QMainWindow
    """

    def __init__(self, parent=None, app=None):
        """Constructor for Window class.

        Args:
            parent (QWidget, optional):
                The current Widget's parent. Defaults to None.
            app (QApplication, optional):
                Controls the GUI application. Defaults to None.
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
        self.setStyleSheet(mainWindowSheet)
        self.resize(800, 600)
        self._setupUI()

    def _setupUI(self):
        """Internal function for setting up UI elements."""
        self.central = TabWidget(parent=self)
        self.centralLayout = QVBoxLayout()
        self.central.setLayout(self.centralLayout)
        self.setCentralWidget(self.central)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet(statusBarSheet)


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
        self.setStyleSheet(tabBarSheet + tabSheet)
        self.addTab(self.createWidget, "Create Torrent")
        self.addTab(self.checkWidget, "Re-Check Torrent")
        self.addTab(self.infoWidget, "Torrent Info")


class Application(QApplication):
    def __init__(self, args=None):
        self.args = args
        if not args:
            self.args = sys.argv
        super().__init__(self.args)


def start():
    app = Application()
    window = Window(parent=None, app=app)
    window.show()
    sys.exit(app.exec())


def alt_start():
    app = Application()
    window = Window(parent=None, app=app)
    window.show()
    return window, app


if __name__ == "__main__":
    start()
