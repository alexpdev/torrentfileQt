import os
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (QHBoxLayout, QTextBrowser, QPushButton,
                             QWidget, QFormLayout, QRadioButton, QToolButton,
                             QFileDialog, )

from torrentfile.metafile import Checker

from torrentfileQt.qss import (pushButtonStyleSheet, toolButtonStyleSheet)

from torrentfileQt.widgets import Label, LineEdit

class CheckWidget(QWidget):

    labelRole = QFormLayout.ItemRole.LabelRole
    fieldRole = QFormLayout.ItemRole.FieldRole
    spanRole = QFormLayout.ItemRole.SpanningRole

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.hlayout1 = QHBoxLayout()
        self.hlayout2 = QHBoxLayout()

        self.fileLabel = Label("Torrent File", parent=self)
        self.fileLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.fileInput = LineEdit(parent=self)
        self.browseButton1 = BrowseButton(parent=self)
        self.browseButton1.setInputWidget(self.fileInput)

        self.searchLabel = Label("Search Path", parent=self)
        self.searchLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.searchInput = LineEdit(parent=self)
        self.browseButton2 = BrowseButton(parent=self)
        self.browseButton2.setInputWidget(self.searchInput)
        self.checkButton = CheckButton("Check", parent=self)

        self.hlayout1.addWidget(self.fileInput)
        self.hlayout1.addWidget(self.browseButton1)
        self.hlayout2.addWidget(self.searchInput)
        self.hlayout2.addWidget(self.browseButton2)

        self.layout.setWidget(1, self.labelRole, self.fileLabel)
        self.layout.setLayout(1, self.fieldRole, self.hlayout1)
        self.layout.setWidget(2, self.labelRole, self.searchLabel)
        self.layout.setLayout(2, self.fieldRole, self.hlayout2)
        self.textbrowser = QTextBrowser(parent=self)
        self.layout.setWidget(3, self.spanRole, self.textbrowser)
        self.layout.setWidget(4, self.spanRole, self.checkButton)

        self.layout.setObjectName(u"CheckWidget_layout")
        self.hlayout1.setObjectName("CheckWidget_hlayout1")
        self.hlayout2.setObjectName("CheckWidget_hlayout2")
        self.browseButton2.setObjectName("CheckWidget_browseButton2")
        self.browseButton1.setObjectName("CheckWidget_browseButton1")
        self.fileLabel.setObjectName("CheckWidget_fileLabel")
        self.searchLabel.setObjectName("CheckWidget_searchLabel")
        self.fileInput.setObjectName("CheckWidget_fileInput")
        self.searchInput.setObjectName("CheckWidget_searchInput")


class CheckButton(QPushButton):

    stylesheet = pushButtonStyleSheet

    def __init__(self, text, parent=None):
        super().__init__(text, parent=parent)
        self.pressed.connect(self.submit)
        self.setStyleSheet(self.stylesheet)

    def submit(self):
        Checker

class BrowseButton(QToolButton):
    """
    BrowseButton ToolButton for activating filebrowser.

    Subclass:
        QToolButton : PyQt6 Button Widget
    """

    stylesheet = toolButtonStyleSheet

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        """
        __init__ public constructor for BrowseButton Class.
        """
        self.setText("...")
        self.window = parent
        self.setStyleSheet(self.stylesheet)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.inputWidget = None
        self.pressed.connect(self.browse)

    def setInputWidget(self, widget):
        self.inputWidget = widget

    def browse(self, path=None):
        """
        browse Action performed when user presses button.

        Opens File/Folder Dialog.

        Returns:
            str: Path to file or folder to include in torrent.
        """
        caption = "Choose Root Directory"
        if not path:
            path = QFileDialog.getExistingDirectory(parent=self, caption=caption)
        if not path: return
        path = os.path.realpath(path)
        self.inputWidget.clear()
        self.inputWidget.setText(path)
