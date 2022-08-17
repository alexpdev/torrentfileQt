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

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget,
                               QVBoxLayout)

from torrentfileQt.checkTab import CheckWidget
from torrentfileQt.createTab import CreateWidget
from torrentfileQt.editorTab import EditorWidget
from torrentfileQt.infoTab import InfoWidget
from torrentfileQt.magnetTab import MagnetWidget
from torrentfileQt.menu import MenuBar
from torrentfileQt.qss import dark_theme, light_theme
from torrentfileQt.utils import StyleManager, get_icon


class Window(QMainWindow):
    """
    Window MainWindow of GUI extension interface.

    Subclass
    --------
    QMainWindow : QWidget
        PySide6 QMainWindow
    """

    def __init__(self, parent=None, app=None):
        """
        Construct for Window class.

        Parameters
        ----------
        parent : QWidget
            The current Widget's parent.
        app : QApplication
            Controls the GUI application.
        """
        super().__init__(parent=parent)
        self.app = app
        self.menubar = MenuBar(parent=self)
        self.statusbar = self.statusBar()
        self.icon = QIcon(get_icon("torrentfile"))
        self.setObjectName("Mainwindow")
        self.setWindowTitle("TorrentfileQt")
        self.setWindowIcon(self.icon)
        self.setMenuBar(self.menubar)
        self.setStatusBar(self.statusbar)
        self.resize(750, 650)
        self._setupUI()

    def _setupUI(self):
        """Initialize UI widgits function for setting up UI elements."""
        self.central = TabWidget(parent=self)
        self.centralLayout = QVBoxLayout()
        self.central.setLayout(self.centralLayout)
        self.setCentralWidget(self.central)
        self.menubar.setObjectName("menubar")
        self.central.setObjectName("centralTabWidget")
        self.statusbar.setObjectName("statusbar")
        self.centralLayout.setObjectName("centralLayout")


class TabWidget(QTabWidget):
    """Qt Widget subclass for the tab widget."""

    def __init__(self, parent=None):
        """
        Construct Tab Widget for MainWindow.

        Parameters
        ----------
        parent : QWidget
            QMainWindow
        """
        super().__init__(parent=parent)
        self.window = parent
        self.createWidget = CreateWidget(parent=self)
        self.checkWidget = CheckWidget(parent=self)
        self.infoWidget = InfoWidget(parent=self)
        self.editorWidget = EditorWidget(parent=self)
        self.magnetWidget = MagnetWidget(parent=self)
        self.addTab(self.createWidget, "Create Torrent")
        self.addTab(self.checkWidget, "Re-Check Torrent")
        self.addTab(self.infoWidget, "Torrent Info")
        self.addTab(self.editorWidget, "Torrent Editor")
        self.addTab(self.magnetWidget, "Magnet URL")
        self.magnetWidget.setObjectName("magnetWidget")
        self.createWidget.setObjectName("createTab")
        self.checkWidget.setObjectName("checkTab")
        self.infoWidget.setObjectName("infoTab")
        self.editorWidget.setObjectName("editorTab")


class Application(QApplication):
    """QApplication Widget."""

    def __init__(self, args=None):
        """
        Construct for main application backend.

        Parameters
        ----------
        args : list
            argument list passed to window.
        """
        self.args = args if args else sys.argv
        self.themes = {"light": light_theme, "dark": dark_theme}
        super().__init__(self.args)
        self.styleManager = StyleManager(self.themes, dark_theme, self)

    def apply_theme(self, theme):
        """Apply the given stylesheet."""
        self.setStyleSheet(theme)


def start():  # pragma: no cover
    """Start the program entrypoint."""
    app = Application()
    window = Window(parent=None, app=app)
    window.show()
    sys.exit(app.exec())


def alt_start():
    """Start the program entrypoint alternate."""
    app = Application()
    window = Window(parent=None, app=app)
    window.show()
    return window, app


if __name__ == "__main__":
    start()  # pragma: no cover
