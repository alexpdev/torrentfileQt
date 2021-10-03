import os
import sys
from pathlib import Path
import threading
import pyben
from PyQt6.QtCore import Qt


from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFileDialog,
                             QHBoxLayout, QLabel, QLineEdit, QSpacerItem,
                             QPlainTextEdit, QTextBrowser, QPushButton,
                             QToolButton, QWidget, QFormLayout, QTabWidget,
                             QRadioButton, QGridLayout, QTextEdit)
import torrentfile
from torrentfileGUI.qss import (pushButtonStyleSheet, comboBoxStyleSheet,
                                tabBarStyleSheet, lineEditStyleSheet,
                                toolButtonStyleSheet, checkBoxStyleSheet,
                                labelStyleSheet, textEditStyleSheet,
                                altLineEditStyleSheet)


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
        self.addTab(self.createWidget,"Create Torrent")
        self.addTab(self.checkWidget,"Check Torrent")
        self.addTab(self.infoWidget, "Torrent Info")




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


class CreateWidget(QWidget):

    labelRole = QFormLayout.ItemRole.LabelRole
    fieldRole = QFormLayout.ItemRole.FieldRole
    spanRole = QFormLayout.ItemRole.SpanningRole

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setup_Ui()
        self.content_dir = None
        self.outpath = None


    def setup_Ui(self):
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.hlayout1 = QHBoxLayout()
        self.hlayout2 = QHBoxLayout()
        self.hlayout3 = QHBoxLayout()
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
        self.output_input.setDisabled(True)
        self.output_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.output_button = OutButton(parent=self)
        self.hlayout3.addWidget(self.output_input)
        self.hlayout3.addWidget(self.output_button)
        self.layout.setWidget(2, self.labelRole, self.output_label)
        self.layout.setLayout(2, self.fieldRole, self.hlayout3)

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
        self.announce_input = PlainTextEdit(parent=self)
        self.layout.setWidget(5, self.labelRole, self.announce_label)
        self.layout.setWidget(5, self.fieldRole, self.announce_input)

        self.piece_length_label = Label("Piece Length:", parent=self)
        self.piece_length_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.piece_length = ComboBox(parent=self)
        self.private = CheckBox("Private Tracker",parent=self)
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



class TextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        print("It's alive!")
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoBulletList)



class CheckBox(QCheckBox):

    stylesheet = checkBoxStyleSheet

    def __init__(self,label, parent=None):
        super().__init__(label, parent=parent)
        self.setStyleSheet(self.stylesheet)


class Flags:
    pass


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
        self.pressed.connect(self.browse)

    def browse(self):
        """
        browse Action performed when user presses button.

        Opens File/Folder Dialog.

        Returns:
            str: Path to file or folder to include in torrent.
        """
        caption = "Choose Root Directory"
        path = QFileDialog.getExistingDirectory(parent=self, caption=caption)
        path = os.path.realpath(path)
        self.window.path_input.clear()
        self.window.path_input.insert(path)
        self.window.output_input.clear()
        outdir = os.path.dirname(str(path))
        outfile = os.path.splitext(os.path.split(str(path))[-1])[0] + ".torrent"
        outpath = os.path.realpath(os.path.join(outdir, outfile))
        self.window.output_input.insert(outpath)
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


class OutButton(BrowseButton):

    stylesheet = toolButtonStyleSheet

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.pressed.connect(self.output)
        self.setStyleSheet(self.stylesheet)

    def output(self):
        caption = "Select Output Directory"
        outpath = QFileDialog.getExistingDirectory(parent=self,caption=caption)
        self.window.output_input.clear()
        if self.parent().content_dir:
            name = os.path.split(self.parent().content_dir)[-1]
            outpath = os.path.join(str(outpath), name)
            outpath = os.path.realpath(outpath)
        self.parent().output_input.insert(outpath)
        self.parent().outpath = outpath


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
        flags = Flags()
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


class SubmitButton(QPushButton):
    """
    SubmitButton Button to signal finished setup options.

    Subclass:
        QPushButton
    """

    stylesheet = pushButtonStyleSheet

    def __init__(self, text, parent=None):
        """Public Constructor for Submit Button.

        Args:
            text (str): Text displayed on the button itself.
            parent (QWidget, optional): This Widget's parent. Defaults to None.
        """
        super().__init__(text, parent=parent)
        self._text = text
        self.widget = parent
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setText(text)
        self.setStyleSheet(self.stylesheet)
        self.pressed.connect(self.submit)

    def submit(self):
        """Submit Action performed when user presses Submit Button."""
        flags = Flags()
        # Gather Information from other Widgets.
        flags.path = self.widget.path_input.text()
        flags.private = 1 if self.widget.private.isChecked() else 0
        flags.source = self.widget.source_input.text()

        # at least 1 tracker input is required
        announce = self.widget.announce_input.toPlainText()
        flags.announce = announce.split("\n")

        # Calculates piece length if not specified by user.
        flags.outfile = self.widget.output_input.text()
        piece_length_index = self.widget.piece_length.currentIndex()
        data = self.widget.piece_length.itemData(piece_length_index)
        print(data)
        flags.piece_length = data
        flags.created_by = None
        flags.comment = self.widget.comment_input.text()

        if self.widget.v1button.isChecked():
            tfile = torrentfile.TorrentFile(flags)
        else:
            tfile = torrentfile.TorrentFileV2(flags)

        def assemble(tfile):
            tfile.assemble()
            if not flags.outfile.endswith(".torrent"):
                flags.outfile = Path(flags.output).with_suffix(".torrent")
            tfile.write(flags.outfile)

        t = threading.Thread(group=None, target=assemble,args=(tfile,))
        t.run()



class CheckButton(SubmitButton):

    stylesheet = pushButtonStyleSheet

    def __init__(self, text, parent=None):
        super().__init__(text, parent=parent)
        self.pressed.connect(self.submit)
        self.setStyleSheet(self.stylesheet)

    def submit(self):
        pass

class Label(QLabel):
    """Label Identifier for Window Widgets.

    Subclass: QLabel
    """

    stylesheet = labelStyleSheet

    def __init__(self, text, parent=None):
        super().__init__(text, parent=parent)
        self.setStyleSheet(self.stylesheet)
        font = self.font()
        font.setBold(True)
        font.setPointSize(12)
        self.setFont(font)


class LineEdit(QLineEdit):

    stylesheet = lineEditStyleSheet

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.setStyleSheet(self.stylesheet)


class InfoLineEdit(QLineEdit):

    stylesheet = altLineEditStyleSheet

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.setReadOnly(True)
        self.setStyleSheet(self.stylesheet)
        self.setDragEnabled(True)


class PlainTextEdit(QPlainTextEdit):

    stylesheet = textEditStyleSheet

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.setBackgroundVisible(True)
        self.setStyleSheet(self.stylesheet)


class ComboBox(QComboBox):

    stylesheet = comboBoxStyleSheet

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
            self.addItem(item, 2**exp)
        self.setEditable(False)


class Application(QApplication):

    def __init__(self, args=None):
        if not args:
            args = sys.argv
        super().__init__(args)
