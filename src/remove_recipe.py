import os
from PyQt6 import uic
from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6 import QtSql


class RemoveRecipe(QtWidgets.QDialog):
    def __init__(self, db, forms_dir, rc):
        super().__init__()
        uic.load_ui.loadUi(os.path.join(forms_dir, "remove_recipe.ui"), self)
        self.db = db
        self.rc = rc
        self.setWindowFlags(
            QtCore.Qt.WindowType.CustomizeWindowHint
            | QtCore.Qt.WindowType.WindowTitleHint
            | QtCore.Qt.WindowType.WindowMaximizeButtonHint
            | QtCore.Qt.WindowType.WindowMinimizeButtonHint)

        # Attributes
        self.recipe_table_model = QtSql.QSqlTableModel(self, self.db)
        self.recipe_proxy_model = QtCore.QSortFilterProxyModel()
        self.recipe_proxy_model.setFilterCaseSensitivity(
                QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self.recipe_proxy_model.setDynamicSortFilter(True)
        self.recipe_proxy_model.setFilterKeyColumn(-1)
        self.mainViewTV.setModel(self.recipe_proxy_model)

        # Signals
        self.searchLE.textChanged.connect(self.search)
        self.removePB.clicked.connect(self.remove)
        self.closePB.clicked.connect(self.close)

        # Methods
        self.load_recipes()

    def load_recipes(self):
        query = f"SELECT * FROM recipe;"
        query_model = QtSql.QSqlQueryModel()
        query_model.setQuery(query, self.db)
        self.recipe_proxy_model.setSourceModel(query_model)
        self.mainViewTV.setColumnHidden(self.rc.id, True)
        self.mainViewTV.setColumnHidden(self.rc.ingredients, True)
        self.mainViewTV.setColumnHidden(self.rc.instructions, True)
        self.mainViewTV.setColumnHidden(self.rc.created_at, True)
        self.mainViewTV.setColumnHidden(self.rc.updated_at, True)
        self.mainViewTV.setSortingEnabled(True)
        self.mainViewTV.sortByColumn(self.rc.name, 
                                     QtCore.Qt.SortOrder.AscendingOrder)
        self.mainViewTV.resizeColumnsToContents()
        self.mainViewTV.resizeRowsToContents()
        self.mainViewTV.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeMode.Stretch)

    def search(self, text):
        if text == "":
            self.searchLE.clear()
        self.recipe_proxy_model.setFilterFixedString(text)

    def get_id_list(self):
        id_list = []
        selected_indexes = self.mainViewTV.selectionModel().selectedIndexes()
        rows = {index.row() for index in selected_indexes}
        output = []
        for row in rows:
            row_data = []
            for column in range(self.mainViewTV.model().columnCount()):
                index = self.mainViewTV.model().index(row, column)
                row_data.append(index.data())
            output.append(row_data)
        for list in output:
            id_list.append(list[0])
        id_list_str = str(id_list)
        id_list_str = id_list_str[1:-1]
        id_list_str = "(" + id_list_str + ")"
        return id_list_str

    def remove(self):
        id_list_str = self.get_id_list()
        query_str = f"DELETE FROM recipe WHERE id IN {id_list_str}"
        query = QtSql.QSqlQuery(self.db)
        success = query.exec(query_str)
        if success:
            QtWidgets.QMessageBox.information(self, "Success", "Your recipe \
                    has been deleted")
            self.load_recipes()
        else:
            print(f"Failed Query: {query_str}")
            print(f"THIS ERROR: {query.lastError().text()}")

    def closeEvent(self, event):
        event.accept()

