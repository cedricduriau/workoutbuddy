# third party modules
from PySide2 import QtCore


class CheckableStringListModel(QtCore.QStringListModel):

    item_checked = QtCore.Signal(str, bool)

    def __init__(self, *args, **kwargs):
        self._checked_items = []
        super(CheckableStringListModel, self).__init__(*args, **kwargs)

    def flags(self, index):
        flags = super(CheckableStringListModel, self).flags(index)
        if index.isValid():
            flags |= QtCore.Qt.ItemIsUserCheckable
        return flags

    def setData(self, index, value, role):
        if not index.isValid() or role != QtCore.Qt.CheckStateRole:
            return False

        item = index.data(role=QtCore.Qt.DisplayRole)
        if value == QtCore.Qt.Checked:
            if item not in self._checked_items:
                self._checked_items.append(item)
                self.item_checked.emit(item, True)
        else:
            self._checked_items.remove(item)
            self.item_checked.emit(item, False)

        self.dataChanged.emit(index, index)
        return True

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == QtCore.Qt.CheckStateRole:
            item = index.data(role=QtCore.Qt.DisplayRole)
            return QtCore.Qt.Checked if item in self._checked_items else QtCore.Qt.Unchecked

        return super(CheckableStringListModel, self).data(index, role)

    def get_items(self):
        items = []
        for i in range(self.rowCount()):
            index = self.index(i, 0)
            item = index.data(role=QtCore.Qt.DisplayRole)
            items.append(item)
        return items

    def get_checked_items(self):
        items = self._checked_items.copy()
        return items

    def set_checked_items(self, items):
        for i in range(self.rowCount()):
            index = self.index(i, 0)
            value = index.data(role=QtCore.Qt.DisplayRole)
            checkstate = QtCore.Qt.Checked if value in items else QtCore.Qt.Unchecked
            self.setData(index, checkstate, QtCore.Qt.CheckStateRole)
