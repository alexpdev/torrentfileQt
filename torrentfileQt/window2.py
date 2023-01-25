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
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget,
                               QVBoxLayout, QWidget, QStackedWidget, QHBoxLayout, QLabel, QPushButton)

from torrentfileQt.bencodeTab import BencodeEditWidget
from torrentfileQt.checkTab import CheckWidget
from torrentfileQt.createTab import CreateWidget
from torrentfileQt.editorTab import EditorWidget
from torrentfileQt.infoTab import InfoWidget
from torrentfileQt.menu import MenuBar, TitleBar
from torrentfileQt.qss import dark_theme, light_theme
from torrentfileQt.rebuildTab import RebuildWidget
from torrentfileQt.toolTab import ToolWidget
from torrentfileQt.utils import StyleManager, get_icon

# from torrentfileQt.qss import compile

THEMES = {"dark_theme": dark_theme, "light_theme": light_theme}
DEFAULT_THEME = "dark_theme"


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
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.app = app
        self.statusbar = self.statusBar()
        self.icon = get_icon("torrentfile48")
        self.setObjectName("Mainwindow")
        self.setStatusBar(self.statusbar)
        self.resize(820, 740)
        self._setupUI()

    def _setupUI(self):
        """Initialize UI widgits function for setting up UI elements."""
        self.menubar = MenuBar(parent=self)
        self.central = QWidget(self)
        self.central_layout = QVBoxLayout(self.central)
        self.titleBar = TitleBar(parent=self)
        self.central_layout.addWidget(self.titleBar)
        self.hlayout = QHBoxLayout()
        self.central_layout.setSpacing(0)
        self.setContentsMargins(1,0,1,1)
        self.titleBar.setWindowTitle("TorrentfileQt")
        self.central_layout.setContentsMargins(0,0,0,0)
        self.titleBar.setWindowIcon(self.icon)
        self.titleBar.setMenuBar(self.menubar)
        self.stack = QStackedWidget(parent=self)
        self.tabs = TabWidget(self)
        self.hlayout.addWidget(self.tabs)
        self.hlayout.addWidget(self.stack)
        self.central_layout.addLayout(self.hlayout)
        self.setCentralWidget(self.central)
        self.menubar.setObjectName("menubar")
        self.central.setObjectName("centralTabWidget")
        self.statusbar.setObjectName("statusbar")
        self.central_layout.setObjectName("centralLayout")


class TabWidget(QWidget):
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
        self._parent = parent
        self.layout = QVBoxLayout(self)
        self.setProperty("tabs", True)
        self.setObjectName("tabbar")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.createWidget = CreateWidget(parent=self)
        self.checkWidget = CheckWidget(parent=self)
        self.infoWidget = InfoWidget(parent=self)
        self.editorWidget = EditorWidget(parent=self)
        self.toolWidget = ToolWidget(parent=self)
        self.bencodeEditWidget = BencodeEditWidget(parent=self)
        self.rebuildWidget = RebuildWidget(parent=self)
        self.tabs = {}
        self.addTab(self.createWidget, "Create Torrent")
        self.addTab(self.editorWidget, "Edit Torrent")
        self.addTab(self.checkWidget, "Recheck Torrent")
        self.addTab(self.rebuildWidget, "Rebuild Torrent")
        self.addTab(self.bencodeEditWidget, "Bencode Editor")
        self.addTab(self.infoWidget, "Torrent Info")
        self.addTab(self.toolWidget, "Torrent Tools")
        self.createWidget.setProperty("ActiveTab", True)
        self.layout.addStretch(1)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.toolWidget.setObjectName("toolWidget")
        self.rebuildWidget.setObjectName("rebuildTab")
        self.createWidget.setObjectName("createTab")
        self.infoWidget.setObjectName("infoTab")
        self.checkWidget.setObjectName("checkTab")
        self.bencodeEditWidget.setObjectName("bencodeTab")
        self.editorWidget.setObjectName("editorTab")

    def addTab(self, widget, title):
        button = QPushButton(title, self)
        l = len(self.tabs)
        self.tabs[l] = {
            "widget": widget,
            "button": button,
            "func": lambda: self.open_tab(l)
        }
        self.layout.addWidget(button)
        self._parent.stack.addWidget(widget)
        button.setProperty("Tab", True)
        button.clicked.connect(self.tabs[l]["func"])

    def open_tab(self, index):
        for k, v in self.tabs.items():
            button = v.get("button")
            if k == index:
                button.setProperty("Tab", False)
                button.setProperty("ActiveTab", True)
            elif button.property("ActiveTab"):
                button.setProperty("ActiveTab", False)
                button.setProperty("Tab", True)
        self.window().stack.setCurrentIndex(index)



class Application(QApplication):
    """QApplication Widget."""

    def __init__(self, args):
        """
        Construct for main application backend.

        Parameters
        ----------
        args : list
            argument list passed to window.
        """
        super().__init__(args)
        self._setup_stylesheets()
        self.window = Window(parent=None, app=self)
        # self.setStyleSheet(compile())

    def _setup_stylesheets(self):
        """Construct initial stylesheet state."""
        self.qstyles = StyleManager(THEMES)
        self.qstyles.set_theme_from_title(DEFAULT_THEME)

    def set_new_theme(self, theme):
        """Apply the given stylesheet."""
        self.qstyles.current = theme
        self.setStyleSheet(theme)

    @classmethod
    def start(cls, args=None):  # pragma: no cover
        """Start the program entrypoint."""
        app = cls(args if args else sys.argv)
        app.window.show()
        sys.exit(app.exec())


def execute():
    """Run application."""
    Application.start()  # pragma: nocover
