# third party modules
from PySide2 import QtCore


class CheckableStringListModel(QtCore.QStringListModel):
    """Custom QStringListModel with checkable items."""

    # signals
    item_checked = QtCore.Signal(str, bool)

    def __init__(self, *args, **kwargs):
        """Initialize the objects."""
        self._checked_items = []
        super(CheckableStringListModel, self).__init__(*args, **kwargs)

    # overrides
    def flags(self, index):
        """
        Return the flags of an index.

        :param index: Model index.
        :type index: QtCore.QModelIndex

        :rtype: QtCore.Qt.ItemFlags
        """
        flags = super(CheckableStringListModel, self).flags(index)
        if index.isValid():
            flags |= QtCore.Qt.ItemIsUserCheckable
        return flags

    def setData(self, index, value, role):
        """
        Set data on a model index.

        :param index: Model index.
        :type index: QtCore.QModelIndex

        :param value: Value to set on index.

        :param role: Role to display data for.
        :type role: QtCore.Qt.ItemDataRole

        :rtype: bool
        """
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
        """
        Return the data of an index.

        :param index: Model index.
        :type index: QtCore.QModelIndex

        :param role: Role to store data for.
        :type role: QtCore.Qt.ItemDataRole
        """
        if not index.isValid():
            return None

        if role == QtCore.Qt.CheckStateRole:
            item = index.data(role=QtCore.Qt.DisplayRole)
            return QtCore.Qt.Checked if item in self._checked_items else QtCore.Qt.Unchecked

        return super(CheckableStringListModel, self).data(index, role)

    # custom
    def get_items(self):
        """
        Return the displayed data of all model indexes.

        :rtype: list[str]
        """
        items = []
        for i in range(self.rowCount()):
            index = self.index(i, 0)
            item = index.data(role=QtCore.Qt.DisplayRole)
            items.append(item)
        return items

    def get_checked_items(self):
        """
        Return the displayed data of all checked model indexes.

        :rtype: list[str]
        """
        items = self._checked_items.copy()
        return items

    def find_item_index(self, item):
        """
        Return the index of an item.

        :param item: Displayed item.
        :type item: str

        :rtype: QtCore.QModelIndex
        """
        for i in range(self.rowCount()):
            index = self.index(i, 0)
            value = index.data(role=QtCore.Qt.DisplayRole)
            if value == item:
                return index
        return QtCore.QModelIndex()

    def set_item_checked(self, item, checked):
        """
        Set the checkstate of an item.

        :param item: Displayed item.
        :type item: str

        :param checked: True to check, False to uncheck.
        :type checked: bool
        """
        index = self.find_item_index(item)
        if index.isValid():
            checkstate = QtCore.Qt.Checked if checked else QtCore.Qt.Unchecked
            result = self.setData(index, checkstate, QtCore.Qt.CheckStateRole)
            return result
        return False
