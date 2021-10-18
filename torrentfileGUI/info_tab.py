import os
import pyben


from PyQt6.QtWidgets import (QFileDialog, QLineEdit, QPushButton,
                             QWidget, QGridLayout)


from torrentfileGUI.qss import pushButtonStyleSheet, altLineEditStyleSheet
from PyQt6.QtWidgets import QWidget, QGridLayout
from torrentfileGUI.widgets import Label, TextEdit

class InfoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Labels
        self.pathLabel = Label("Path: ", parent=self)
        self.nameLabel = Label("Name: ", parent=self)
        self.pieceLengthLabel = Label("Piece Length: ", parent=self)
        self.sizeLabel = Label("Size: ", parent=self)
        self.totalPiecesLabel = Label("Number of Pieces: ", parent=self)
        self.trackerLabel = Label("Tracker: ", parent=self)
        self.privateLabel = Label("Private: ", parent=self)
        self.sourceLabel = Label("Source: ", parent=self)
        self.commentLabel = Label("Comment: ", parent=self)
        self.dateCreatedLabel = Label("Creation Date: ", parent=self)
        self.contentsLabel = Label("Contents: ", parent=self)
        self.contentsEdit = TextEdit(parent=self)
        self.sourceEdit = InfoLineEdit(parent=self)
        self.pathEdit = InfoLineEdit(parent=self)
        self.nameEdit = InfoLineEdit(parent=self)
        self.pieceLengthEdit = InfoLineEdit(parent=self)
        self.sizeEdit = InfoLineEdit(parent=self)
        self.privateEdit = InfoLineEdit(parent=self)
        self.commentEdit = InfoLineEdit(parent=self)
        self.trackerEdit = InfoLineEdit(parent=self)
        self.totalPiecesEdit = InfoLineEdit(parent=self)
        self.dateCreatedEdit = InfoLineEdit(parent=self)
        self.layout.addWidget(self.pathLabel,0,0,1,1)
        self.layout.addWidget(self.pathEdit,0,1,1,1)
        self.layout.addWidget(self.nameLabel,1,0,1,1)
        self.layout.addWidget(self.nameEdit,1,1,1,1)
        self.layout.addWidget(self.pieceLengthLabel,2,0,1,1)
        self.layout.addWidget(self.pieceLengthEdit,2,1,1,1)
        self.layout.addWidget(self.sizeLabel,3,0,1,1)
        self.layout.addWidget(self.sizeEdit,3,1,1,1)
        self.layout.addWidget(self.totalPiecesLabel,4,0,1,1)
        self.layout.addWidget(self.totalPiecesEdit,4,1,1,1)
        self.layout.addWidget(self.trackerLabel,5,0,1,1)
        self.layout.addWidget(self.trackerEdit,5,1,1,1)
        self.layout.addWidget(self.privateLabel,6,0,1,1)
        self.layout.addWidget(self.privateEdit,6,1,1,1)
        self.layout.addWidget(self.sourceLabel,7,0,1,1)
        self.layout.addWidget(self.sourceEdit,7,1,1,1)
        self.layout.addWidget(self.commentLabel, 8, 0, 1, 1)
        self.layout.addWidget(self.commentEdit, 8, 1, 1, 1)
        self.layout.addWidget(self.dateCreatedLabel, 9, 0, 1, 1)
        self.layout.addWidget(self.dateCreatedEdit, 9, 1, 1, 1)
        self.layout.addWidget(self.contentsLabel, 10, 0, 1, 1)
        self.layout.addWidget(self.contentsEdit, 10, 1, 1, 1)
        self.selectButton = SelectButton("Select Torrent", parent=self)
        self.layout.addWidget(self.selectButton, 11, 0, -1, -1)

    def fill(self, flags):
        self.pathEdit.setText(flags.path)
        self.nameEdit.setText(flags.name)
        if flags.comment:
            self.commentEdit.setText(flags.comment)
        self.pieceLengthEdit.setText(str(flags.piece_length))
        self.trackerEdit.setText(flags.tracker)
        if flags.source:
            self.sourceEdit.setText(flags.source)
        if flags.date_created:
            self.dateCreatedEdit.setText(flags.date_created)
        if flags.private:
            self.privateEdit.setText("True")
        else:
            self.privateEdit.setText("False")
        if flags.size:
            self.sizeEdit.setText(str(flags.size))
        if flags.contents:
            for item in flags.contents:
                string = f"* {item} \n"
                self.contentsEdit.append(string)



class InfoLineEdit(QLineEdit):

    stylesheet = altLineEditStyleSheet

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.setReadOnly(True)
        self.setStyleSheet(self.stylesheet)
        self.setDragEnabled(True)



class SelectButton(QPushButton):

    stylesheet = pushButtonStyleSheet

    def __init__(self, text, parent=None):
        super().__init__(text, parent=parent)
        self.setStyleSheet(self.stylesheet)
        self.pressed.connect(self.selectTorrent)


    def selectTorrent(self):
        files = QFileDialog.getOpenFileName(
            parent=self, caption="select '.torrent' file", filter="*.torrent")
        path = files[0]
        meta = pyben.load(path)
        info = meta["info"]
        flags = object()
        flags.path = path
        flags.piece_length = info["piece length"]
        flags.name = info["name"]
        flags.tracker = meta["announce"]
        if "comment" in info:
            flags.comment = info["comment"]
        else:
            flags.comment = None

        if "source" in info:
            flags.source = info["source"]
        else:
            flags.source = None

        if "private" in info:
            flags.private = info["private"]
        else:
            flags.private = None

        if "length" in info:
            flags.length = info["length"]
        else:
            flags.length = None

        if "date created" in meta:
            flags.date_created = meta["date created"]
        else:
            flags.date_created = None

        contents, size = [], 0
        if "files" in info:
            for item in info["files"]:
                size += item["length"]
                name = os.path.join(*item["path"])
                contents.append(name)
        flags.contents = contents
        flags.size = size

        self.parent().fill(flags)
