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

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QMenu, QMenuBar)

class Menu(QMenu):

    def __init__(self,text,parent=None):
        super().__init__(text,parent=parent)
        self.menubar = parent
        self.txt = text
        font = self.font()
        self.setObjectName(text)
        font.setPointSize(12)
        self.setFont(font)


class MenuBar(QMenuBar):

    stylesheet = """
        QMenu{
            background-color:#000000;
        }
        QMenuBar {
            background:rgb(30, 30, 30);
            color: #FFFFFF;
            margin: 2px;
            font: 9pt;
        }
        QMenuBar::item {
            spacing: 3px;
            padding: 1px 4px;
            background: transparent;
        }
        QMenuBar::item:selected {
            border-style: solid;
            border-top-color: transparent;
            border-right-color: transparent;
            border-left-color: transparent;
            border-bottom-color: #e67e22;
            border-bottom-width: 1px;
            border-style: solid;
            color: #FFFFFF;
            padding-bottom: 0px;
            background-color: #000000;
        }
        QMenu::item:selected {
            border-style: solid;
            border-top-color: transparent;
            border-right-color: transparent;
            border-left-color: #e67e22;
            border-bottom-color: transparent;
            border-left-width: 2px;
            color: #FFFFFF;
            padding-left:15px;
            padding-top:4px;
            padding-bottom:4px;
            padding-right:7px;
            background-color:#000000;
        }
        QMenu::item {
            border-style: solid;
            border-top-color: transparent;
            border-right-color: transparent;
            border-left-color: transparent;
            border-bottom-color: transparent;
            border-bottom-width: 1px;
            border-style: solid;
            color: #a9b7c6;
            padding-left:17px;
            padding-top:4px;
            padding-bottom:4px;
            padding-right:7px;
            background-color:#000000;
        }"""

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        self.args = args
        self.window = parent
        self.kwargs = kwargs
        self.setStyleSheet(self.stylesheet)
        self.file_menu = Menu("File")
        self.help_menu = Menu("Help")
        self.addMenu(self.file_menu)
        self.addMenu(self.help_menu)
        self.actionExit = QAction(self.window)
        self.actionAbout = QAction(self.window)
        self.actionExit.setText("Exit")
        self.actionAbout.setText("About")
        self.file_menu.addAction(self.actionExit)
        self.help_menu.addAction(self.actionAbout)
        self.actionExit.triggered.connect(self.exit_app)
        self.actionAbout.triggered.connect(self.about_qt)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout.setObjectName("actionAbout")

    def about_qt(self):
        self.window.app.aboutQt()

    def exit_app(self):
        self.parent().app.quit()
