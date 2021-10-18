import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFileDialog,
                             QLabel, QLineEdit, QPlainTextEdit, QToolButton,
                             QTextEdit)

import torrentfile
from torrentfileGUI.qss import (comboBoxStyleSheet, lineEditStyleSheet,
                                toolButtonStyleSheet, checkBoxStyleSheet,
                                labelStyleSheet, textEditStyleSheet)


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
