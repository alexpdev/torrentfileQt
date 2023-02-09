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

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
                               QMenu, QMenuBar, QPlainTextEdit, QPushButton,
                               QSizePolicy, QToolButton, QVBoxLayout, QWidget)

from torrentfileQt.utils import get_icon

icon = os.path.join(os.path.dirname(__file__), "home.png")


class TitleBarButton(QPushButton):
    """Standard Buttons for closing and minimizing the window."""

    def __init__(self, prop, parent=None):
        """Construct the standard window control buttons."""
        super().__init__(parent=parent)
        self.setFixedHeight(25)
        self.setFixedWidth(25)
        self.setProperty(prop, True)
        self.setProperty("titlebutton", True)
        self.setObjectName(prop + "Button")
        self.setIcon(QIcon(get_icon(prop + "-dark")))
        self.clicked.connect(self.window_action)

    def window_action(self):
        """Perform action for the specified button."""
        if self.property("close"):  # pragma: nocover
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
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("titlebar")
        pix = QIcon(icon)
        self.icon = QToolButton(parent=self)
        self.icon.setObjectName("titlebaricon")
        self.icon.setIcon(pix)
        self.setMaximumHeight(35)
        self.setMinimumHeight(30)
        self.closeButton = TitleBarButton("close", parent=self)
        self.minimizeButton = TitleBarButton("min", parent=self)
        self.maximizeButton = TitleBarButton("max", parent=self)
        sizePolicy = QSizePolicy()
        sizePolicy.setHorizontalPolicy(QSizePolicy.Policy.Fixed)
        self.closeButton.setSizePolicy(sizePolicy)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
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
        """Set the title bar label."""
        self.label.setText(title)

    def setWindowIcon(self, icon: str) -> None:
        """Set the window icon."""
        icon = QIcon(icon)
        self.icon.setIcon(icon)

    def mouseDoubleClickEvent(self, _):
        """Trigger event to maximize window."""
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def mousePressEvent(self, event):
        """Trigger event to move window."""
        self._pressed = True
        self._cpos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        """Start moving window."""
        if not self._pressed:
            return
        pos = event.position().toPoint()
        difx, dify = (pos - self._cpos).toTuple()
        geom = self.window().geometry()
        x, y, w, h = geom.x(), geom.y(), geom.width(), geom.height()
        new_coords = x + difx, y + dify, w, h
        self.window().setGeometry(*new_coords)

    def mouseReleaseEvent(self, _):
        """End the window move event."""
        self._pressed = False
        self._cpos = None

    def setMenuBar(self, menubar):
        """Set the menu bar in the title bar."""
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
        self.options_menu = OptionsMenu("Options", self)
        self.addMenu(self.options_menu)


class OptionsMenu(QMenu):
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
        self.styleAction = QAction(self.window)
        self.addAction(self.actionExit)
        self.addAction(self.actionLightTheme)
        self.addAction(self.actionDarkTheme)
        self.actionDarkTheme.setText("Dark Theme")
        self.actionLightTheme.setText("Light Theme")
        self.actionExit.setText("Exit")
        self.styleAction.setText("Edit StyleSheet")
        self.styleAction.triggered.connect(self.open_style_dialog)
        self.actionExit.triggered.connect(self.exit_app)
        self.actionLightTheme.triggered.connect(self.light_theme)
        self.actionDarkTheme.triggered.connect(self.dark_theme)
        self.actionExit.setObjectName("actionExit")
        self.actionLightTheme.setObjectName("actionLightTheme")
        self.actionDarkTheme.setObjectName("actiondDarkTheme")
        self.actionAbout = QAction(self.window)
        self.actionDocs = QAction(self.window)
        self.actionRepo = QAction(self.window)
        self.addAction(self.actionAbout)
        self.addAction(self.actionDocs)
        self.addAction(self.actionRepo)
        self.addAction(self.styleAction)
        self.actionRepo.setText("Github Repository")
        self.actionAbout.setText("About")
        self.actionDocs.setText("Documentation")
        self.actionAbout.triggered.connect(self.about_qt)
        self.actionDocs.triggered.connect(self.documentation)
        self.actionRepo.triggered.connect(self.repository)
        self.actionDocs.setObjectName("actionDocs")
        self.actionAbout.setObjectName("actionAbout")

    def exit_app(self):
        """Close application."""
        self.parent().window.app.quit()  # pragma: nocover

    def light_theme(self):
        """Change the GUI theme for the application."""
        QApplication.instance().set_theme("light")

    def dark_theme(self):
        """Change the GUI application to dark theme."""
        QApplication.instance().set_theme("dark")

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

    def open_style_dialog(self):
        """Edit style sheet."""
        app = QApplication.instance()
        self.dialog = QDialog()
        self.dialog.resize(500, 700)
        vlayout = QVBoxLayout(self.dialog)
        hlayout = QHBoxLayout()
        current = app.styleSheet()
        self.dialog.plainTextEdit = QPlainTextEdit()
        self.dialog.plainTextEdit.setPlainText(current)
        writeButton = QPushButton("Write")
        savebutton = QPushButton("Save")
        cancelbutton = QPushButton("Cancel")
        hlayout.addWidget(savebutton)
        hlayout.addWidget(cancelbutton)
        hlayout.addWidget(writeButton)
        vlayout.addWidget(self.dialog.plainTextEdit)
        vlayout.addLayout(hlayout)
        savebutton.clicked.connect(self.saveStyle)
        cancelbutton.clicked.connect(self.closeStyleDialog)
        writeButton.clicked.connect(self.writeContents)
        self.dialog.show()

    def writeContents(self):  # pragma: nocover
        """Write a copy of the edited style sheet."""
        text = self.dialog.plainTextEdit.toPlainText()
        with open(os.path.join(os.path.dirname(__file__), "temp.qss"),
                  "wt") as qss:
            qss.write(text)

    def closeStyleDialog(self):
        """Close the style sheet dialog."""
        self.dialog.close()
        self.dialog.deleteLater()

    def saveStyle(self):
        """Apply style sheet to active window."""
        app = QApplication.instance()
        text = self.dialog.plainTextEdit.toPlainText()
        app.setStyleSheet(text)
