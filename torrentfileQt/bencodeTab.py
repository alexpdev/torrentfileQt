import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from typing import Any
from torrentfileQt.utils import browse_torrent, browse_folder, get_icon
import pyben

class BencodeEditWidget(QWidget):
    def __init__(self, parent=None):
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

    def load_v(self):
        self.load_folder("V:\\.torrents")

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
        self.treeview.clear()

    def torrent_filter(self, paths):
        torrents = []
        for path in paths:
            if os.path.isfile(path) and path.endswith(".torrent"):
                torrents.append(path)
        return torrents

    def load_file(self, paths=None):
        paths = browse_torrent(self, paths)
        self.load_thread(paths)

    def load_thread(self, paths):
        self.thread = Thread(paths, self.treeview)
        self.thread.start()
        self.thread.finished.connect(self.thread.deleteLater)


    def load_folder(self, path=None):
        if not path:
            path = browse_folder(self, path)
        paths = [os.path.join(path, i) for i in os.listdir(path)]
        self.load_thread(paths)



class BencodeView(QTreeView):

    addChildInfo = Signal([str, dict])

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setProperty("InfoTree", "true")
        self.bencode_model = BencodeModel()
        self.setModel(self.bencode_model)
        self.setHeaderHidden(True)
        self.addChildInfo.connect(self.add_data)
        self.data_items = {}

    def clear(self):
        rows = self.model().rowCount()
        self.model().removeRows(0, rows)

    def add_data(self, path, meta):
        self.data_items[path] = meta
        self.bencode_model.add_row(path, meta)

    def rowCount(self):
        return self.model().rowCount()

    def item(self, row, column):
        return self.model().index(row, column).internalPointer()

    def save_item(self, item):
        path = item.key
        self.model().to_bencode(item)
        pyben.dump(item.data, path)

class Item:
    """A Json item corresponding to a line in QTreeView"""

    model = None

    def __init__(self, parent=None, key=None, root=False, _type=None,
                       index=None, data=None, value=None, icon=None):
        self._parent = parent
        self._key = key
        self._value = value
        self._root = root
        self._data = data
        self._type = _type
        self._children = []
        self._index = index
        self._icon = icon
        self._edited = False
        self._edit = None

    def set_edited(self):
        self._edited = True
        if self._parent is not None:
            self._parent.set_edited()

    def is_edited(self):
        return self._edited

    def setIcon(self, icon):
        self._icon = icon

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, other):
        self._data = other


    def icon(self):
        if not self._icon:
            return self.model.torrent_icon
        return self._icon

    def add_child(self, item):
        """Add item as a child"""
        self._children.append(item)

    def child(self, row):
        """Return the child of the current item from the given row"""
        return self._children[row]

    def parent(self):
        """Return the parent of the current item"""
        return self._parent

    def count(self):
        """Return the number of children of the current item"""
        return len(self._children)

    def row(self):
        """Return the row where the current item occupies in the parent"""
        return self._parent._children.index(self) if self._parent else 0

    def text(self):
        return str(self._key)

    def has_children(self):
        return len(self._children) != 0

    def index(self):
        return self._index

    @property
    def key(self) -> str:
        """Return the key name"""
        return self._key

    @key.setter
    def key(self, key: str):
        """Set key name of the current item"""
        self._key = key

    @property
    def value_type(self):
        return self._value_type

    @value_type.setter
    def value_type(self, other):
        self._value_type = other

    @classmethod
    def set_model(cls, model):
        cls.model = model

    @classmethod
    def build(cls, meta, root):
        if isinstance(meta, (int, float, str, bytes)):
            item = cls(key=meta, icon=cls.model.data_icon, data=meta, parent=root)
            root.add_child(item)
            return item
        elif isinstance(meta, (list, tuple, set)):
            for i, val in enumerate(meta):
                item = cls(index=i, key=i, parent=root,
                           icon=cls.model.list_icon, data=val)
                root.add_child(item)
                cls.build(val, item)
        elif isinstance(meta, dict):
            for key, val in meta.items():
                item = cls(
                    key=key, data=val, icon=cls.model.brackets_icon, parent=root
                )
                root.add_child(item)
                cls.build(val, item)
        return root

    def __str__(self):
        return str(self.data)
    __repr__ = __str__

class BencodeModel(QAbstractItemModel):
    """ An editable model of Json data """

    itemValueChanged = Signal([object, object, QModelIndex])

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._rootItem = Item()
        self._rootItem.value_type = list
        self.data_icon = QIcon(get_icon("data"))
        self.list_icon = QIcon(get_icon("list"))
        self.torrent_icon = QIcon(get_icon("torrentfile"))
        self.brackets_icon = QIcon(get_icon("brackets"))
        self.itemValueChanged.connect(self.setEdited)
        Item.set_model(self)

    def removeRows(self, start, stop, index=QModelIndex()):
        self.beginRemoveRows(index, start, stop)
        root = index.internalPointer()
        for i in range(start, stop):
            del root._children[0]

    def setEdited(self, old, new, index):
        if old != new:
            item = index.internalPointer()
            item._edit = new
            item.set_edited()

    def clear(self):
        """ Clear data from the model """
        self.load({})

    def load(self, data: dict):
        """
        Load model from a nested dictionary returned by pyben.load().

        Parameters
        ----------
        data: dict
            dictionary data
        """
        self.beginResetModel()
        self._rootItem = Item.build(data)
        self.endResetModel()
        return True

    def add_row(self, path, meta):
        start = stop = self._rootItem.count()
        self.beginInsertRows(QModelIndex(), start, stop)
        top = Item(parent=self._rootItem, root=True, key=path,
                   data=meta, icon=self.torrent_icon)
        self._rootItem.add_child(top)
        Item.build(meta, top)
        self.endInsertRows()

    def data(self, index, role):
        """
        Override from QAbstractItemModel.

        Return data from a json item according index and role
        """
        if index and index.isValid():
            item = index.internalPointer()
            if role == Qt.DisplayRole:
                return item.text()
            elif role == Qt.EditRole:
                if not item.has_children():
                    return item.text()
            elif role == Qt.DecorationRole:
                return item.icon()
        return None

    def setData(self, index, value, role):
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

    def index(self, row, column, parent=QModelIndex()):
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
        Override from QAbstractItemModel

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

    def columnCount(self, parent=QModelIndex()):
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

    def to_bencode(self, item):
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
        if item._edit:
            return item._edit





class Thread(QThread):
    def __init__(self, lst, tree):
        super().__init__()
        self.lst = lst
        self.tree = tree

    def run(self):
        for tfile in self.lst:
            meta = pyben.load(tfile)
            self.tree.addChildInfo.emit(tfile, meta)
