from PyQt5.QtWidgets import QTreeView, QAbstractItemView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QModelIndex, QItemSelectionModel, pyqtSignal

from src.ViewTree import TreeModel
import pickle


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
                names.append(value)
        self.select_by_names(names)



