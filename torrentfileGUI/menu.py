from torrentfile import Bendecoder
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QFileDialog, QMenu, QMenuBar)

class Menu(QMenu):

    stylesheet = """
        QMenu {
            color: #dfdbd2;
            background-color: #41403b;
        }
        QMenu::item {
            color: #dfdbd2;
            border-color: #2a2a2c;
            padding: 4px 10px 4px 20px;
            border-style: solid;
            border-width: 3px;
        }
        QMenu::item:selected {
            color:#FFF;
            background-color: #e16c36;
            border-style:solid;
            border-width:3px;
            padding:4px 7px 4px 17px;
            border-bottom-color:#af5530;
            border-top-color:#d95721;
            border-right-color:#cd5a2e;
            border-left-color:#fd9c71;
        }"""

    def __init__(self,text,parent=None):
        super().__init__(text,parent=parent)
        self.menubar = parent
        self.txt = text
        font = self.font()
        self.setObjectName(text)
        font.setPointSize(10)
        self.setFont(font)
        self.setStyleSheet(self.stylesheet)


class MenuBar(QMenuBar):

    stylesheet = """
        QMenuBar {
	        color: #dfdbd2;
	        background-color: #41403b;
        }
        QMenuBar::item {
            padding: 5px;
            color: #dfdbd2;
            background-color: #41403b;
        }
        QMenuBar::item:selected {
            color: #FFF;
            padding: 2px;
            padding-bottom: 0px;
            border-width: 3px;
            border-bottom-width: 0px;
            border-top-right-radius: 4px;
            border-top-left-radius: 4px;
            border-style: solid;
            background-color: #41403b;
            border-top-color: #2a2a2c;
            border-right-color: #2f2f2c;
            border-left-color: #27272c;
        }"""

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        self.args = args
        self.window=parent
        self.kwargs = kwargs
        self.setStyleSheet(self.stylesheet)
        self.file_menu = Menu("File")
        self.options_menu = Menu("Options")
        self.help_menu = Menu("Help")
        self.addMenu(self.file_menu)
        self.addMenu(self.options_menu)
        self.addMenu(self.help_menu)
        self.actionExit = QAction(self.window)
        self.actionLoad = QAction(self.window)
        self.actionAbout = QAction(self.window)
        self.actionExit.setText("Exit")
        self.actionLoad.setText("Load Torrent")
        self.actionAbout.setText("About")
        self.file_menu.addAction(self.actionExit)
        self.options_menu.addAction(self.actionLoad)
        self.help_menu.addAction(self.actionAbout)
        self.actionExit.triggered.connect(self.exit_app)
        self.actionLoad.triggered.connect(self.load)
        self.actionAbout.triggered.connect(self.about_qt)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout.setObjectName("actionAbout")
        self.actionLoad.setObjectName("actionLoad")

    def about_qt(self):
        self.window.app.aboutQt()

    def exit_app(self):
        self.parent().app.exit()

    def load(self):
        fname = QFileDialog.getOpenFileName(self, "Select File", "/", "*.torrent")
        decoder = Bendecoder()
        data = open(fname[0], "rb").read()
        results = decoder.decode(data)
        self.parent().apply_settings(results)
