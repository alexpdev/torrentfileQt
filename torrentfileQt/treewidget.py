import os




from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem

class TreeWidget(QTreeWidget):
    """Tree view of the directory structure cataloged in .torrent file.

    Args:
        parent (`widget`, default=`None`): The widget containing this widget.
    """

    stylesheet = """QTreeWidget{
        background-color: #2a2a2a
        color: #ffffff
    }"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.tree = None
        self.root = self.invisibleRootItem()
        self.setIndentation(8)
        self.setSortEnabled(False)
        self.setEditTriggers(self.EditTrigger.NoEditTriggers)
        self.setItemsExpandable(True)
        self.setColumnCount(1)
        self.setStyleSheet(self.stylesheet)

    def apply_value(self, tree):
        for key, value in tree.items():
            if key == "":
                for item in self.apply_value(value):
                    yield item
            elif isinstance(value, dict):
                item = QTreeWidgetItem([key])
                item.setText(key)
                for child in self.apply_value(value):
                    item.addChild(child)
                yield item
            else:
                item = QTreeWidgetItem([key])
                item.setText(key)
                child = QTreeWidgetItem([value])
                child.setText(value)
                item.addChild(child)
                yield item

    def set_tree(self, tree):
        self.tree = tree
        for key, value in tree.items():
            top_item = QTreeWidgetItem([key])
            top_item.setText(key)
            for item in self.apply_value(value):
                top_item.addChild(item)
            self.addTopLevelItem(top_item)

    def set_file_list(self, lst):
        mapping = {}
        for item in lst:
            path = item["path"]
            top = mapping
            length = item["length"]
            for i, partial in enumerate(path):
                if i == 0:
                    top = QTreeWidgetItem([partial])
                    top.setText(partial)
                    self.addTopLevelItem(top)
                    mapping["partial"] = top
                elif i == len(path) - 1:
                    parent = mapping[os.path.join(*path[:i])]
                    part = QTreeWidgetItem([partial])
                    part.setText(partial)
                    full = os.path.join(*path)
                    child1 = QTreeWidgetItem([full])
                    child1.setText(full)
                    child2 = QTreeWidgetItem([str(length)])
                    child2.setText(str(length))
                    part.addChild(child1)
                    part.addChild(child2)
                    parent.addChild(part)
                    mapping[full] = [partial, length, full]
                else:
                    parent = mapping[os.path.join(*path[:i])]
                    full = os.path.join(parent, partial)
                    if full not in mapping:
                        treeitem = QTreeWidgetItem([partial])
                        treeitem.setText(partial)
                        parent.addChild(treeitem)
                        mapping[full] = treeitem
        self.tree = mapping
