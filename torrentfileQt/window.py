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

import string
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QButtonGroup, QHBoxLayout,
                               QMainWindow, QPushButton, QStackedWidget,
                               QVBoxLayout, QWidget)

from torrentfileQt.bencodeTab import BencodeEditWidget
from torrentfileQt.checkTab import CheckWidget
from torrentfileQt.createTab import CreateWidget
from torrentfileQt.editorTab import EditorWidget
from torrentfileQt.infoTab import InfoWidget
from torrentfileQt.menu import MenuBar, TitleBar
from torrentfileQt.qss import dark, light, style, tab_style
from torrentfileQt.rebuildTab import RebuildWidget
from torrentfileQt.toolTab import ToolWidget
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
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.app = app
        self.statusbar = self.statusBar()
        self.icon = get_icon("torrentfile48")
        self.setObjectName("Mainwindow")
        self.setAttribute(Qt.WA_StyledBackground, True)
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
        self.setContentsMargins(1, 0, 1, 1)
        self.titleBar.setWindowTitle("TorrentfileQt")
        self.central.setAttribute(Qt.WA_StyledBackground, True)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
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
        self.app = QApplication.instance()
        self._parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.addSpacing(10)
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
        self.buttons = []
        self.button_group = QButtonGroup(parent=self)
        self.addTab(self.createWidget, "Create Torrent")
        self.addTab(self.editorWidget, "Edit Torrent")
        self.addTab(self.checkWidget, "Recheck Torrent")
        self.addTab(self.rebuildWidget, "Rebuild Torrent")
        self.addTab(self.bencodeEditWidget, "Bencode Editor")
        self.addTab(self.infoWidget, "Torrent Info")
        self.addTab(self.toolWidget, "Torrent Tools")
        self.button_group.buttonClicked.connect(self.switch_tab)
        self.button_group.buttonClicked.emit(self.buttons[0])
        self.layout.addStretch(1)
        self.layout.setContentsMargins(0, 0, 2, 0)

    def addTab(self, widget, title):
        button = QPushButton(title, self)
        l = len(self.tabs)
        self.tabs[l] = widget
        self.buttons.append(button)
        self.button_group.addButton(button)
        self.button_group.setId(button, l)
        self.layout.addWidget(button)
        self._parent.stack.addWidget(widget)
        button.setProperty("Tab", True)

    def switch_tab(self, button):
        active_style = self.app.get_tab_style(True)
        inactive_style = self.app.get_tab_style(False)
        button.setStyleSheet(active_style)
        b_id = self.button_group.id(button)
        self._parent.stack.setCurrentWidget(self.tabs[b_id])
        for button in self.buttons:
            if self.button_group.id(button) != b_id:
                button.setStyleSheet(inactive_style)


class Application(QApplication):
    """QApplication Widget."""

    def _setup_stylesheets(self):
        """Construct initial stylesheet state."""
        self.tab_style = tab_style
        themes = {"dark": dark, "light": light}
        self.styler = StyleManager(themes, style, "dark")
        self.styler.setTheme()

    def set_new_theme(self, theme):
        """Apply the given stylesheet."""
        self.styler.current = theme
        self.setStyleSheet(theme)

    def get_tab_style(self, active):
        """Return the stylesheet for current tab."""
        tabstyle = self.tab_style(active)
        template = string.Template(tabstyle)
        theme = self.styler.themes[self.styler.default]
        style = template.substitute(theme)
        return style

    @classmethod
    def start(cls, args=None):  # pragma: no cover
        """Start the program entrypoint."""
        app = cls(args if args else sys.argv)
        app._setup_stylesheets()
        app.window = Window(parent=None, app=app)
        app.window.show()
        sys.exit(app.exec())


def execute():
    """Run application."""
    Application.start()  # pragma: nocover
