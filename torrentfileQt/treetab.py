import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from torrentfileQt.utils import browse_torrent, browse_folder, get_icon
import pyben

class EditInfoWidget(QWidget):
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
        self.treeview = TreeView(self)
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



class TreeView(QTreeWidget):

    addChildInfo = Signal([str, dict])

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setProperty("InfoTree", "true")
        self.setHeaderHidden(True)
        self.addChildInfo.connect(self.add_data)
        self.data_icon = QIcon(get_icon("data"))
        self.list_icon = QIcon(get_icon("list"))
        self.torrent_icon = QIcon(get_icon("torrentfile"))
        self.brackets_icon = QIcon(get_icon("brackets"))

    def add_data(self, path, meta):
        item = QTreeWidgetItem(type=0)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        item.setText(0, path)
        self.addTopLevelItem(item)
        item.setIcon(0, self.torrent_icon)
        self.traverse_meta(item, meta)

    def traverse_meta(self, root, meta):
        if isinstance(meta, (str, bytes, int, float)):
            item = QTreeWidgetItem(type=0)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled|
                         Qt.ItemFlag.ItemIsEditable|
                         Qt.ItemFlag.ItemNeverHasChildren)
            if isinstance(meta, bytes) and len(meta) > 150:
                item.data = meta
                item.setText(0,str(meta)[:150] + "...")
            else:
                item.setText(0, str(meta))
            item.setIcon(0, self.data_icon)
            root.addChild(item)
        elif isinstance(meta, (list, tuple, set)):
            for i, value in enumerate(meta):
                item = QTreeWidgetItem(type=0)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                item.setText(0, f"[{i}]")
                item.setIcon(0, self.list_icon)
                root.addChild(item)
                self.traverse_meta(item, value)
        elif isinstance(meta, dict):
            for k,v in meta.items():
                item = QTreeWidgetItem(type=0)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                item.setIcon(0, self.brackets_icon)
                item.setText(0, str(k))
                root.addChild(item)
                self.traverse_meta(item, v)

class Thread(QThread):
    def __init__(self, lst, tree):
        super().__init__()
        self.lst = lst
        self.tree = tree

    def run(self):
        for tfile in self.lst:
            meta = pyben.load(tfile)
            self.tree.addChildInfo.emit(tfile, meta)
