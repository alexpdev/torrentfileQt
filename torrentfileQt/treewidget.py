import os

from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem

class TreeWidget(QTreeWidget):
    """Tree view of the directory structure cataloged in .torrent file.

    Args:
        parent (`widget`, default=`None`): The widget containing this widget.
    """

    stylesheet = """QTreeWidget{
        background-color: #2a2a2a;
        color: #ffffff;
    }
    QTreeWidgetItem{
        color: #ffffff;
        font: 9pt;
        font-style: italic;
        background-color: #2a2a2a;
    }"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.tree = None
        self.root = self.invisibleRootItem()
        self.indicator = self.root.ChildIndicatorPolicy
        self.childPolicy = self.indicator.DontShowIndicatorWhenChildless
        self.setIndentation(8)
        # self.setSortEnabled(False)
        self.setEditTriggers(self.EditTrigger.NoEditTriggers)
        self.root.setChildIndicatorPolicy(self.root.ChildIndicatorPolicy.DontShowIndicatorWhenChildless)
        self.setHeaderHidden(True)
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
                item.setChildIndicatorPolicy(self.childPolicy)
                item.setText(0, key)
                for child in self.apply_value(value):
                    item.addChild(child)
                yield item
            else:
                item = QTreeWidgetItem([key])
                item.setText(0, key)
                item.setChildIndicatorPolicy(self.childPolicy)
                child = QTreeWidgetItem([str(value)])
                child.setText(0, str(value))
                child.setChildIndicatorPolicy(self.childPolicy)
                item.addChild(child)
                yield item

    def set_tree(self, tree):
        self.tree = tree
        for key, value in tree.items():
            top_item = QTreeWidgetItem([key])
            top_item.setChildIndicatorPolicy(self.childPolicy)
            top_item.setText(0, key)
            for item in self.apply_value(value):
                top_item.addChild(item)
            self.addTopLevelItem(top_item)

    def set_files(self, lst):
        mapping = {}
        tree = {}
        for i, item in enumerate(lst):
            partials = item["path"]
            length = item["length"]
            level = tree
            if partials[0] not in tree:
                topitem = QTreeWidgetItem([partials[0]])
                topitem.setChildIndicatorPolicy(self.childPolicy)
                topitem.setText(0, partials[0])
                self.addTopLevelItem(topitem)
                level[partials[0]] = {}
                mapping[partials[0]] = topitem
                level = level[partials[0]]
                parent = topitem
            if len(partials) > 1:
                for i, partial in enumerate(partials[1:]):
                    treeitem = QTreeWidgetItem([partial])
                    treeitem.setChildIndicatorPolicy(self.childPolicy)
                    treeitem.setText(0, partial)
                    if partial is partials[-1]:
                        pathitem = QTreeWidgetItem([os.path.join(*partials)])
                        pathitem.setChildIndicatorPolicy(self.childPolicy)
                        pathitem.setText(0, os.path.join(*partials))
                        lengthitem = QTreeWidgetItem([str(length)])
                        lengthitem.setChildIndicatorPolicy(self.childPolicy)
                        lengthitem.setText(0, str(length))
                        parent.addChild(treeitem)
                        treeitem.addChild(pathitem)
                        treeitem.addChild(lengthitem)
                        mapping[os.path.join(*partials)] = treeitem
                        level[partial] = [os.path.join(*partials), length]
                    else:
                        ref = os.path.join(*partials[:i])
                        parent.addChild(treeitem)
                        mapping[os.path.join(ref, partial)] = treeitem
                        level[partial] = {}
                        level = level[partial]
                    parent = treeitem
            else:
                tree[partials[0]] = [os.path.join(*partials), str(length)]
                pathitem = QTreeWidgetItem([os.path.join(*partials)])
                pathitem.setChildIndicatorPolicy(self.childPolicy)
                pathitem.setText(0, os.path.join(*partials))
                lengthitem = QTreeWidgetItem([str(length)])
                lengthitem.setChildIndicatorPolicy(self.childPolicy)
                lengthitem.setText(0, str(length))
                topitem.addChild(pathitem)
                topitem.addChild(lengthitem)
            print(tree)
