import os
import math
from datetime import datetime
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
        self.sizeLabel = Label("Total Size: ", parent=self)
        self.totalPiecesLabel = Label("Total Pieces: ", parent=self)
        self.trackerLabel = Label("Tracker: ", parent=self)
        self.privateLabel = Label("Private: ", parent=self)
        self.sourceLabel = Label("Source: ", parent=self)
        self.commentLabel = Label("Comment: ", parent=self)
        self.dateCreatedLabel = Label("Creation Date: ", parent=self)
        self.createdByLabel = Label("Created By: ", parent=self)
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
        self.createdByEdit = InfoLineEdit(parent=self)
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
        self.layout.addWidget(self.createdByLabel, 9, 0, 1, 1)
        self.layout.addWidget(self.createdByEdit, 9, 1, 1, 1)
        self.layout.addWidget(self.dateCreatedLabel, 10, 0, 1, 1)
        self.layout.addWidget(self.dateCreatedEdit, 10, 1, 1, 1)
        self.layout.addWidget(self.contentsLabel, 11, 0, 1, 1)
        self.layout.addWidget(self.contentsEdit, 11, 1, 4, 1)
        self.selectButton = SelectButton("Select Torrent", parent=self)
        self.layout.addWidget(self.selectButton, 15, 0, -1, -1)

    def fill(self, kws):
        self.pathEdit.setText(kws["path"])
        self.nameEdit.setText(kws["name"])
        self.commentEdit.setText(kws["comment"])
        self.trackerEdit.setText("; ".join(kws["announce"]))
        self.sourceEdit.setText(kws["source"])
        self.dateCreatedEdit.setText(str(kws["creation_date"]))
        self.createdByEdit.setText(kws["created_by"])
        self.privateEdit.setText(kws["private"])
        piece_length = kws["piece_length"]
        plength_str = denom(piece_length) + " / (" +  pretty_int(piece_length) + ")"
        self.pieceLengthEdit.setText(plength_str)
        size = denom(kws["length"]) + " / (" + pretty_int(kws["length"]) + ")"
        self.sizeEdit.setText(size)
        total_pieces = math.ceil(kws["length"] / kws["piece_length"])
        self.totalPiecesEdit.setText(str(total_pieces))
        for item in kws["contents"]:
            self.contentsEdit.append(item)
        for widg in [self.pathEdit, self.nameEdit, self.trackerEdit,
                     self.privateEdit, self.pieceLengthEdit, self.sizeEdit,
                     self.totalPiecesEdit]:
            widg.setCursorPosition(0)



class InfoLineEdit(QLineEdit):

    stylesheet = altLineEditStyleSheet

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setReadOnly(True)
        self.setStyleSheet(self.stylesheet)
        self.setDragEnabled(True)
        font = self.font()
        font.setBold(True)
        self.setFont(font)


class SelectButton(QPushButton):

    stylesheet = pushButtonStyleSheet

    def __init__(self, text, parent=None):
        super().__init__(text, parent=parent)
        self.setStyleSheet(self.stylesheet)
        self.pressed.connect(self.selectTorrent)


    def selectTorrent(self):
        caption = "Select '.torrent' file"
        files = QFileDialog.getOpenFileName(parent=self,
                                            caption=caption,
                                            filter="*.torrent")
        if not files: return
        meta = pyben.load(files[0])
        info = meta["info"]
        keywords = {}
        keywords["path"] = files[0]
        keywords["piece_length"] = info["piece length"]
        if "created by" in meta:
            keywords["created_by"] = meta["created by"]
        else:
            keywords["created_by"] = ""
        for kw in ["name", "length", "comment", "source"]:
            if kw in info:
                keywords[kw] = info[kw]
            else:
                keywords[kw] = ""
        if "announce list" in info:
            keywords["announce"] = info["announce list"] + [meta["announce"]]
        else:
            keywords["announce"] = [meta["announce"]]
        files, size = [], 0
        if "files" in info:
            for entry in info["files"]:
                files.append(os.path.join(*entry["path"]))
                size += entry["length"]
            keywords["contents"] = files
            keywords["length"] = size
        elif "file tree" in info:
            paths = parse_filetree(info["file tree"])
            for k, v in paths.items():
                files.append(k)
                size += v
            keywords["contents"] = files
            keywords["length"] = size
        if "creation date" in meta:
            date = datetime.fromtimestamp(meta["creation date"])
            text = date.strftime("%B %d, %Y %H:%M")
            keywords["creation_date"] = text
        else:
            keywords["creation_date"] = ""
        if "private" in info:
            keywords["private"] = "True"
        else:
            keywords["private"] = "False"
        if "contents" not in keywords:
            keywords["contents"] = [info["name"]]
        self.parent().fill(keywords)


def parse_filetree(filetree):
    paths = {}
    for key in filetree:
        if key == "":
            paths[key] = filetree[key]["length"]
        else:
            out = parse_filetree(filetree[key])
            for k,v in out.items():
                paths[os.path.join(key, k)] = v
    return paths


def denom(num):
    txt = str(num)
    if num < 1000:
        return txt
    if 1000 <= num <= 999999:
        return "".join([txt[:-3], ".", txt[-3], "KB"])
    if 1_000_000 <= num < 1_000_000_000:
        return "".join([txt[:-6], ".", txt[-6], "MB"])
    if num >= 1_000_000_000:
        return "".join([txt[:-9], ".", txt[-9], "GB"])


def pretty_int(num):
    text, seq = str(num), []
    digits, count = len(text) - 1, 0
    while digits >= 0:
        if count == 3:
            seq.insert(0,",")
            count = 0
        seq.insert(0,text[digits])
        count += 1
        digits -= 1
    return "".join(seq) + " Bytes"
