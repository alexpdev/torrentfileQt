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
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFormLayout,
                             QStatusBar, QVBoxLayout, QTabWidget)

from torrentfileQt.createTab import CreateWidget
from torrentfileQt.infoTab import InfoWidget
from torrentfileQt.checkTab import CheckWidget
from torrentfileQt.menu import MenuBar
from torrentfileQt.qss import tabBarStyleSheet


"""
Graphical Extension for Users who prefer a GUI over CLI.
"""

class Window(QMainWindow):
    """
    Window MainWindow of GUI extension interface.

    Subclass:
        QMainWindow (QWidget): PyQt6 QMainWindow
    """

    labelRole = QFormLayout.ItemRole.LabelRole
    fieldRole = QFormLayout.ItemRole.FieldRole
    spanRole = QFormLayout.ItemRole.SpanningRole


    stylesheet = """
        QMainWindow {
            background-color:#ddd;
        }
        QDialog {
            background-color:#000000;
        }
        QPlainTextEdit {
            selection-background-color:#f39c12;
            background-color:#000000;
            border-style: solid;
            border-top-color: transparent;
            border-right-color: transparent;
            border-left-color: transparent;
            border-bottom-color: transparent;
            border-width: 1px;
            color: #a9b7c6;
        }
        QStatusBar {
            color:#027f7f;
        }
        QSpinBox {
            color: #a9b7c6;
            background-color:#000000;
        }
        QDoubleSpinBox {
            color: #a9b7c6;
            background-color:#000000;
        }
        QToolBox {
            color: #a9b7c6;
            background-color:#000000;
        }
        QToolBox::tab {
            color: #a9b7c6;
            background-color:#000000;
        }
        QToolBox::tab:selected {
            color: #FFFFFF;
            background-color:#000000;
        }
        QScrollArea {
            color: #FFFFFF;
            background-color:#000000;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
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
        self.icon = QIcon("./assets/torrent-icon.png")
        self.setObjectName("Mainwindow")
        self.setWindowTitle("Torrentfile Tools")
        self.setWindowIcon(self.icon)
        self.setMenuBar(self.menubar)
        self.setStatusBar(self.statusbar)
        self.setStyleSheet(self.stylesheet)
        self.resize(500, 450)
        self._setupUI()

    def _setupUI(self):
        """Internal function for setting up UI elements."""
        self.central = TabWidget()
        self.centralLayout = QVBoxLayout()
        self.central.setLayout(self.centralLayout)
        self.setCentralWidget(self.central)
        self.statusbar.setObjectName(u"statusbar")


class TabWidget(QTabWidget):
    """
    Tab Widget.

    Args:
        stylesheet (`str`): QSS styling for Tab Widget.
    """
    stylesheet = tabBarStyleSheet

    def __init__(self, parent=None):
        """Construct Tab Widget for MainWindow.

        Args:
            parent (`QWidget`, deault=None): QMainWindow
        """
        super().__init__(parent=parent)
        self.createWidget = CreateWidget()
        self.checkWidget = CheckWidget()
        self.infoWidget = InfoWidget()
        self.setStyleSheet(self.stylesheet)
        self.addTab(self.createWidget,"Create Torrent")
        self.addTab(self.checkWidget,"Check Torrent")
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
