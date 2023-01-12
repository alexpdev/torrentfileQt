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

from PySide6.QtGui import QAction, QPixmap
from PySide6.QtWidgets import QMenu, QMenuBar, QApplication, QPushButton, QWidget, QLabel, QSizePolicy, QHBoxLayout



icon = os.path.join(os.path.dirname(__file__), "home.png")


class TitleBarButton(QPushButton):
    """Standard Buttons for closing and minimizing the window."""

    def __init__(self, prop, parent=None):
        """Construct the standard window control buttons."""
        super().__init__(parent=parent)
        self.setFixedHeight(20)
        self.setFixedWidth(20)
        self.setProperty(prop, "true")
        self.clicked.connect(self.window_action)

    def window_action(self):
        """Perform action for the specified button."""
        if self.property("close"):
            self.window().destroy(True, True)
            QApplication.instance().exit()
        if self.property("min"):
            if self.window().isMinimized():
                self.window().showNormal()
            else:
                self.window().showMinimized()
        if self.property("max"):
            if self.window().isMaximized():
                self.window().showNormal()
            else:
                self.window().showMaximized()


class TitleBar(QWidget):
    """Custom titlebar for a frameless QMainWindow."""

    def __init__(self, parent=None):
        """Construct for titlebar."""
        super().__init__(parent=parent)
        self.label = QLabel()
        self.setProperty("titleBar", "true")
        pix = QPixmap(icon)
        self.icon = QLabel()
        self.icon.setPixmap(pix)
        self.label.setText("TitleBar")
        self.setMaximumHeight(50)
        self.closeButton = TitleBarButton("close", parent=self)
        self.minimizeButton = TitleBarButton("min", parent=self)
        self.maximizeButton = TitleBarButton("max", parent=self)
        sizePolicy = QSizePolicy()
        sizePolicy.setHorizontalPolicy(QSizePolicy.Policy.Fixed)
        self.closeButton.setSizePolicy(sizePolicy)
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.icon)
        self.layout.addStretch(1)
        self.layout.addWidget(self.label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.minimizeButton)
        self.layout.addWidget(self.maximizeButton)
        self.layout.addWidget(self.closeButton)
        self.setMouseTracking(True)
        self._pressed = False
        self._cpos = None

    def setWindowTitle(self, title: str) -> None:
        """Sets the title bar label."""
        self.label.setText(title)

    def setWindowIcon(self, icon: str) -> None:
        """Sets the window icon."""
        pixmap = QPixmap(icon)
        self.icon.setPixmap(pixmap)

    def mouseDoubleClickEvent(self, _):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def mousePressEvent(self, event):
        self._pressed = True
        self._cpos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if not self._pressed:
            return
        pos = event.position().toPoint()
        difx, dify = (pos - self._cpos).toTuple()
        geom = self.window().geometry()
        x, y, w, h = geom.x(), geom.y(), geom.width(), geom.height()
        new_coords = x+difx, y+dify, w, h
        self.window().setGeometry(*new_coords)

    def mouseReleaseEvent(self, event):
        self._pressed = False
        self._cpos = None

    def setMenuBar(self, menubar):
        self.menuBar = menubar
        self.layout.insertWidget(1, menubar)


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
        self.addMenu(self.file_menu)
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
        self.parent().window.app.quit()  # pragma: nocover

    def light_theme(self):
        """Change the GUI theme for the application."""
        app = self.parent().window.app
        app.qstyles.set_theme_from_title("light_theme")

    def dark_theme(self):
        """Change the GUI application to dark theme."""
        app = self.parent().window.app
        app.qstyles.set_theme_from_title("dark_theme")

    def increaseFont(self):
        """Increase Font Size for all widgets with text."""
        app = self.parent().window.app
        app.qstyles.increase_font_size()

    def decreaseFont(self):
        """Decrease font size for all widgets with text."""
        app = self.parent().window.app
        app.qstyles.decrease_font_size()


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
