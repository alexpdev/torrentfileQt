import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFileDialog,
                             QHBoxLayout, QLabel, QLineEdit, QSpacerItem,
                             QMainWindow, QPlainTextEdit, QTextBrowser,
                             QPushButton, QToolButton, QWidget, QFormLayout,
                             QStatusBar, QTabWidget, QVBoxLayout, QRadioButton)
import torrentfile
from torrentfileGUI.menu import MenuBar

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
        background-color:#000000;
    }
    QDialog {
        background-color:#000000;
    }
    QColorDialog {
        background-color:#000000;
    }
    QTextEdit {
        background-color:#000000;
        color: #a9b7c6;
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
    QPushButton{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: transparent;
        border-width: 1px;
        border-style: solid;
        color: #a9b7c6;
        padding: 2px;
        background-color: #000000;
    }
    QPushButton::default{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-width: 1px;
        color: #a9b7c6;
        padding: 2px;
        background-color: #000000;
    }
    QPushButton:hover{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-bottom-width: 1px;
        border-style: solid;
        color: #FFFFFF;
        padding-bottom: 2px;
        background-color: #000000;
    }
    QPushButton:pressed{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-bottom-width: 2px;
        border-style: solid;
        color: #e67e22;
        padding-bottom: 1px;
        background-color: #000000;
    }
    QPushButton:disabled{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: transparent;
        border-bottom-width: 2px;
        border-style: solid;
        color: #808086;
        padding-bottom: 1px;
        background-color: #000000;
    }
    QToolButton {
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-bottom-width: 1px;
        border-style: solid;
        color: #a9b7c6;
        padding: 2px;
        background-color: #000000;
    }
    QToolButton:hover{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-bottom-width: 2px;
        border-style: solid;
        color: #FFFFFF;
        padding-bottom: 1px;
        background-color: #000000;
    }
    QLineEdit {
        border-width: 1px; border-radius: 4px;
        border-color: rgb(58, 58, 58);
        border-style: inset;
        padding: 0 8px;
        color: #a9b7c6;
        background:#000000;
        selection-background-color:#007b50;
        selection-color: #FFFFFF;
    }
    QLabel {
        color: #a9b7c6;
    }
    QLCDNumber {
        color: #e67e22;
    }
    QProgressBar {
        text-align: center;
        color: rgb(240, 240, 240);
        border-width: 1px;
        border-radius: 10px;
        border-color: rgb(58, 58, 58);
        border-style: inset;
        background-color:#000000;
    }
    QProgressBar::chunk {
        background-color: #e67e22;
        border-radius: 5px;
    }
    QMenu{
        background-color:#000000;
    }
    QMenuBar {
        background:rgb(0, 0, 0);
        color: #a9b7c6;
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
    }
    QTabWidget {
        color:rgb(0,0,0);
        background-color:#000000;
    }
    QTabWidget::pane {
            border-color: rgb(77,77,77);
            background-color:#000000;
            border-style: solid;
            border-width: 1px;
            border-radius: 6px;
    }
    QTabBar::tab {
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: transparent;
        border-bottom-width: 1px;
        border-style: solid;
        color: #808086;
        padding: 3px;
        margin-left:3px;
        background-color:#000000;
    }
    QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-bottom-width: 2px;
        border-style: solid;
        color: #FFFFFF;
        padding-left: 3px;
        padding-bottom: 2px;
        margin-left:3px;
        background-color:#000000;
    }

    QCheckBox {
        color: #a9b7c6;
        padding: 2px;
    }
    QCheckBox:disabled {
        color: #808086;
        padding: 2px;
    }

    QCheckBox:hover {
        border-radius:4px;
        border-style:solid;
        padding-left: 1px;
        padding-right: 1px;
        padding-bottom: 1px;
        padding-top: 1px;
        border-width:1px;
        border-color: rgb(87, 97, 106);
        background-color:#000000;
    }
    QCheckBox::indicator:checked {

        height: 10px;
        width: 10px;
        border-style:solid;
        border-width: 1px;
        border-color: #e67e22;
        color: #a9b7c6;
        background-color: #e67e22;
    }
    QCheckBox::indicator:unchecked {

        height: 10px;
        width: 10px;
        border-style:solid;
        border-width: 1px;
        border-color: #e67e22;
        color: #a9b7c6;
        background-color: transparent;
    }
    QRadioButton {
        color: #a9b7c6;
        background-color:#000000;
        padding: 1px;
    }
    QRadioButton::indicator:checked {
        height: 10px;
        width: 10px;
        border-style:solid;
        border-radius:5px;
        border-width: 1px;
        border-color: #e67e22;
        color: #a9b7c6;
        background-color: #e67e22;
    }
    QRadioButton::indicator:!checked {
        height: 10px;
        width: 10px;
        border-style:solid;
        border-radius:5px;
        border-width: 1px;
        border-color: #e67e22;
        color: #a9b7c6;
        background-color: transparent;
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
    QTimeEdit {
        color: #a9b7c6;
        background-color:#000000;
    }
    QDateTimeEdit {
        color: #a9b7c6;
        background-color:#000000;
    }
    QDateEdit {
        color: #a9b7c6;
        background-color:#000000;
    }
    QComboBox {
        color: #a9b7c6;
        background: #1e1d23;
    }
    QComboBox:editable {
        background: #1e1d23;
        color: #a9b7c6;
        selection-background-color:#000000;
    }
    QComboBox QAbstractItemView {
        color: #a9b7c6;
        background: #1e1d23;
        selection-color: #FFFFFF;
        selection-background-color:#000000;
    }
    QComboBox:!editable:on, QComboBox::drop-down:editable:on {
        color: #a9b7c6;
        background: #1e1d23;
    }
    QFontComboBox {
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
    QSlider::groove:horizontal {
        height: 5px;
        background: #e67e22;
    }
    QSlider::groove:vertical {
        width: 5px;
        background: #e67e22;
    }
    QSlider::handle:horizontal {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
        border: 1px solid #5c5c5c;
        width: 14px;
        margin: -5px 0;
        border-radius: 7px;
    }
    QSlider::handle:vertical {
        background: qlineargradient(x1:1, y1:1, x2:0, y2:0, stop:0 #b4b4b4, stop:1 #8f8f8f);
        border: 1px solid #5c5c5c;
        height: 14px;
        margin: 0 -5px;
        border-radius: 7px;
    }
    QSlider::add-page:horizontal {
        background: white;
    }
    QSlider::add-page:vertical {
        background: white;
    }
    QSlider::sub-page:horizontal {
        background: #e67e22;
    }
    QSlider::sub-page:vertical {
        background: #e67e22;
    }
    QScrollBar:horizontal {
        max-height: 20px;
        background: rgb(0,0,0);
        border: 1px transparent grey;
        margin: 0px 20px 0px 20px;
    }
    QScrollBar::handle:horizontal {
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 0, 0, 0), stop:0.7 rgba(255, 0, 0, 0), stop:0.71 rgb(230, 126, 34), stop:1 rgb(230, 126, 34));
        border-style: solid;
        border-width: 1px;
        border-color: rgb(0,0,0);
        min-width: 25px;
    }
    QScrollBar::handle:horizontal:hover {
        background: rgb(230, 126, 34);
        border-style: solid;
        border-width: 1px;
        border-color: rgb(0,0,0);
        min-width: 25px;
    }
    QScrollBar::add-line:horizontal {
        border: 1px solid;
        border-color: rgb(0,0,0);
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 0, 0, 0), stop:0.7 rgba(255, 0, 0, 0), stop:0.71 rgb(230, 126, 34), stop:1 rgb(230, 126, 34));
        width: 20px;
        subcontrol-position: right;
        subcontrol-origin: margin;
    }
    QScrollBar::add-line:horizontal:hover {
        border: 1px solid;
        border-color: rgb(0,0,0);
        border-radius: 8px;
        background: rgb(230, 126, 34);
        height: 16px;
        width: 16px;
        subcontrol-position: right;
        subcontrol-origin: margin;
    }
    QScrollBar::add-line:horizontal:pressed {
        border: 1px solid;
        border-color: grey;
        border-radius: 8px;
        background: rgb(230, 126, 34);
        height: 16px;
        width: 16px;
        subcontrol-position: right;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:horizontal {
        border: 1px solid;
        border-color: rgb(0,0,0);
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 0, 0, 0), stop:0.7 rgba(255, 0, 0, 0), stop:0.71 rgb(230, 126, 34), stop:1 rgb(230, 126, 34));
        width: 20px;
        subcontrol-position: left;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:horizontal:hover {
        border: 1px solid;
        border-color: rgb(0,0,0);
        border-radius: 8px;
        background: rgb(230, 126, 34);
        height: 16px;
        width: 16px;
        subcontrol-position: left;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:horizontal:pressed {
        border: 1px solid;
        border-color: grey;
        border-radius: 8px;
        background: rgb(230, 126, 34);
        height: 16px;
        width: 16px;
        subcontrol-position: left;
        subcontrol-origin: margin;
    }
    QScrollBar::left-arrow:horizontal {
        border: 1px transparent grey;
        border-radius: 3px;
        width: 6px;
        height: 6px;
        background: rgb(0,0,0);
    }
    QScrollBar::right-arrow:horizontal {
        border: 1px transparent grey;
        border-radius: 3px;
        width: 6px;
        height: 6px;
        background: rgb(0,0,0);
    }
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
        background: none;
    }
    QScrollBar:vertical {
        max-width: 20px;
        background: rgb(0,0,0);
        border: 1px transparent grey;
        margin: 20px 0px 20px 0px;
    }
    QScrollBar::add-line:vertical {
        border: 1px solid;
        border-color: rgb(0,0,0);
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 0), stop:0.7 rgba(255, 0, 0, 0), stop:0.71 rgb(230, 126, 34), stop:1 rgb(230, 126, 34));
        height: 20px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    QScrollBar::add-line:vertical:hover {
        border: 1px solid;
        border-color: rgb(0,0,0);
        border-radius: 8px;
        background: rgb(230, 126, 34);
        height: 16px;
        width: 16px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    QScrollBar::add-line:vertical:pressed {
        border: 1px solid;
        border-color: grey;
        border-radius: 8px;
        background: rgb(230, 126, 34);
        height: 16px;
        width: 16px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:vertical {
        border: 1px solid;
        border-color: rgb(0,0,0);
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 0), stop:0.7 rgba(255, 0, 0, 0), stop:0.71 rgb(230, 126, 34), stop:1 rgb(230, 126, 34));
        height: 20px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:vertical:hover {
        border: 1px solid;
        border-color: rgb(0,0,0);
        border-radius: 8px;
        background: rgb(230, 126, 34);
        height: 16px;
        width: 16px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:vertical:pressed {
        border: 1px solid;
        border-color: grey;
        border-radius: 8px;
        background: rgb(230, 126, 34);
        height: 16px;
        width: 16px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
        QScrollBar::handle:vertical {
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 0), stop:0.7 rgba(255, 0, 0, 0), stop:0.71 rgb(230, 126, 34), stop:1 rgb(230, 126, 34));
        border-style: solid;
        border-width: 1px;
        border-color: rgb(0,0,0);
        min-height: 25px;
    }
    QScrollBar::handle:vertical:hover {
        background: rgb(230, 126, 34);
        border-style: solid;
        border-width: 1px;
        border-color: rgb(0,0,0);
        min-heigth: 25px;
    }
    QScrollBar::up-arrow:vertical {
        border: 1px transparent grey;
        border-radius: 3px;
        width: 6px;
        height: 6px;
        background: rgb(0,0,0);
    }
    QScrollBar::down-arrow:vertical {
        border: 1px transparent grey;
        border-radius: 3px;
        width: 6px;
        height: 6px;
        background: rgb(0,0,0);
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }"""


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
        self.resize(450, 450)
        self._setupUI()

    def _setupUI(self):
        """Internal function for setting up UI elements."""
        self.central = TabWidget()
        self.centralLayout = QVBoxLayout()
        self.central.setLayout(self.centralLayout)
        self.setCentralWidget(self.central)
        self.statusbar.setObjectName(u"statusbar")

    def apply_settings(self, result):
        """
        apply_settings Activated by MenuBar action to import from external file.

        Args:
            result (dict): Data retreived from external file.
        """
        d = result[0]
        info = d["info"]
        trackers = d["announce"]
        piece_length = info["piece length"]
        self.announce_input.appendPlainText(trackers)

        if "source" in info:
            source = info["source"]
            self.source_input.insert(source)

        if "comment" in info:
            comment = info["comment"]
            self.comment_input.insert(comment)

        if "created by" in info:
            created_by = info["created by"]
            self.created_by_input.insert(created_by)

        if "private" in info:
            if info["private"]:
                self.private.setChecked()

        val_kb = str(int(piece_length) // 1024)
        val_mb = str(int(piece_length) // (1024 ** 2))

        for i in range(self.piece_length.count()):
            if val_kb in self.piece_length.itemText(i):
                self.piece_length.setCurrentIndex(i)
                break
            elif val_mb in self.piece_length.itemText(i):
                self.piece_length.setCurrentIndex(i)
                break
        return


class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.createWidget = CreateWidget()
        self.checkWidget = CheckWidget()
        self.addTab(self.createWidget,"Create")
        self.addTab(self.checkWidget,"Check")



class CheckWidget(QWidget):

    labelRole = QFormLayout.ItemRole.LabelRole
    fieldRole = QFormLayout.ItemRole.FieldRole
    spanRole = QFormLayout.ItemRole.SpanningRole

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.hlayout0 = QHBoxLayout()
        self.hlayout1 = QHBoxLayout()
        self.hlayout2 = QHBoxLayout()
        self.version_label = Label("Bittorrent Version",parent=self)
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.v1button = QRadioButton("v1", parent=self)
        self.v2button = QRadioButton("v2", parent=self)
        self.fileLabel = Label("Torrent File", parent=self)
        self.fileLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.fileInput = LineEdit(parent=self)
        self.browseButton1 = BrowseButton(parent=self)
        self.searchLabel = Label("Search Path", parent=self)
        self.searchLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.searchInput = LineEdit(parent=self)
        self.browseButton2 = BrowseButton(parent=self)
        self.hlayout0.addWidget(self.v1button)
        self.hlayout0.addWidget(self.v2button)
        self.hlayout1.addWidget(self.fileInput)
        self.hlayout1.addWidget(self.browseButton1)
        self.hlayout2.addWidget(self.searchInput)
        self.hlayout2.addWidget(self.browseButton2)
        self.layout.setWidget(0, self.labelRole, self.version_label)
        self.layout.setLayout(0, self.fieldRole, self.hlayout0)
        self.layout.setWidget(1, self.labelRole, self.fileLabel)
        self.layout.setLayout(1, self.fieldRole, self.hlayout1)
        self.layout.setWidget(2, self.labelRole, self.searchLabel)
        self.layout.setLayout(2, self.fieldRole, self.hlayout2)
        self.textbroser = QTextBrowser(parent=self)
        self.layout.setWidget(3, self.spanRole, self.textbroser)

        self.layout.setObjectName(u"CheckWidget_layout")
        self.hlayout1.setObjectName("CheckWidget_hlayout1")
        self.hlayout2.setObjectName("CheckWidget_hlayout2")
        self.browseButton2.setObjectName("CheckWidget_browseButton2")
        self.browseButton1.setObjectName("CheckWidget_browseButton1")
        self.fileLabel.setObjectName("CheckWidget_fileLabel")
        self.searchLabel.setObjectName("CheckWidget_searchLabel")
        self.fileInput.setObjectName("CheckWidget_fileInput")
        self.searchInput.setObjectName("CheckWidget_searchInput")


class CreateWidget(QWidget):

    labelRole = QFormLayout.ItemRole.LabelRole
    fieldRole = QFormLayout.ItemRole.FieldRole
    spanRole = QFormLayout.ItemRole.SpanningRole

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.hlayout1 = QHBoxLayout()
        self.hlayout2 = QHBoxLayout()
        self.hlayout0 = QHBoxLayout()

        self.version_label = Label("Bittorrent Version",parent=self)
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.v1button = QRadioButton("v1", parent=self)
        self.v2button = QRadioButton("v2", parent=self)
        self.layout.setWidget(0, self.labelRole, self.version_label)
        self.layout.setLayout(0, self.fieldRole, self.hlayout0)
        self.hlayout0.addWidget(self.v1button)
        self.hlayout0.addWidget(self.v2button)

        self.path_label = Label("Path", parent=self)
        self.path_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.path_input = LineEdit(parent=self)
        self.path_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.browse_button = BrowseButton(parent=self)
        self.hlayout1.addWidget(self.path_input)
        self.hlayout1.addWidget(self.browse_button)
        self.layout.setWidget(1, self.labelRole, self.path_label)
        self.layout.setLayout(1, self.fieldRole, self.hlayout1)

        self.output_label = Label("Output", parent=self)
        self.output_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.output_input = LineEdit(parent=self)
        self.output_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.setWidget(2, self.labelRole, self.output_label)
        self.layout.setWidget(2, self.fieldRole, self.output_input)

        self.source_label = Label("Source:", parent=self)
        self.source_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.source_input = LineEdit(parent=self)
        self.source_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.setWidget(3, self.labelRole, self.source_label)
        self.layout.setWidget(3, self.fieldRole, self.source_input)

        self.comment_label = Label("Comment:", parent=self)
        self.comment_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.comment_input = LineEdit(parent=self)
        self.comment_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.setWidget(4, self.labelRole, self.comment_label)
        self.layout.setWidget(4, self.fieldRole, self.comment_input)

        self.announce_label = Label("Trackers:", parent=self)
        self.announce_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.announce_input = TextEdit(parent=self)
        self.layout.setWidget(5, self.labelRole, self.announce_label)
        self.layout.setWidget(5, self.fieldRole, self.announce_input)

        self.piece_length_label = Label("Piece Length:", parent=self)
        self.piece_length_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.piece_length = ComboBox(parent=self)
        self.private = QCheckBox("Private Tracker",parent=self)
        self.private.setStyleSheet("QCheckBox {color: #e1e7f6; font-size: 11pt;}")
        self.spacer = QSpacerItem(50,0)
        self.hlayout2.addWidget(self.piece_length)
        self.hlayout2.addItem(self.spacer)
        self.hlayout2.addWidget(self.private)
        self.layout.setWidget(6, self.labelRole, self.piece_length_label)
        self.layout.setLayout(6, self.fieldRole, self.hlayout2)

        self.submit_button = SubmitButton("Submit",parent=self)
        self.layout.setWidget(7, self.spanRole,self.submit_button)

        self.layout.setObjectName(u"createWidget_formLayout")
        self.hlayout2.setObjectName("createWidget_hlayout2")
        self.submit_button.setObjectName("createWidget_submit_button")
        self.private.setObjectName("createWidget_private")
        self.path_label.setObjectName("createWidget_path_label")
        self.path_input.setObjectName("createWidget_path_input")
        self.piece_length.setObjectName("createWidget_piece_length")
        self.piece_length_label.setObjectName("createWidget_piece_length_label")
        self.source_label.setObjectName("createWidget_source_label")
        self.source_input.setObjectName("createWidget_source_input")
        self.announce_input.setObjectName("createWidget_announce_input")
        self.announce_label.setObjectName("createWidget_announce_label")
        self.comment_input.setObjectName("createWidget_comment_input")
        self.comment_label.setObjectName("createWidget_comment_label")
        self.browse_button.setObjectName("createWidget_browse_button")




class BrowseButton(QToolButton):
    """
    BrowseButton ToolButton for activating filebrowser.

    Subclass:
        QToolButton : PyQt6 Button Widget
    """

    stylesheet = """
        QPushButton {
            border-color: #F80;
            border-width: 1px;
            border-style: solid;
            color: #000;
            padding: 4px;
            background-color: #ddd;
        }
        QPushButton::hover{
            background-color: #ced;
        }"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        """
        __init__ public constructor for BrowseButton Class.
        """
        self.setText("...")
        self.window = parent
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pressed.connect(self.browse)

    def browse(self):
        """
        browse Action performed when user presses button.

        Opens File/Folder Dialog.

        Returns:
            str: Path to file or folder to include in torrent.
        """
        caption = "Choose File or Root Folder"
        path = QFileDialog.getExistingDirectory(parent=self.window, caption=caption)
        self.window.path_input.insert(str(path))
        _, size, piece_length = torrentfile.utils.path_stat(path)

        if piece_length < (2**20):
            val = f"{piece_length//(2**10)}KB"

        else:
            val = f"{piece_length//(2**20)}MB"

        for i in range(self.window.piece_length.count()):
            if self.window.piece_length.itemText(i) == val:
                self.window.piece_length.setCurrentIndex(i)
                break
        return size


class SubmitButton(QPushButton):
    """
    SubmitButton Button to signal finished setup options.

    Subclass:
        QPushButton
    """

    stylesheet = """
        QPushButton {
            border-width: 4px;
            border-style: outset;
            border-top-color: #999999;
            border-left-color: #999999;
            border-right-color: #707070;
            border-bottom-color: #707070;
            border-bottom-width: 2px;
            border-radius: 8px;
            padding: 3px;
            margin: 3px;
            color: #fff;
            background-color: #575757;
        }
        QPushButton::hover{
            border-top-color: #b4b4b4;
            border-left-color: #929292;
            border-right-color: #7f7f7f;
            border-bottom-color: #737373;
            background-color: #8d8d8d;
            color: #fff;
        }"""

    def __init__(self, text, parent=None):
        """Public Constructor for Submit Button.

        Args:
            text (str): Text displayed on the button itself.
            parent (QWidget, optional): This Widget's parent. Defaults to None.
        """
        super().__init__(text, parent=parent)
        self._text = text
        self.window = parent
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setText(text)
        self.setStyleSheet(self.stylesheet)
        self.pressed.connect(self.submit)

    def submit(self):
        """Submit Action performed when user presses Submit Button."""
        window = self.window

        # Gather Information from other Widgets.
        path = window.path_input.text()
        private = 1 if window.private.isChecked() else 0
        source = window.source_input.text()

        # at least 1 tracker input is required
        announce = window.announce_input.toPlainText()
        announce = announce.split("\n")

        # Calculates piece length if not specified by user.
        created_by = window.created_by_input.text()
        piece_length = window.piece_length.currentText()

        denom = piece_length[-2:]
        val = piece_length[:-2]

        if denom == "KB":
            val = int(val) * 1024

        elif denom == "MB":
            val = int(val) * (1024 ** 2)

        comment = window.comment_input.text()

        tfile = torrentfile.TorrentFile(
            path=path,
            private=private,
            source=source,
            announce=announce,
            created_by=created_by,
            piece_length=val,
            comment=comment,
        )
        tfile.assemble()
        try:
            save_dir = os.getenv("HOME")
        except:
            save_dir = os.getenv("USERPROFILE")
        save_file = os.path.join(save_dir, os.path.basename(path) + ".torrent")
        save_location = QFileDialog.getSaveFileName(
            parent=window, caption="Save Location", directory=save_file
        )
        tfile.write(save_location)
        print("success")


class Label(QLabel):
    """Label Identifier for Window Widgets.

    Subclass: QLabel
    """

    stylesheet = """QLabel {
        color: #fff;
        padding: 3px;
    }"""

    def __init__(self, text, parent=None):
        super().__init__(text, parent=parent)
        self.setStyleSheet(self.stylesheet)
        font = self.font()
        font.setBold(True)
        font.setPointSize(12)
        self.setFont(font)

class LineEdit(QLineEdit):

    stylesheet = """QLineEdit {
        border-color: #3a3a3a;
        border-width: 1px;
        border-radius: 4px;
        border-style: inset;
        padding: 0 8px;
        color: #fff;
        background: #646464;
        selection-background-color: #bbbbbb;
        selection-color: #3c3f41;
    }"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.setStyleSheet(self.stylesheet)


class TextEdit(QPlainTextEdit):

    stylesheet = """QPlainTextEdit {
        color: #0F0;
        background-color: #2a2a2a;
    }"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.setBackgroundVisible(True)
        self.setStyleSheet(self.stylesheet)


class ComboBox(QComboBox):

    stylesheet = """
        QCombobox {
            margin: 10px;
        }
        QComboBox QAbstractItemView {
            padding: 4px;
            background-color: #444;
            color: #FFF;
            border: 1px solid brown;
        }
        QCombobox QLineEdit {
            margin: 10px;
        }"""

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        self.args = args
        self.kwargs = kwargs
        self.setStyleSheet(self.stylesheet)
        self.addItem("")
        for exp in range(14, 24):
            if exp < 20:
                item = str((2 ** exp) // (2**10)) + "KB"
            else:
                item = str((2 ** exp) // (2**20)) + "MB"
            self.addItem(item)
        self.setEditable(False)

class Application(QApplication):
    def __init__(self, args=None):
        if not args:
            args = sys.argv
        super().__init__(args)

def start():
    app = Application()
    window = Window(parent=None, app=app)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    start()
