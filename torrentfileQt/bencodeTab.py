import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
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
        self.hlayout1 = QHBoxLayout()
        self.hlayout1.addWidget(self.file_button)
        self.hlayout1.addWidget(self.folder_button)
        self.layout.addLayout(self.hlayout1)
        self.treeview = BencodeView(self)
        self.layout.addWidget(self.treeview)
        self.file_button.clicked.connect(self.load_file)
        self.folder_button.clicked.connect(self.load_folder)

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

    def add_data(self, path, meta):
        self.data_items[path] = meta
        self.bencode_model.add_row(path, meta)


class Item:
    """A Json item corresponding to a line in QTreeView"""

    model = None

    def __init__(self, parent=None):
        self._parent = parent
        self._key = ""
        self._value = ""
        self._value_type = ""
        self._children = []
        self._icon = None
        self._edited = False

    def set_edited(self):
        self._edited = True
        if self._parent:
            self._parent.set_edited()

    def setIcon(self, icon):
        self._icon = icon

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
    def build(cls, meta, root=None):
        """
        Create a 'root' TreeItem from a nested list or a nested dictonary.

        Returns
        -------
        TreeItem
            TreeItem
        """
        rootItem = Item(root)
        rootItem.key = "root"
        if isinstance(meta, dict):
            for key, value in meta.items():
                child = cls.build(value, rootItem)
                child.key = key
                child.value_type = dict
                child.setIcon(cls.model.brackets_icon)
                rootItem.add_child(child)
                rootItem.value_type = dict
                rootItem.setIcon(cls.model.brackets_icon)
        elif isinstance(meta, (list, tuple, set)):
            for index, value in enumerate(meta):
                child = cls.build(value, rootItem)
                child.key = index
                child.value_type = type(meta)
                child.setIcon(cls.model.list_icon)
                rootItem.add_child(child)
                rootItem.value_type = list
                rootItem.setIcon(cls.model.list_icon)
        else:
            child = cls(rootItem)
            child.key = meta
            child.value_type = type(meta)
            child.setIcon(cls.model.data_icon)
            rootItem.add_child(child)
        return rootItem


class BencodeModel(QAbstractItemModel):
    """ An editable model of Json data """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._rootItem = Item()
        self._rootItem.value_type = list
        self.data_icon = QIcon(get_icon("data"))
        self.list_icon = QIcon(get_icon("list"))
        self.torrent_icon = QIcon(get_icon("torrentfile"))
        self.brackets_icon = QIcon(get_icon("brackets"))
        Item.set_model(self)

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
        child_item = Item.build(meta)
        child_item.key = path
        child_item.value_type = "torrent"
        child_item.setIcon(self.torrent_icon)
        self._rootItem.add_child(child_item)
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
            if not item.has_children():
                item.key = str(value)
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

    def to_bencode(self, item=None):
        if item is None:
            item = self._rootItem
        nchild = item.count()
        if item.value_type is dict:
            meta = {}
            for i in range(nchild):
                ch = item.child(i)
                meta[ch.key] = self.to_bencode(ch)
            return meta
        elif item.value_type == list:
            meta = []
            for i in range(nchild):
                ch = item.child(i)
                meta.append(self.to_json(ch))
            return meta
        else:
            return item.key


class Thread(QThread):
    def __init__(self, lst, tree):
        super().__init__()
        self.lst = lst
        self.tree = tree

    def run(self):
        for tfile in self.lst:
            meta = pyben.load(tfile)
            self.tree.addChildInfo.emit(tfile, meta)
