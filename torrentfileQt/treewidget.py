from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem

from .qss import treeSheet


class TreeWidget(QTreeWidget):
    """Tree view of the directory structure cataloged in .torrent file.

    Args:
        parent (`widget`, default=`None`): The widget containing this widget.
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.tree = None
        self.root = self.invisibleRootItem()
        self.root.setChildIndicatorPolicy(self.root.ChildIndicatorPolicy.ShowIndicator)
        self.setIndentation(10)
        self.setEditTriggers(self.EditTrigger.NoEditTriggers)
        self.setHeaderHidden(True)
        self.setItemsExpandable(True)
        self.setColumnCount(1)
        self.setStyleSheet(treeSheet)

    def apply_value(self, tree):
        for key, value in tree.items():
            if key == "":
                for item in self.apply_value(value):
                    yield item
            elif isinstance(value, dict):
                item = TreeItem(self, 0)
                item.setText(0, key)
                for child in self.apply_value(value):
                    item.addChild(child)
                yield item
            else:
                item = TreeItem(type=0)
                item.setText(0, key)
                child = TreeItem(type=0)
                child.setText(0, str(value))
                item.addChild(child)
                yield item

    def set_tree(self, tree):
        self.tree = tree
        for key, value in tree.items():
            top_item = TreeItem(type=0)
            top_item.setText(0, key)
            for item in self.apply_value(value):
                top_item.addChild(item)
            self.addTopLevelItem(top_item)

    def assign_children(self, groups, parent):
        for k, v in groups.items():
            item = TreeItem(type=0)
            item.setText(0, k)
            parent.addChild(item)
            if not isinstance(v, dict):
                length = TreeItem(type=0)
                length.setText(0, f"Length: {v} bytes")
                length.alt_icon()
                item.addChild(length)
                continue
            self.assign_children(v, item)

    def set_files(self, filelist):
        groups = {}
        for item in filelist:
            current = groups
            partials = item["path"]
            parts, start = len(partials), 0
            while start < parts:
                partial = partials[start]
                if start == parts - 1:
                    current[partial] = item["length"]
                elif partial in current:
                    current = current[partial]
                else:
                    current[partial] = {}
                    current = current[partial]
                start += 1
        self.assign_children(groups, self.root)


class TreeItem(QTreeWidgetItem):
    def __init__(self, type=0):
        super().__init__(type=type)
        icon = QIcon("./assets/folder.png")
        self.setIcon(0, icon)
        self.setChildIndicatorPolicy(self.ChildIndicatorPolicy.ShowIndicator)

    def alt_icon(self):
        icon = QIcon("./assets/ruler.png")
        self.setIcon(0, icon)
