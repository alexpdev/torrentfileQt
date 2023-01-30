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
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (QHBoxLayout, QToolBar, QTreeView, QVBoxLayout,
                               QWidget)

from torrentfileQt.utils import (browse_folder, browse_torrent, get_icon,
                                 torrent_filter)


class BencodeEditWidget(QWidget):
    """
    Tab widget for the bencode editor.
    """

    def __init__(self, parent: QWidget = None):
        """
        Subclass of qwidget for the Bencode editor page.

        Parameters
        ----------
        parent : QWidget, optional
            parent widget, by default None
        """
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("bencodeTab")
        self.toolbar = QToolBar(parent=self)
        self.setAcceptDrops(True)
        self.file_action = QAction(get_icon("browse_file"), "Select File")
        self.folder_action = QAction(
            get_icon("browse_folder"), "Select Folder"
        )
        self.save_action = QAction(get_icon("save-as"), "Save Data")
        self.clear_action = QAction(get_icon("erase"), "Clear Data")
        self.remove_item_action = QAction(get_icon("trash"), "Remove Item")
        self.insert_item_action = QAction(get_icon("insert"), "Insert Item")
        self.treeview = BencodeView(self)
        self.toolbar.addActions((self.file_action, self.folder_action))
        self.toolbar.addSeparator()
        self.toolbar.addActions(
            [self.insert_item_action, self.remove_item_action]
        )
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
        item = self.treeview.model().getItem(current)
        row = item.childNumber()
        self.treeview.model().removeRow(row, current.parent())

    def insert_view_item(self):
        """Insert the currently selected row."""
        current = self.treeview.selectionModel().currentIndex()
        parent = self.treeview.model().parent(current)
        item = self.treeview.model().getItem(current)
        row = item.childNumber()
        self.treeview.model().insertRow(row, parent)

    def save_changes(self):
        """
        Trigger when Save action is clicked.

        Traverses contents of bencode editor and saving their contents if any
        entry has been marked as edited.
        """
        rows = self.treeview.rowCount()
        for i in range(rows):
            item = self.treeview.item(i, 0)
            if item.edited():
                self.treeview.save_item(item)

    def clear_contents(self):
        """Wipe the tree of all of it's contents."""
        self.treeview.clear()

    def load_file(self, paths: list = None):
        """
        Load the a file or files from the Files_action.

        Parameters
        ----------
        paths : list, optional
            torrent file paths, by default None
        """
        paths = browse_torrent(self, paths)
        self.load_thread(paths)

    def load_thread(self, paths: list):
        """
        Load the thread to process the bencode parsing.

        Parameters
        ----------
        paths : list
            list of path strings
        """
        paths = torrent_filter(paths)
        self.thread = Thread(paths, self.treeview)
        self.thread.start()
        self.thread.finished.connect(self.thread.deleteLater)

    def load_folder(self, path: str = None):
        """
        Load all of the files contained in given folder path.

        Parameters
        ----------
        path : str, optional
            folder path, by default None
        """
        if not path:
            path = browse_folder(self, path)  # pragma: nocover
        paths = [os.path.join(path, i) for i in os.listdir(path)]
        self.load_thread(paths)

    def dragEnterEvent(self, event):
        """Drag enter event for widget."""
        if event.mimeData().hasUrls:
            event.accept()
            return True
        return event.ignore()

    def dragMoveEvent(self, event):
        """Drag Move Event for widgit."""
        if event.mimeData().hasUrls:
            event.accept()
            return True
        return event.ignore()

    def dropEvent(self, event) -> bool:
        """Drag drop event for widgit."""
        urls = event.mimeData().urls()
        path = urls[0].toLocalFile()
        if os.path.exists(path):
            self.load_thread([path])
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
        self.setHeaderHidden(True)
        self.addChildInfo.connect(self.addItem)

    def clear(self):
        """Clear the contents of the widget."""
        rows = self.model().rowCount()
        self.model().removeRows(0, rows)

    def addItem(self, item: "Item"):
        """
        Add a row to the tree view with the torrent information from the path.

        Parameters
        ----------
        item : Item
            the item
        """
        self.model().addItem(item)

    def rowCount(self) -> int:
        """Return number of rows in the tree view."""
        return self.model().rowCount()

    def item(self, row: int, column: int):
        """Return the item associated with the given index values."""
        return self.model().getItem(self.model().index(row, column))

    def save_item(self, item: dict):
        """
        Save edited data from the bencode editor.

        Parameters
        ----------
        item : dict
            torrent file metadata
        """
        if item.edited():
            path = item.itemData
            self.model().to_bencode(item)
            pyben.dump(item.data(), path)


class Item:
    """A Bencode item corresponding to a line in QTreeView."""

    model = None

    def __init__(
        self, parent: "Item" = None, value: Any = None, data: Any = None
    ):
        """
        Return a Item instance for the bencode tree view editor.

        Parameters
        ----------
        parent : Item, optional
            parent, by default None
        value : Any, optional
            displayed value, by default None
        data : Any, optional
            data for this item and children, by default None
        """
        self.parentItem = parent
        self.itemData = value
        self.childItems = []
        self.columns = 1
        self._data = data
        self._index = None
        self._icon = None
        self._isroot = False
        self._edited = False
        self.edit = None

    def parent(self) -> "Item":
        """Return parent item."""
        return self.parentItem

    def isIndex(self) -> bool:
        """Return index state."""
        return self._index is not None  # pragma: nocover

    def setIndex(self, index: int):
        """Set index state."""
        self._index = index

    def isRoot(self, state: bool = None):
        """Set the root state."""
        if state is not None:
            self._isroot = state
        return self._isroot

    def icon(self) -> QIcon:
        """Return this item's icon."""
        return self._icon

    def setIcon(self, icon):
        """Set this item's display icon."""
        self._icon = icon

    def text(self):
        """Return the data as a string."""
        return str(self.itemData)

    def edited(self, state: bool = None, other: Any = None):
        """Set the edited state."""
        if state is not None:
            if other is not None:
                self.edit = other
            if not self._isroot:
                self.parentItem.edited(state)
            self._edited = state
        return self._edited

    def child(self, row: int) -> "Item":
        """Return the child of the current item from the given row."""
        return self.childItems[row]

    def hasChildren(self) -> bool:
        """Return if the item has children."""
        return self.childCount() != 0

    def childCount(self):
        """Return the number of children."""
        return len(self.childItems)

    def childNumber(self):
        """Return the row number."""
        if self.parentItem is not None:
            return self.parentItem.childItems.index(self)
        return 0

    def columnCount(self):
        """Return number of columns."""
        return self.columns  # pragma: nocover

    def data(self):
        """Return the data for the specified column."""
        return self._data

    def insertChildren(
        self, position: int, count: int
    ) -> bool:  # pragma: nocover
        """
        Insert child items into list of children.

        Parameters
        ----------
        position : int
            start position
        count : int
            number of children

        Returns
        -------
        bool
            success state
        """
        if position >= 0 and position + count <= len(self.childItems):
            if not self.hasChildren() or self.isIndex():
                return False
            for _ in range(count):
                item = Item(parent=self, value=None, data=None)
                self.childItems.insert(position, item)
            return True
        return False

    def removeChildren(self, position: int, count: int) -> bool:
        """
        Remove child items from list of children.

        Parameters
        ----------
        position : int
            start position
        count : int
            number of children

        Returns
        -------
        bool
            success state
        """
        if position >= 0 and position + count <= len(self.childItems):
            for _ in range(count):
                self.childItems.pop(position)
            return True
        return False  # pragma: nocover

    def addChild(self, child: "Item"):
        """Add child to list of children."""
        self.childItems.append(child)

    def setData(self, value: Any) -> bool:
        """
        Edit the column's contents to reflect new value.

        Parameters
        ----------
        value : Any
            value

        Returns
        -------
        bool
            success state
        """
        if not self.hasChildren():
            old = self.itemData
            self.itemData = value
            self.edited(True, old)
            return True
        return False  # pragma: nocover

    def index(self):
        """Get the index for the item."""
        row = self.childNumber()
        if self.isRoot():
            index = self.model.index(row, 0, QModelIndex())
            return index
        return self.model.index(row, 0, self.parent().index())

    @classmethod
    def set_model(cls, model: QAbstractItemModel):
        """Set the model for the item class."""
        cls.model = model

    @classmethod
    def buildItem(cls, meta: Any, root: "Item") -> "Item":
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
            item = cls(value=meta, data=meta, parent=root)
            item.setIcon(cls.model.data_icon)
            root.addChild(item)
            return item
        if isinstance(meta, (list, tuple, set)):
            for i, val in enumerate(meta):
                item = cls(value=i, parent=root, data=val)
                item.setIcon(cls.model.list_icon)
                item.setIndex(i)
                root.addChild(item)
                cls.buildItem(val, item)
        elif isinstance(meta, dict):
            for key, val in meta.items():
                item = cls(value=key, data=val, parent=root)
                item.setIcon(cls.model.brackets_icon)
                root.addChild(item)
                cls.buildItem(val, item)
        return root


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
        self.columns = 1
        self.rootItem = Item()
        self.data_icon = QIcon(get_icon("data"))
        self.list_icon = QIcon(get_icon("list"))
        self.torrent_icon = QIcon(get_icon("torrentfile"))
        self.brackets_icon = QIcon(get_icon("brackets"))
        Item.set_model(self)

    def columnCount(self, _=QModelIndex()):
        """
        Override from QAbstractItemModel.

        Return column number. For the model, it always return 2 columns
        """
        return self.columns

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        """
        Override from QAbstractItemModel.

        Return data from a json item according index and role
        """
        if index and index.isValid():
            item = self.getItem(index)
            if role == Qt.DisplayRole:
                return item.text()
            if role == Qt.EditRole:
                if not item.hasChildren():  # pragma: nocover
                    return item.text()
            elif role == Qt.DecorationRole:
                return item.icon()
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """
        Override from QAbstractItemModel.

        Return flags of index
        """
        flags = super().flags(index)
        if index and index.isValid():
            item = self.getItem(index)
            if not item.hasChildren():
                flags |= Qt.ItemIsEditable
        return flags

    def getItem(self, index: QModelIndex) -> Item:
        """
        Get the item associated with the model index.

        Parameters
        ----------
        index : QModelIndex
            model index

        Returns
        -------
        Item
            Tree Item
        """
        item = self.rootItem
        if index.isValid():
            item = index.internalPointer()
        return item

    def index(
        self, row: int, column: int = 0, parent: QModelIndex = QModelIndex()
    ):
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
        if self.hasIndex(row, column, parent):
            if not parent.isValid():
                parentItem = self.rootItem
            else:
                parentItem = self.getItem(parent)
            childItem = parentItem.child(row)
            if childItem:
                return self.createIndex(row, column, childItem)
        return QModelIndex()

    def insertColumns(
        self, position: int, columns: int = 0, parent=QModelIndex()
    ):  # pragma: nocover
        """Insert a column into tree."""
        self.beginInsertColumns(parent, position, position + columns - 1)
        success = self.rootItem.insertColumns(position, columns)
        self.endInsertColumns()
        return success

    def removeRow(self, row, parentIndex):  # pragma: nocover
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
        parentItem = self.getItem(index)
        self.beginRemoveRows(index, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()
        return success

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
        return self.insertRows(position, 1, parent)  # pragma: nocover

    def insertRows(
        self, position: int, rows: int, parent=QModelIndex()
    ) -> bool:  # pragma: nocover
        """
        Add item row and tree to the model and view.

        Parameters
        ----------
        position : int
            location
        rows : int
            number of rows
        parent : QModelIndex, optional
            parent index, by default QModelIndex()

        Returns
        -------
        bool
            success state
        """
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows)
        self.endInsertRows()
        return success

    def parent(self, index: QModelIndex) -> QModelIndex:
        """
        Override from QAbstractItemModel.

        Return parent index of index
        """
        if index and index.isValid():
            childItem = self.getItem(index)
            parentItem = childItem.parent()
            if parentItem and parentItem != self.rootItem:
                return self.createIndex(
                    parentItem.childNumber(), 0, parentItem
                )
        return QModelIndex()  # pragma: nocover

    def removeColumns(
        self, position: int, columns: int = 0, index=QModelIndex()
    ):  # pragma: nocover
        """
        Remove rows from the model and view.

        Parameters
        ----------
        position : int
            start index
        columns : int
            end index
        index : QModelIndex, optional
            item index, by default QModelIndex()
        """
        parentItem = self.getItem(index)
        self.beginRemoveRows(index, position, position + columns - 1)
        success = parentItem.removeChildren(position, columns)
        self.endRemoveRows()
        if self.rootItem.columnCount() == 0:
            self.removeRows(0, self.rowCount())
        return success

    def rowCount(self, parent=QModelIndex()):
        """
        Override from QAbstractItemModel.

        Return row count from parent index
        """
        parentItem = self.getItem(parent)
        return parentItem.childCount()

    def setData(
        self,
        index: QModelIndex,
        value: Any,
        role: Qt.ItemDataRole = Qt.EditRole,
    ):
        """Override from QAbstractItemModel.

        Set json item according index and role

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
            item = self.getItem(index)
            if not item.hasChildren():
                result = item.setData(value)
                if result:
                    self.dataChanged.emit(index, index)
                    return True
        return False  # pragma: nocover

    def addItem(self, item: Item):
        """
        Add item to the view.

        Parameters
        ----------
        item : Item
            added item
        """
        rowCount = self.rowCount()
        self.beginInsertRows(QModelIndex(), rowCount, rowCount)
        item.setIcon(self.torrent_icon)
        item.isRoot(True)
        self.rootItem.addChild(item)
        self.endInsertRows()

    def row(self, index: int) -> Item:  # pragma: nocover
        """Return the row item."""
        return self.rootItem.child(index)

    def to_bencode(self, item: Item) -> Any:
        """
        Convert Item Node Tree to bencoded data.

        Parameters
        ----------
        item : Item
            root item of tree.

        Returns
        -------
        Any
            the edited data.
        """
        if not item.hasChildren():
            return item.itemData
        for i in range(item.childCount()):
            child = item.child(i)
            change = self.to_bencode(child)
            if change is not None:
                data = item.parent().data()
                if data[item.itemData] != change:
                    data[item.itemData] = change
        return None


class Thread(QThread):
    """Thread for processing torrent files prior to loading."""

    def __init__(self, lst: list, tree: QAbstractItemModel):
        """Process list of torrent files and send data to model."""
        super().__init__()
        self.lst = lst
        self.tree = tree

    def run(self):
        """Iterate through list and emit a signal with data."""
        for tfile in self.lst:  # pragma: nocover
            meta = pyben.load(tfile)
            root = Item(data=meta, value=tfile)
            Item.buildItem(meta, root)
            self.tree.addChildInfo.emit(root)
