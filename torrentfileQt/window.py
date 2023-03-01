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

from PySide6.QtCore import Qt, QRect
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QSizeGrip,
)

from torrentfileQt.bencodeTab import BencodeEditWidget
from torrentfileQt.checkTab import CheckWidget
from torrentfileQt.createTab import CreateWidget
from torrentfileQt.editorTab import EditorWidget
from torrentfileQt.infoTab import InfoWidget
from torrentfileQt.qss import Styles
from torrentfileQt.rebuildTab import RebuildWidget
from torrentfileQt.titleBar import MenuBar, TitleBar
from torrentfileQt.toolTab import ToolWidget
from torrentfileQt.utils import get_icon


class Side(QWidget):
    """
    Class for the sides of the window controlling the shape and size.
    """

    left = Qt.LeftEdge
    right = Qt.RightEdge
    top = Qt.TopEdge
    bottom = Qt.BottomEdge

    def __init__(self, parent, edge):
        """Construct the edge widgets."""
        super().__init__(parent)
        if edge == self.left:
            self.setCursor(Qt.SizeHorCursor)
            self.resizeFunc = self.resizeLeft
        elif edge == self.top:
            self.setCursor(Qt.SizeVerCursor)
            self.resizeFunc = self.resizeTop
        elif edge == self.right:
            self.setCursor(Qt.SizeHorCursor)
            self.resizeFunc = self.resizeRight
        else:
            self.setCursor(Qt.SizeVerCursor)
            self.resizeFunc = self.resizeBottom
        self.mousePos = None

    def resizeLeft(self, delta):
        """Resize the widget from the left."""
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)

    def resizeTop(self, delta):
        """Resize the widget from the top."""
        window = self.window()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)

    def resizeRight(self, delta):
        """Resize the widget from the right."""
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        window.resize(width, window.height())

    def resizeBottom(self, delta):
        """Resize the widget from the bottom."""
        window = self.window()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)

    def mousePressEvent(self, event):
        """Perform action when mouse is button is pressed."""
        if event.button() == Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        """Perform action when mouse is moved."""
        if self.mousePos is not None:
            delta = event.pos() - self.mousePos
            self.resizeFunc(delta)

    def mouseReleaseEvent(self, _):
        """Perform action when mouse button is released."""
        self.mousePos = None


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
        self.sides = [
            Side(self, Side.left),
            Side(self, Side.top),
            Side(self, Side.right),
            Side(self, Side.bottom),
        ]
        self.corners = [QSizeGrip(self) for _ in range(4)]
        self.app = app
        self.statusbar = self.statusBar()
        self.icon = get_icon("torrentfile48")
        self.setWindowIcon(self.icon)
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

    _size = 3

    @property
    def gripSize(self):
        """Return the size of the size grip."""
        return self._size

    def setGripSize(self, size):
        """Set all of the windows side grips."""
        if size == self.gripSize:
            return
        self._size = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        """Update the geometry of the window."""
        self.setContentsMargins(*[self.gripSize] * 4)
        outRect = self.rect()
        inRect = outRect.adjusted(
            self.gripSize, self.gripSize, -self.gripSize, -self.gripSize
        )
        self.corners[0].setGeometry(QRect(outRect.topLeft(), inRect.topLeft()))
        self.corners[1].setGeometry(
            QRect(outRect.topRight(), inRect.topRight()).normalized()
        )
        self.corners[2].setGeometry(
            QRect(inRect.bottomRight(), outRect.bottomRight())
        )
        self.corners[3].setGeometry(
            QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized()
        )
        self.sides[0].setGeometry(
            0, inRect.top(), self.gripSize, inRect.height()
        )
        self.sides[1].setGeometry(
            inRect.left(), 0, inRect.width(), self.gripSize
        )
        self.sides[2].setGeometry(
            inRect.left() + inRect.width(),
            inRect.top(),
            self.gripSize,
            inRect.height(),
        )
        self.sides[3].setGeometry(
            self.gripSize,
            inRect.top() + inRect.height(),
            inRect.width(),
            self.gripSize,
        )

    def resizeEvent(self, event):
        """Trigger event to resize window."""
        super().resizeEvent(event)
        self.updateGrips()


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
        self.addTab(self.bencodeEditWidget, "Bencode Editor")
        self.addTab(self.infoWidget, "Torrent Info")
        self.addTab(self.toolWidget, "Torrent Tools")
        self.addTab(self.rebuildWidget, "Rebuild Torrent")
        self.button_group.buttonClicked.connect(self.switch_tab)
        self.button_group.buttonClicked.emit(self.buttons[0])
        self.layout.addStretch(1)
        self.layout.setContentsMargins(0, 0, 2, 0)

    def addTab(self, widget, title):
        """Add a tab widget to tab bar."""
        button = QPushButton(title, self)
        last = len(self.tabs)
        self.tabs[last] = widget
        self.buttons.append(button)
        self.button_group.addButton(button)
        self.button_group.setId(button, last)
        self.layout.addWidget(button)
        self._parent.stack.addWidget(widget)
        button.setProperty("Tab", True)

    def switch_tab(self, button):
        """Switch do different widget in the stack."""
        active_style = self.app.get_tab_style(True)
        inactive_style = self.app.get_tab_style(False)
        button.setStyleSheet(active_style)
        b_id = self.button_group.id(button)
        self._parent.stack.setCurrentWidget(self.tabs[b_id])
        for tab_button in self.buttons:
            if self.button_group.id(tab_button) != b_id:
                tab_button.setStyleSheet(inactive_style)


class Application(QApplication):
    """QApplication Widget."""

    def _setup_stylesheets(self):
        """Construct initial stylesheet state."""
        self.current_theme = Styles.dark
        theme = Styles.compile(Styles.stylesheet, self.current_theme)
        self.setStyleSheet(theme)

    def set_theme(self, theme):  # pragma: nocover
        """Apply the given stylesheet."""
        self.current_theme = Styles.keys[theme]
        ssheet = Styles.compile(Styles.stylesheet, self.current_theme)
        self.setStyleSheet(ssheet)

    def get_tab_style(self, active):
        """Return the stylesheet for current tab."""
        tabstyle = Styles.tab_stylesheet(active)
        tabsheet = Styles.compile(tabstyle, self.current_theme)
        return tabsheet

    @classmethod
    def start(cls, args=None):
        """Start the program entrypoint."""
        app = cls(args if args else sys.argv)
        app._setup_stylesheets()
        app.window = Window(parent=None, app=app)
        return app


def execute():  # pragma: nocover
    """Run application."""
    app = Application.start()
    app.window.show()
    sys.exit(app.exec())
