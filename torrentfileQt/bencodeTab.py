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
"""Bencode editor module."""

import os
from typing import Any

import pyben
from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt, QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QTreeView,
                               QVBoxLayout, QWidget)

from torrentfileQt.utils import browse_folder, browse_torrent, get_icon


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
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.file_button = QPushButton("Select File", self)
        self.file_button.setIcon(QIcon(get_icon("browse_file")))
        self.folder_button = QPushButton("Select Folder", self)
        self.folder_button.setIcon(QIcon(get_icon("browse_folder")))
        self.save_button = QPushButton("Save Data", self)
        self.save_button.setIcon(QIcon(get_icon("save-as")))
        self.clear_button = QPushButton("Clear Contents", self)
        self.clear_button.setIcon(QIcon(get_icon("erase")))
        self.hlayout1 = QHBoxLayout()
        self.hlayout1.addWidget(self.file_button)
        self.hlayout1.addWidget(self.folder_button)
        self.hlayout1.addWidget(self.save_button)
        self.hlayout1.addWidget(self.clear_button)
        self.layout.addLayout(self.hlayout1)
        self.treeview = BencodeView(self)
        self.layout.addWidget(self.treeview)
        self.file_button.clicked.connect(self.load_file)
        self.folder_button.clicked.connect(self.load_folder)
        self.save_button.clicked.connect(self.save_changes)
        self.clear_button.clicked.connect(self.clear_contents)

    def save_changes(self):
        """
        Trigger when Save button is clicked.

        Traverses contents of bencode editor and saving their contents if any
        entry has been marked as edited.
        """
        rows = self.treeview.rowCount()
        for i in range(rows):
            item = self.treeview.item(i, 0)
            if item.is_edited():
                self.treeview.save_item(item)

    def clear_contents(self):
        """Wipe the tree of all of it's contents."""
        self.treeview.clear()

    def torrent_filter(self, paths: tuple) -> list:
        """
        Filter non torrent files from the given tuple of paths.

        Parameters
        ----------
        paths : tuple
            path strings

        Returns
        -------
        list
            torrent file paths
        """
        torrents = []
        for path in paths:
            if os.path.isfile(path) and path.endswith(".torrent"):
                torrents.append(path)
        return torrents

    def load_file(self, paths: list = None):
        """
        Load the a file or files from the Files_button.

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
        paths = self.torrent_filter(paths)
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
            path = browse_folder(self, path)
        paths = [os.path.join(path, i) for i in os.listdir(path)]
        self.load_thread(paths)


class BencodeView(QTreeView):
    """
    TreeView subclass for holding the bencode data for each processed file.
    """

    addChildInfo = Signal(str, dict)

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
        self.addChildInfo.connect(self.add_data)
        self.data_items = {}

    def clear(self):
        """Clear the contents of the widget."""
        rows = self.model().rowCount()
        self.model().removeRows(0, rows)

    def add_data(self, path: str, meta: dict):
        """
        Add a row to the tree view with the torrent information from the path.

        Parameters
        ----------
        path : str
            torrent file path
        meta : dict
            torrent metadata
        """
        self.data_items[path] = meta
        self.bencode_model.add_row(path, meta)

    def rowCount(self) -> int:
        """Return number of rows in the tree view."""
        return self.model().rowCount()

    def item(self, row: int, column: int):
        """Return the item associated with the given index values."""
        return self.model().index(row, column).internalPointer()

    def save_item(self, item: dict):  # pragma: nocover
        """
        Save edited data from the bencode editor.

        Parameters
        ----------
        item : dict
            torrent file metadata
        """
        path = item.key
        self.model().to_bencode(item)
        pyben.dump(item.data, path)

    def index_from_item(self, item: "Item") -> QModelIndex:
        """Get the index from the given item."""
        if not item._root:
            row = item.row()
            return self.model().createIndex(row, 0, item)
        return QModelIndex()


class Item:
    """A Bencode item corresponding to a line in QTreeView."""

    model = None

    def __init__(
        self,
        parent: "Item" = None,
        key: Any = None,
        root: bool = False,
        index: int = None,
        data: Any = None,
        icon: QIcon = None,
    ):
        """
        Return a Item instance for the bencode tree view editor.

        Parameters
        ----------
        parent : Item, optional
            parent, by default None
        key : Any, optional
            displayed value, by default None
        root : bool, optional
            True if this is the root item, by default False
        index : int, optional
            position in a list, by default None
        data : Any, optional
            data for this item and children, by default None
        icon : QIcon, optional
            icon, by default None
        """
        self._parent = parent
        self._key = key
        self._root = root
        self._data = data
        self._children = []
        self._index = index
        self._icon = icon
        self._edited = False
        self._edit = None

    def set_edited(self):
        """Set edit state to True."""
        self._edited = True
        if self._parent is not None:
            self._parent.set_edited()

    def is_edited(self) -> bool:
        """Return edit state."""
        return self._edited

    def setIcon(self, icon: QIcon):
        """Set the item icon."""
        self._icon = icon

    @property
    def data(self) -> Any:
        """Return the items data."""
        return self._data

    @data.setter
    def data(self, other: Any):
        """Set the data property to other."""
        self._data = other

    def icon(self) -> QIcon:
        """Return the icon."""
        if not self._icon:
            return self.model.torrent_icon
        return self._icon

    def add_child(self, item: "Item"):
        """Add item as a child."""
        self._children.append(item)

    def child(self, row: int) -> "Item":
        """Return the child of the current item from the given row."""
        return self._children[row]

    def parent(self) -> "Item":
        """Return the parent of the current item."""
        return self._parent

    def count(self) -> int:
        """Return the number of children of the current item."""
        return len(self._children)

    def row(self) -> int:
        """Return the row where the current item occupies in the parent."""
        return self._parent._children.index(self) if self._parent else 0

    def text(self) -> str:
        """Return the string representation of the item."""
        return str(self._key)

    def has_children(self) -> bool:
        """Return if the item has children."""
        return len(self._children) != 0

    def index(self) -> int:
        """Return the index value if there is one."""
        return self._index

    @property
    def key(self) -> str:
        """Return the key name."""
        return self._key

    @key.setter
    def key(self, key: str):
        """Set key name of the current item."""
        self._key = key

    def remove_child(self, row):
        """Remove child from list of children."""
        value = self._children[row]
        self._children.remove(value)
        return True

    @classmethod
    def set_model(cls, model: QAbstractItemModel):
        """Set the model for the item class."""
        cls.model = model

    @classmethod
    def build(cls, meta: Any, root: "Item") -> "Item":
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
            item = cls(key=meta,
                       icon=cls.model.data_icon,
                       data=meta,
                       parent=root)
            root.add_child(item)
            return item
        if isinstance(meta, (list, tuple, set)):
            for i, val in enumerate(meta):
                item = cls(
                    index=i,
                    key=i,
                    parent=root,
                    icon=cls.model.list_icon,
                    data=val,
                )
                root.add_child(item)
                cls.build(val, item)
        elif isinstance(meta, dict):
            for key, val in meta.items():
                item = cls(
                    key=key,
                    data=val,
                    icon=cls.model.brackets_icon,
                    parent=root,
                )
                root.add_child(item)
                cls.build(val, item)
        return root


class BencodeModel(QAbstractItemModel):
    """An editable model of Bencode data."""

    itemValueChanged = Signal(object, object, QModelIndex)

    def __init__(self, parent: QWidget = None):
        """
        Subclass for QAbstactItemModel for Bencode Editor.

        Parameters
        ----------
        parent : QWidget, optional
            parent widget, by default None
        """
        super().__init__(parent=parent)
        self._rootItem = Item()
        self._rootItem.value_type = list
        self.data_icon = QIcon(get_icon("data"))
        self.list_icon = QIcon(get_icon("list"))
        self.torrent_icon = QIcon(get_icon("torrentfile"))
        self.brackets_icon = QIcon(get_icon("brackets"))
        self.itemValueChanged.connect(self.setEdited)
        Item.set_model(self)

    def removeRow(self, row, parentIndex):
        """Remove row from treeview."""
        return self.removeRows(row, 1, parentIndex)

    def removeRows(self, row: int, count: int, index=QModelIndex()):
        """
        Remove rows from the model and view.

        Parameters
        ----------
        start : int
            start index
        stop : int
            end index
        index : QModelIndex, optional
            item index, by default QModelIndex()
        """
        if index and index.isValid():
            self.beginRemoveRows(index, row, count)
            root = index.internalPointer()
            root.removeChild(row)
            self.endRemoveRows()
            return True
        return False

    def setEdited(self, old: Any, new: Any, index: QModelIndex):
        """
        Set the edit state for an item.

        Parameters
        ----------
        old : Any
            old value
        new : Any
            edited value
        index : QModelIndex
            item model index
        """
        if old != new:
            item = index.internalPointer()
            item._edit = new
            item.set_edited()

    def clear(self):
        """Clear data from the model."""
        self.load({})

    def load(self, data: dict):  # pragma: nocover
        """
        Load model from a nested dictionary returned by pyben.

        Parameters
        ----------
        data: dict
            dictionary data
        """
        self.beginResetModel()
        root = Item(parent=self._rootItem,
                    root=True,
                    data=data,
                    icon=self.torrent_icon)
        self._rootItem = Item.build(data, root)
        self.endResetModel()
        return True

    def add_row(self, path: str, meta: Any):
        """
        Add item row and tree to the model and view.

        Parameters
        ----------
        path : str
            path to torrent file
        meta : Any
            decoded bencode data
        """
        start = stop = self._rootItem.count()
        self.beginInsertRows(QModelIndex(), start, stop)
        top = Item(
            parent=self._rootItem,
            root=True,
            key=path,
            data=meta,
            icon=self.torrent_icon,
        )
        self._rootItem.add_child(top)
        Item.build(meta, top)
        self.endInsertRows()

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        """
        Override from QAbstractItemModel.

        Return data from a json item according index and role
        """
        if index and index.isValid():
            item = index.internalPointer()
            if role == Qt.DisplayRole:
                return item.text()
            if role == Qt.EditRole:
                if not item.has_children():
                    return item.text()
            elif role == Qt.DecorationRole:
                return item.icon()
        return None

    def setData(self, index: QModelIndex, value: Any, role: Qt.ItemDataRole):
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
            item = index.internalPointer()
            old = item.key
            if not item.has_children():
                item.key = value
                self.itemValueChanged.emit(old, value, index)
                self.dataChanged.emit(index, index, [Qt.EditRole])
                return True
        return False

    def index(self, row: int, column: int, parent=QModelIndex()):
        """
        Override from QAbstractItemModel.

        Return index according row, column and parent
        """
        if self.hasIndex(row, column, parent):
            if not parent.isValid():
                parentItem = self._rootItem
            else:
                parentItem = parent.internalPointer()
            childItem = parentItem.child(row)
            if childItem:
                return self.createIndex(row, column, childItem)
        return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        """
        Override from QAbstractItemModel.

        Return parent index of index
        """
        if index and index.isValid():
            childItem = index.internalPointer()
            parentItem = childItem.parent()
            if parentItem and parentItem != self._rootItem:
                return self.createIndex(parentItem.row(), 0, parentItem)
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        """
        Override from QAbstractItemModel.

        Return row count from parent index
        """
        parentItem = self._rootItem
        if parent.isValid():
            parentItem = parent.internalPointer()
        return parentItem.count()

    def columnCount(self, _=QModelIndex()):
        """
        Override from QAbstractItemModel.

        Return column number. For the model, it always return 2 columns
        """
        return 1

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """
        Override from QAbstractItemModel.

        Return flags of index
        """
        flags = super().flags(index)
        if index and index.isValid():
            item = index.internalPointer()
            if not item.has_children():
                flags |= Qt.ItemIsEditable
        return flags

    def to_bencode(self, item: Item) -> Any:  # pragma: nocover
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
        if not item.has_children():
            if item._edit is not None:
                return item._edit
            return None
        total = item.count()
        for i in range(total):
            child = item.child(i)
            change = self.to_bencode(child)
            if change is not None:
                data = item.parent().data
                data[item.key] = change
        if item._edit is not None:
            return item._edit
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
            self.tree.addChildInfo.emit(tfile, meta)
