from PyQt5.QtWidgets import QTreeView, QApplication, QAbstractItemView
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt, QItemSelection, QItemSelectionModel
import pickle


class TreeNode:
    def __init__(self, data):
        self._data = data
        self._children = []
        self._parent = None
        self._row = 0

    def data(self, column):
        return self._data

    def columnCount(self):
        return 1

    def childCount(self):
        return len(self._children)

    def child(self, row):
        return self._children[row]

    def parent(self):
        return self._parent

    def row(self):
        return self._row

    def addChild(self, child):
        child._parent = self
        child._row = len(self._children)
        self._children.append(child)


class TreeModel(QAbstractItemModel):
    def __init__(self, filepath, name):
        super().__init__()

        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        self.root_node = TreeNode(name)

        self.from_dict(data, self.root_node)

    def from_dict(self, d, parent):
        for key, value in sorted(d.items()):
            if isinstance(value, dict):
                name = value['name']
                node = TreeNode(name)
                parent.addChild(node)
                self.from_dict(value, node)

    def rowCount(self, in_index):
        if in_index.isValid():
            return in_index.internalPointer().childCount()
        return self.root_node.childCount()

    def addChild(self, in_node, in_parent):
        if not in_parent or not in_parent.isValid():
            parent = self._root
        else:
            parent = in_parent.internalPointer()
        parent.addChild(in_node)

    def index(self, in_row, in_column, in_parent=None):
        if not in_parent or not in_parent.isValid():
            parent = self.root_node
        else:
            parent = in_parent.internalPointer()

        if not self.hasIndex(in_row, in_column, QModelIndex()):
            return QModelIndex()

        child = parent.child(in_row)
        if child:
            return QAbstractItemModel.createIndex(self, in_row, in_column, child)
        else:
            return QModelIndex()

    def parent(self, in_index):
        if in_index.isValid():
            p = in_index.internalPointer().parent()
            if p:
                return QAbstractItemModel.createIndex(self, p.row(), 0, p)
        return QModelIndex()

    def columnCount(self, in_index):
        return 1

    def data(self, in_index, role):
        if not in_index.isValid():
            return None
        node = in_index.internalPointer()
        if role == Qt.DisplayRole:
            return node.data(in_index.column())
        return None


def main():
    import sys
    app = QApplication(sys.argv)
    items = []

    v = QTreeView()
    model = TreeModel('../resources/disease_num2name.p', 'Disease')
    v.setModel(model)
    v.selectionModel().select(QItemSelection(model.index(0, 0), model.index(5, 0)), QItemSelectionModel.Select)
    v.setSelectionMode(QAbstractItemView.NoSelection)
    v.setEditTriggers(QAbstractItemView.NoEditTriggers)
    v.show()
    app.exec()

v = main()  