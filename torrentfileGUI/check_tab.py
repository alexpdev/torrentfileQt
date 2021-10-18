from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (QHBoxLayout, QTextBrowser, QPushButton,
                             QWidget, QFormLayout, QRadioButton)

from torrentfileGUI.qss import (pushButtonStyleSheet)

from torrentfileGUI.widgets import BrowseButton, Label, LineEdit

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
        self.checkButton = CheckButton("Check", parent=self)

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
        pass
