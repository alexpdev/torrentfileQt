import os
import threading
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (QFileDialog, QHBoxLayout, QSpacerItem, QToolButton,
                             QPushButton, QWidget, QFormLayout, QRadioButton,
                             QGridLayout)

from torrentfile import TorrentFile, TorrentFileV2, TorrentFileHybrid
from torrentfileGUI.qss import pushButtonStyleSheet, toolButtonStyleSheet
from torrentfileGUI.widgets import (CheckBox, LineEdit, BrowseButton, Label,
                                    PlainTextEdit, ComboBox)

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
        self.hybridbutton = QRadioButton("v1+2 (hybrid)", parent=self)
        self.layout.setWidget(0, self.labelRole, self.version_label)
        self.layout.setLayout(0, self.fieldRole, self.hlayout0)
        self.hlayout0.addWidget(self.v1button)
        self.hlayout0.addWidget(self.v2button)
        self.hlayout0.addWidget(self.hybridbutton)

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



def torrentfile_create(args, obj):
    tfile = obj(**args)
    tfile.write()
    return


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
        # Gather Information from other Widgets.
        args = {}
        args["path"] = self.widget.path_input.text()
        args["private"] = 1 if self.widget.private.isChecked() else 0
        args["source"] = self.widget.source_input.text()

        # at least 1 tracker input is required
        announce = self.widget.announce_input.toPlainText()
        announce = [i for i in announce.split("\n") if i]
        args["announce"] = announce[0]
        args["announce_list"] = announce[1:]

        # Calculates piece length if not specified by user.
        args["outfile"] = self.widget.output_input.text()
        piece_length_index = self.widget.piece_length.currentIndex()
        args["piece_length"] = self.widget.piece_length.itemData(piece_length_index)
        args["comment"] = self.widget.comment_input.text()

        if self.widget.hybridbutton.isChecked():
            obj = TorrentFileHybrid
        elif self.widget.v2button.isChecked():
            obj = TorrentFileV2
        else:
            obj = TorrentFile
        t = threading.Thread(group=None, target=torrentfile_create,args=(args,obj))
        t.run()



class OutButton(QToolButton):

    stylesheet = toolButtonStyleSheet

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setText("...")
        self.window = parent
        self.setStyleSheet(self.stylesheet)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pressed.connect(self.output)

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
