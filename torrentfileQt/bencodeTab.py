#! /usr/bin/python3
# -_- coding: utf-8 -_-

##############################################################################
# Copyright 2020 AlexPDev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# <http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################
"""Bencode editor module."""

import os
from typing import Any

import pyben
from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt, QThread, Signal
from PySide6.QtGui import QAction, QIcon, QMouseEvent
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QToolBar, QTreeView,
                               QVBoxLayout, QWidget)

from torrentfileQt.utils import (browse_folder, browse_torrent, get_icon,
                                 torrent_filter)


class BencodeEditWidget(QWidget):
    """Tab widget for the bencode editor."""

    def __init__(self, parent: QWidget = None):
        """
        Subclass of qwidget for the Bencode editor page.

        Parameters
        ----------
        parent : QWidget, optional
            parent widget, by default None
        """
        super().__init__(parent=parent)
        self.centralWidget = QWidget(self)
        self.centralLayout = QVBoxLayout(self)
        mainLabel = QLabel("Bencode Editor")
        mainLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLabel.setObjectName("bencodeMainLabel")
        self.data_icon = QIcon(get_icon("data"))
        self.list_icon = QIcon(get_icon("list"))
        self.torrent_icon = QIcon(get_icon("torrentfile"))
        self.brackets_icon = QIcon(get_icon("brackets"))
        self.centralLayout.addWidget(mainLabel)
        self.centralLayout.addWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("bencodeTab")
        self.toolbar = QToolBar(parent=self)
        self.setAcceptDrops(True)
        self.file_action = QAction(get_icon("browse_file"), "Select File")
        self.folder_action = QAction(get_icon("browse_folder"),
                                     "Select Folder")
        self.save_action = QAction(get_icon("save-as"), "Save Data")
        self.clear_action = QAction(get_icon("erase"), "Clear Data")
        self.remove_item_action = QAction(get_icon("trash"), "Remove Item")
        self.insert_item_action = QAction(get_icon("insert"), "Insert Item")
        self.treeview = BencodeView(self)
        self.toolbar.addActions((self.file_action, self.folder_action))
        self.toolbar.addSeparator()
        self.toolbar.addActions(
            [self.insert_item_action, self.remove_item_action])
        self.toolbar.addSeparator()
        self.toolbar.addActions((self.save_action, self.clear_action))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolbar_layout = QHBoxLayout()
        self.toolbar_layout.addStretch(1)
        self.toolbar_layout.addWidget(self.toolbar)
        self.toolbar_layout.addStretch(1)
        self.layout.addLayout(self.toolbar_layout)
        self.layout.addWidget(self.treeview)
        self.file_action.triggered.connect(self.load_file)
        self.folder_action.triggered.connect(self.load_folder)
        self.save_action.triggered.connect(self.save_changes)
        self.clear_action.triggered.connect(self.clear_contents)
        self.remove_item_action.triggered.connect(self.remove_view_item)
        self.insert_item_action.triggered.connect(self.insert_view_item)

    def remove_view_item(self):
        """Remove the currently selected row."""
        current = self.treeview.selectionModel().currentIndex()
        item = self.treeview.model().itemFromIndex(current)
        self.treeview.removeItem(item)

    def insert_view_item(self):
        """Insert the currently selected row."""
        current = self.treeview.selectionModel().currentIndex()
        parent = self.treeview.model().parent(current)
        item = self.treeview.model().itemFromIndex(current)
        row = item.row()
        self.treeview.model().insertRow(row, parent)

    def save_changes(self):
        """
        Trigger when Save action is clicked.

        Traverses contents of bencode editor and saving their contents if any
        entry has been marked as edited.
        """
        for row in range(self.treeview.rowCount()):
            torrent = self.treeview.item(row, 0)
            path = torrent.data(0)
            meta = self.get_children(torrent)
            pyben.dump(path, meta)

    def get_children(self, item):
        """Get torrent metdata."""
        if item.dataType() == dict:
            meta = {}
            for child in item.children():
                key = child.data(0)
                if child.columnCount() > 1:
                    value = child.data(1)
                else:
                    value = self.get_children(child)
                meta.update({key: value})
        else:
            meta = []
            for child in item.children():
                if child.columnCount() > 1:
                    value = child.data(1)
                else:
                    value = self.get_children(child)
                meta.append(value)
        return meta

    def clear_contents(self) -> bool:
        """Wipe the tree of all of it's contents."""
        return self.treeview.clear()

    def load_file(self):
        """
        Load the a file or files from the Files_action.

        Parameters
        ----------
        paths : list, optional
            torrent file paths, by default None
        """
        paths = browse_torrent(self)
        self.load_thread([paths])

    def load_thread(self, paths: list):
        """
        Load the thread to process the bencode parsing.

        Parameters
        ----------
        paths : list
            list of path strings
        """
        paths = torrent_filter(paths)
        self.thread = Thread(paths, self)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.itemReady.connect(self.treeview.addItem)
        self.thread.start()

    def load_folder(self):
        """
        Load all of the files contained in given folder path.

        Parameters
        ----------
        path : str, optional
            folder path, by default None
        """
        path = browse_folder(self)
        paths = [os.path.join(path, i) for i in os.listdir(path)]
        self.load_thread(paths)

    def dragEnterEvent(self, drag_event: QMouseEvent) -> bool:
        """Drag enter event for bencodeWidget."""
        if drag_event.mimeData().hasUrls:
            drag_event.accept()
            return True
        return drag_event.ignore()

    def dragMoveEvent(self, drag_event: QMouseEvent) -> bool:
        """Drag Move Event for bencodeWidgit."""
        if drag_event.mimeData().hasUrls:
            drag_event.accept()
            return True
        return drag_event.ignore()

    def dropEvent(self, drop_event: QMouseEvent) -> bool:
        """Drag drop event for bencodeWidgit."""
        path_urls = drop_event.mimeData().urls()
        fspath = path_urls[0].toLocalFile()
        if os.path.exists(fspath):
            self.load_thread([fspath])
            return True
        return False


class BencodeView(QTreeView):
    """
    TreeView subclass for holding the bencode data for each processed file.
    """

    addChildInfo = Signal(object)

    def __init__(self, parent: QWidget = None):
        """
        Subclass of QTreeView that shows structured output for torrent files.

        Parameters
        ----------
        parent : QWidget, optional
            parent widget, by default None
        """
        super().__init__(parent=parent)
        self.setProperty("InfoTree", "true")
        self.bencode_model = BencodeModel()
        self.setModel(self.bencode_model)
        self.setIcons(parent)

    def removeItem(self, item: object):
        """
        Remove item from model.

        Parameters
        ----------
        item : object
            item object
        """
        self.model().removeItem(item)

    def setIcons(self, parent):
        """Set icons for tree items."""
        self.bencode_model.torrent_icon = parent.torrent_icon
        self.bencode_model.data_icon = parent.data_icon
        self.bencode_model.brackets_icon = parent.brackets_icon
        self.bencode_model.list_icon = parent.list_icon

    def clear(self):
        """Clear the contents of the widget."""
        rows = self.model().rowCount()
        self.model().removeRows(0, rows)
        return True

    def addItem(self, item: "Item"):
        """
        Add a row to the tree view with the torrent information from the path.

        Parameters
        ----------
        item : Item
            the item
        """
        self.model().addItem(item)
        self.resizeColumnToContents(0)

    def rowCount(self) -> int:
        """Return number of rows in the tree view."""
        return self.model().rowCount()

    def item(self, row: int, column: int):
        """Return the item associated with the given index values."""
        return self.model().itemFromIndex(self.model().index(row, column))


class Item:
    """A Bencode item corresponding to a line in QTreeView."""

    model = None

    def __init__(self, parent: "Item" = None, icon: QIcon = None):
        """
        Return a Item instance for the bencode tree view editor.

        Parameters
        ----------
        parent : Item, optional
            parent, by default None
        icon : QIcon, optional
            icon, by default None
        """
        self._data = []
        self._icon = icon
        self._parent = parent
        self._childItems = []
        self._dataType = None
        if parent is not None:
            parent.addChild(self)

    def parent(self) -> "Item":
        """Return parent item."""
        return self._parent

    def setParent(self, parent: "Item"):
        """Set the item's parent."""
        self._parent = parent

    def icon(self) -> QIcon:
        """Return the item's icon."""
        return self._icon

    def setIcon(self, icon: QIcon):
        """Set the item's icon."""
        self._icon = icon

    def child(self, row: int) -> "Item":
        """Return the child of the current item from the given row."""
        return self._childItems[row]

    def childCount(self) -> int:
        """Return the number of children."""
        return len(self._childItems)

    def columnCount(self) -> int:
        """Return number of columns."""
        return len(self._data)

    def data(self, column: int = 0) -> Any:
        """Return the data for the specified column."""
        if column >= len(self._data):
            return None
        return self._data[column]

    def setDataType(self, dataType: Any):
        """Set item's data type."""
        self._dataType = dataType

    def dataType(self):
        """Set data type for item."""
        return self._dataType

    def setData(self, data: Any, column: int = 0):
        """Set the data for column."""
        if column >= len(self._data):
            self._data.append(data)
        else:
            self._data[column] = data
        return True

    def row(self) -> int:
        """Return the index row of the item."""
        return 0 if not self.parent() else self.parent().children().index(self)

    def children(self):
        """Return Children."""
        return self._childItems

    def addChild(self, child: "Item"):
        """Append item to children list."""
        self.children().append(child)

    @classmethod
    def set_model(cls, model: QAbstractItemModel):
        """Set the model for the item class."""
        cls.model = model


class BencodeModel(QAbstractItemModel):
    """An editable model of Bencode data."""

    def __init__(self, parent: QWidget = None):
        """
        Subclass for QAbstactItemModel for Bencode Editor.

        Parameters
        ----------
        parent : QWidget, optional
            parent widget, by default None
        """
        super().__init__(parent=parent)
        self.rootItem = Item()
        self.header_data = ["Field", "Value"]
        Item.set_model(self)

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: Qt.ItemDataRole):
        """
        Return header data.

        Parameters
        ----------
        section : int
            header section
        orientation : Qt.Orientation
            header orientation
        role : Qt.ItemDataRole
            header section role

        Returns
        -------
        Any
            item for role and section in header
        """
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section <= len(self.header_data):
                return self.header_data[section]
        return super().headerData(section, orientation, role)

    def columnCount(self, _=QModelIndex()):
        """Return column number. For the model, it always return 2 columns."""
        return len(self.header_data)

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        """Return data from a bencode item according index and role."""
        if index.isValid():
            column = index.column()
            item = self.itemFromIndex(index)
            if role in [Qt.DisplayRole, Qt.EditRole]:
                data = item.data(column)
                if not data:
                    return data
                return str(data)
            if role == Qt.DecorationRole and column == 0:
                return item.icon()
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """
        Override from QAbstractItemModel.
        """
        flags = super().flags(index)
        flags |= Qt.ItemIsEditable
        return flags

    def index(self, row: int, column: int,
              parent: QModelIndex = QModelIndex()):
        """
        Get the index for the given row and column of the parent index.

        Parameters
        ----------
        row : int
            row number
        column : int, optional
            column number, by default 0
        parent : QModelIndex, optional
            parent index, by default QModelIndex()

        Returns
        -------
        QModelIndex
            The item's index
        """
        if not self.hasIndex(row, column, parent):
            return QModelIndex()  # pragma: nocover
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        child = parentItem.child(row)
        if child:
            return self.createIndex(row, column, child)
        return QModelIndex()  # pragma: nocover

    def removeRow(self, row, parentIndex):
        """Remove row from treeview."""
        return self.removeRows(row, 1, parentIndex)

    def removeRows(self, position: int, rows: int, index=QModelIndex()):
        """
        Remove rows from the model and view.

        Parameters
        ----------
        position : int
            start index
        rows : int
            end index
        index : QModelIndex, optional
            item index, by default QModelIndex()

        Returns
        -------
        bool
            success state
        """
        if index and index.isValid():
            item = index.internalPointer()
        else:
            item = self.rootItem
        if item.childCount() < position + rows:
            return False
        self.beginRemoveRows(index, position, position + rows - 1)
        start = position + rows - 1
        while start >= position:
            del item.children()[start]
            start -= 1
        self.endRemoveRows()
        return True

    def insertRow(self, position: int, parent=QModelIndex()) -> bool:
        """
        Insert a single row into the tree.

        Parameters
        ----------
        position : int
            location to insert the row.
        parent : QModelIndex, optional
            parent index, by default QModelIndex()

        Returns
        -------
        bool
            success state
        """
        if parent.isValid():
            parentItem = parent.internalPointer()
        else:
            parentItem = self.rootItem
        if position > parentItem.childCount():
            return False  # pragma: nocover
        self.beginInsertRows(parent, position, position)
        item = Item()
        item.setParent(parentItem)
        parentItem.children().insert(position, item)
        self.endInsertRows()
        return True

    def parent(self, index: QModelIndex) -> QModelIndex:
        """Override from QAbstractItemModel."""
        if index.isValid():
            childItem = index.internalPointer()
            parentItem = childItem.parent()
            if parentItem and parentItem != self.rootItem:
                return self.createIndex(parentItem.row(), 0, parentItem)
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        """Return row count from parent index."""
        if parent.isValid():
            parentItem = parent.internalPointer()
        else:
            parentItem = self.rootItem
        return parentItem.childCount()

    def setData(
        self,
        index: QModelIndex,
        value: Any,
        role: Qt.ItemDataRole = Qt.EditRole,
    ):
        """Set json item according index and role.

        Parameters
        ----------
        index : QModelIndex
            index
        value : Any
            value
        role : Qt.ItemDataRole
            role
        """
        if role == Qt.EditRole:
            column = index.column()
            if index.isValid():
                item = index.internalPointer()
            result = item.setData(value, column)
            if result:
                self.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
                return True
        return False  # pragma: nocover

    def itemFromIndex(self, index: QModelIndex) -> Item:
        """Convert and item to it's index."""
        if index.isValid():
            return index.internalPointer()
        return self.rootItem

    def addItem(self, item):
        """Add item to root item."""
        row_num = self.rowCount()
        self.beginInsertRows(QModelIndex(), row_num, row_num)
        self.rootItem.children().append(item)
        self.endInsertRows()

    def removeItem(self, item):
        """Remove item from tree view."""
        row = item.row()
        index = self.createIndex(row, 0, item)
        self.removeRow(row, self.parent(index))


class Thread(QThread):
    """Thread for processing torrent files prior to loading."""

    itemReady = Signal(Item)

    def __init__(self, lst: list, parent: QWidget):
        """Process list of torrent files and send data to model."""
        super().__init__()
        self.lst = lst
        self.parent = parent
        self.dict_icon = self.parent.brackets_icon
        self.list_icon = self.parent.list_icon
        self.data_icon = self.parent.data_icon
        self.torrent_icon = self.parent.torrent_icon

    def buildItem(self, meta: Any, root: "Item") -> "Item":
        """
        Build the bencode value tree.

        Parameters
        ----------
        meta : Any
            data
        root : Item
            parent Item

        Returns
        -------
        Item
            Bencode Tree Nodes
        """
        if isinstance(meta, (int, float, str, bytes)):
            root.setData(meta, 1)
        if isinstance(meta, (list, tuple, set)):
            for i, val in enumerate(meta):
                item = Item(parent=root, icon=self.list_icon)
                item.setData(i, 0)
                root.setDataType(list)
                self.buildItem(val, item)
        elif isinstance(meta, dict):
            for key, val in meta.items():
                item = Item(parent=root, icon=self.dict_icon)
                item.setData(key, 0)
                root.setDataType(dict)
                self.buildItem(val, item)

    def run(self):
        """Iterate through list and emit a signal with data."""
        for tfile in self.lst:
            meta = pyben.load(tfile)
            root = Item(icon=self.torrent_icon)
            root.setData(tfile, 0)
            root.setDataType("torrent")
            self.buildItem(meta, root)
            self.itemReady.emit(root)
