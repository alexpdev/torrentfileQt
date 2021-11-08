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

import os
import logging
from pathlib import Path
from collections.abc import Sequence

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidget,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QToolButton,
    QTreeWidget,
    QTreeWidgetItem,
    QLineEdit,
    QLabel,
)
from torrentfile.progress import CheckerClass


from torrentfileQt.qss import (
    logTextEditSheet,
    lineEditSheet,
    labelSheet,
    pushButtonSheet,
    toolButtonSheet,
    treeSheet,
    headerSheet,
)


class CheckWidget(QWidget):

    labelRole = QFormLayout.ItemRole.LabelRole
    fieldRole = QFormLayout.ItemRole.FieldRole
    spanRole = QFormLayout.ItemRole.SpanningRole

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.window = parent.window
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.hlayout1 = QHBoxLayout()
        self.hlayout2 = QHBoxLayout()

        self.fileLabel = Label("Torrent File", parent=self)
        self.fileLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.fileInput = LineEdit(parent=self)
        self.browseButton1 = BrowseTorrents(parent=self)

        self.searchLabel = Label("Search Path", parent=self)
        self.searchLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.searchInput = LineEdit(parent=self)
        self.browseButton2 = BrowseFolders(parent=self)
        self.checkButton = ReCheckButton("Check", parent=self)

        self.hlayout1.addWidget(self.fileInput)
        self.hlayout1.addWidget(self.browseButton1)
        self.hlayout2.addWidget(self.searchInput)
        self.hlayout2.addWidget(self.browseButton2)

        self.layout.setWidget(1, self.labelRole, self.fileLabel)
        self.layout.setLayout(1, self.fieldRole, self.hlayout1)
        self.layout.setWidget(2, self.labelRole, self.searchLabel)
        self.layout.setLayout(2, self.fieldRole, self.hlayout2)
        self.textEdit = LogTextEdit(parent=self)
        self.treeWidget = TreeWidget(parent=self)
        self.layout.setWidget(3, self.spanRole, self.textEdit)
        self.layout.setWidget(4, self.spanRole, self.treeWidget)
        self.layout.setWidget(5, self.spanRole, self.checkButton)

        self.layout.setObjectName("CheckWidget_layout")
        self.hlayout1.setObjectName("CheckWidget_hlayout1")
        self.hlayout2.setObjectName("CheckWidget_hlayout2")
        self.browseButton2.setObjectName("CheckWidget_browseButton2")
        self.browseButton1.setObjectName("CheckWidget_browseButton1")
        self.fileLabel.setObjectName("CheckWidget_fileLabel")
        self.searchLabel.setObjectName("CheckWidget_searchLabel")
        self.fileInput.setObjectName("CheckWidget_fileInput")
        self.searchInput.setObjectName("CheckWidget_searchInput")


class ReCheckButton(QPushButton):
    """Button Widget for validating torrent files against downloaded contents.

    Args:
        text (`str`): The text displayed on the button itself.
        parent (`QWidget`, default=None): This widgets parent widget.
    """

    process = None

    def __init__(self, text, parent=None):
        """Construct the CheckButton Widget."""
        super().__init__(text, parent=parent)
        self.widget = parent
        self.window = parent.window
        self.pressed.connect(self.submit)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(pushButtonSheet)

    def submit(self):
        tree = self.widget.treeWidget
        tree.clear()
        textEdit = self.widget.textEdit
        textEdit.clear()
        searchInput = self.widget.searchInput
        fileInput = self.widget.fileInput
        metafile = fileInput.text()
        content = searchInput.text()
        CheckerClass.register_callback(textEdit.callback)
        logging.debug("Registering Callback, setting root")
        piece_hasher(metafile, content, tree)
        # tree.start_thread(metafile, content)


class BrowseTorrents(QToolButton):
    """BrowseButton ToolButton for activating filebrowser.

    Subclass of QToolButton

    Args:
        parent (`widget`): Parent widget.
    """

    def __init__(self, parent=None):
        """Construct Toolbar Button for selecting .torrentfile to check."""
        super().__init__(parent=parent)
        self.setText("...")
        self.window = parent
        self.setStyleSheet(toolButtonSheet)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.inputWidget = None
        self.pressed.connect(self.browse)

    def browse(self, path=None):
        """Browse action performed when user presses button.

        Opens File/Folder Dialog.

        Returns:
            path (`str`): Path to file or folder to include in torrent.
        """
        caption = "Choose .torrent file."
        if not path:
            path = QFileDialog.getOpenFileName(
                parent=self, caption=caption, filter="*.torrent"
            )
        if not path:
            return
        if isinstance(path, Sequence):
            path = path[0]
        path = os.path.normpath(path)
        self.parent().fileInput.clear()
        self.parent().fileInput.setText(path)


class BrowseFolders(QToolButton):
    """Browse Folders ToolButton for activating filedialog.

    Args:
        parent (`QWidget`, default=None): Widget this widget is the child of.
    """

    def __init__(self, parent=None):
        """Construct a BrowseFolders Button Widget."""
        super().__init__(parent=parent)
        self.setText("...")
        self.window = parent
        self.setStyleSheet(toolButtonSheet)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pressed.connect(self.browse)

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
        if not path:
            return
        path = os.path.normpath(path)
        self.parent().searchInput.clear()
        self.parent().searchInput.setText(path)


class TreePieceItem(QTreeWidgetItem):
    def __init__(self, type=0, tree=None):
        super().__init__(type=type)
        policy = self.ChildIndicatorPolicy.DontShowIndicatorWhenChildless
        self.setChildIndicatorPolicy(policy)
        self.tree = tree
        self.progbar = None
        self.total = self.value = self.counted = 0

    def setProgressBar(self, progressBar, size):
        self.total = size
        self.progbar = progressBar
        self.progbar.setRange(0, size)

    def addValue(self, value):
        left = self.total - self.counted
        if left > value:
            self.progbar.addValue(value)
            self.value += value
            self.counted += value
            return 0
        self.progbar.addValue(left)
        self.counted += left
        self.value += left
        remainder = value - left
        return remainder

    def counted(self, value):
        left = self.total - self.counted
        if left < value:
            self.counted += left
            remainder = value - left
            return remainder
        self.counted += value
        return 0



    def __repr__(self):
        return f"<TreeItem: {self.val}>"


class Filler:
    def __init__(self, **kwargs):
        self.tree = kwargs["tree"]
        self.value = None
        self.expected = None

    def set_val(self, val, expected):
        self.expected = expected
        self.value = val

    def text(self):
        if self.expected:
            return self.expected


class ProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setRange(0, 100)

    def addValue(self, value):
        currentvalue = self.value()
        addedVal = currentvalue + value
        self.setValue(addedVal)


class TreeWidget(QTreeWidget):
    """Tree Widget for the `Check` tab.

    Displays percentages for matching files and their progress.

    Args:
        parent(`QWidget`, default=None)
    """

    valueUpdate = pyqtSignal([list])
    addPathChild = pyqtSignal([str, int])

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.window = parent.window
        self.setStyleSheet(treeSheet + headerSheet)
        self.setColumnCount(3)
        self.setIndentation(10)
        self.item = self.invisibleRootItem()
        self.item.setExpanded(True)
        header = self.header()
        header.setSectionResizeMode(0, header.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, header.ResizeMode.ResizeToContents)
        self.setHeaderHidden(True)
        self.itemWidgets = {}
        self.paths = []
        self.total = 0
        self.piece_length = None
        self.item_tree = {"widget": self.item}
        self.valueUpdate.connect(self.updateValue)
        self.addPathChild.connect(self.add_path_child)

    def updateValue(self, args):
        actual, expected, path, size = args
        widget = self.itemWidgets[path]["widget"]
        # print(actual, expected)
        if actual == expected:
            widget.add_piece(size)
            self.window.repaint()

    def clear(self):
        super().clear()
        self.item_tree = {"widget": self.invisibleRootItem()}
        self.itemWidgets = {}
        self.paths = []
        self.root = None

    def add_path_child(self, path, size):
        path = Path(path)
        partials = path.parts
        item, item_tree = None, self.item_tree
        for i, partial in enumerate(partials):
            if partial in item_tree:
                item_tree = item_tree[partial]
                continue
            parent = item_tree["widget"]
            item = TreePieceItem(type=0, tree=self)
            parent.addChild(item)
            parent.setExpanded(True)
            item_tree[partial] = {"widget": item}
            if i == len(partials) - 1:
                fileicon = QIcon("./assets/file.png")
                progressBar = ProgressBar()
                self.setItemWidget(item, 2, progressBar)
                item.setProgressBar(progressBar, size)
                self.itemWidgets[str(path)] = item
            else:
                fileicon = QIcon("./assets/folder.png")
            item.setIcon(0, fileicon)
            item.setText(1, partial)
            item_tree = item_tree[partial]
            self.window.repaint()
        self.paths.append(path)

    def remainder(self, path):
        widget = self.itemWidgets[path]["widget"]
        return widget.total - widget.length


def piece_hasher(metafile, content, tree):
    mapping = {}
    checker = CheckerClass(metafile, content)
    parent = os.path.dirname(content)
    pathlist = checker.paths
    for path in pathlist:
        relpath = path.lstrip(parent)
        length = checker.fileinfo[path]["length"]
        tree.addPathChild.emit(relpath, length)
    index, current = 0, None
    for actual, expected, path, size in checker.iter_hashes():
        print(mapping)
        if not current: current = path
        elif path != current:
            current = path
            index = pathlist.index(path)
        relpath = path.lstrip(parent)
        widget = tree.itemWidgets[relpath]
        if actual == expected:
            methodname = "addValue"
        else:
            methodname = "counted"
        method = widget.__getattribute__(methodname)
        remainder = method(size)
        mapping[path] = {"size": size, "remiander": remainder}
        while remainder > 0:
            index += 1
            nextpath = pathlist[index]
            current = nextpath
            rpath = nextpath.lstrip(parent)
            nwidget = tree.itemWidgets[rpath]
            size = remainder
            method = nwidget.__getattribute__(methodname)
            remainder = method(size)
            mapping[nextpath] = {"size": size, "remiander": remainder}


class LogTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.setBackgroundVisible(True)
        font = self.font()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setPointSize(8)
        self.setFont(font)
        self.setStyleSheet(logTextEditSheet)

    def clear_data(self):
        self.clear()

    def callback(self, msg):
        self.insertPlainText(msg)
        self.insertPlainText("\n")




class LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.setStyleSheet(lineEditSheet)


class Label(QLabel):
    """Label Identifier for Window Widgets.

    Subclass: QLabel
    """

    def __init__(self, text, parent=None):
        super().__init__(text, parent=parent)
        self.setStyleSheet(labelSheet)
        font = self.font()
        font.setBold(True)
        font.setPointSize(12)
        self.setFont(font)
