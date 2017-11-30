from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal

from PyQt5.QtWidgets import QTreeView, QApplication, QAbstractItemView
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt, QItemSelection, QItemSelectionModel
import pickle


class TreeNode:
    def __init__(self, data, number):
        self._data = data
        self._number = number
        self._children = []
        self._children_numbers = []
        self._parent = None
        self._row = 0

    def number(self):
        return self._number

    def children_numbers(self):
        return self._children_numbers

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
        self._children_numbers.append(child.number())
        self._children.append(child)


# Will load tree model from dictionary and populate it
class TreeModel(QAbstractItemModel):
    def __init__(self, filepath, name, parent=None):
        super().__init__(parent)

        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        self.root_node = TreeNode(name, "Root")
        self.from_dict(data, self.root_node)

    def from_dict(self, d, parent):
        for key, value in sorted(d.items()):
            if isinstance(value, dict):
                name = value['name']
                node = TreeNode(name, key)
                parent.addChild(node)
                self.from_dict(value, node)

    def rowCount(self, parent_index=QModelIndex()):
        if parent_index.isValid():
            return parent_index.internalPointer().childCount()
        return self.root_node.childCount()

    def addChild(self, node, index):
        if not index or not index.isValid():
            parent = self._root
        else:
            parent = index.internalPointer()
        parent.addChild(node)

    def index(self, row, column, parent=None):
        if not parent or not parent.isValid():
            parent = self.root_node
        else:
            parent = parent.internalPointer()

        if not self.hasIndex(row, column, QModelIndex()):
            return QModelIndex()

        child = parent.child(row)
        if child:
            return QAbstractItemModel.createIndex(self, row, column, child)
        else:
            return QModelIndex()

    def parent(self, index):
        if index.isValid():
            p = index.internalPointer().parent()
            if p:
                return QAbstractItemModel.createIndex(self, p.row(), 0, p)
        return QModelIndex()

    def columnCount(self, index):
        return 1

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        node = index.internalPointer()

        if role == Qt.DisplayRole:
            return node.data(index.column())
        return None

    def headerData(self, p_int, Qt_Orientation, role=None):
        return self.root_node.data(0)

class TreeWidget(QTreeView):
    codes = {"disease": 'C',
             "drug": 'D'}

    element_selected = pyqtSignal('QString')

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name

        self.model = TreeModel("resources/%s_num2name.p" % name, "", self)

        with open("resources/%s_num2name.p" % name, "rb") as f:
            self.num2name = pickle.load(f)
        with open("resources/%s_name2num.p" % name, "rb") as f:
            self.name2num = pickle.load(f)

        self.setModel(self.model)

        self.font = QFont()
        self.font.setPixelSize(9)
        self.setFont(self.font)
        self.unselect_all()

        self.doubleClicked.connect(self.selected_slot)

    def select_by_names(self, names):
        self.unselect_all()

        for name in names:
            try:
                codes = self.name2num[name].split(" ")
                for code in codes:
                    if code[0] != TreeWidget.codes[self.name]:
                        continue

                    keys = code[1:].split(".")

                    node = self.model.root_node
                    index = QModelIndex()
                    for key in keys:
                        row = node.children_numbers().index(key)
                        index = self.model.index(row, 0, index)
                        node = index.internalPointer()
                        self.selectionModel().select(index, QItemSelectionModel.Select)
                        self.expand(index)
                    self.selectionModel().select(index, QItemSelectionModel.Select)
            except:
                print("Could not select using this name: %s" % name)

    def selected_slot(self, index):
        self.element_selected.emit(self.model.data(index))

    def unselect_all(self):
        self.selectionModel().clearSelection()
        self.collapseAll()

    def highlight_bot_request(self, resolved_query, parameters, contexts, action):
        self.unselect_all()
        names = []
        for key, value in parameters.items():
            if self.name in key:
                names.extend(value)
        self.select_by_names(names)


def main():
    import sys
    app = QApplication(sys.argv)

    v = QTreeView()
    model = TreeModel('../resources/disease_num2name.p', 'Disease')
    v.setModel(model)
    v.selectionModel().select(QItemSelection(model.index(0, 0), model.index(5, 0)), QItemSelectionModel.Select)
    v.setSelectionMode(QAbstractItemView.NoSelection)
    v.setEditTriggers(QAbstractItemView.NoEditTriggers)
    v.show()
    app.exec()

if __name__ == "__main__":
    main()



