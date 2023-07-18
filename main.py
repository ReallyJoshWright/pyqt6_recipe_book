import sys
import os
from PyQt6 import uic
from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6 import QtSql
from config.database import DB
from src.utils import RecipeColumns
from src.add_recipe import AddRecipe
from src.remove_recipe import RemoveRecipe
from src.view_recipe import ViewRecipe

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
FORMS_DIR = os.path.join(MAIN_DIR, "forms")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, db):
        super().__init__()
        uic.load_ui.loadUi(os.path.join(FORMS_DIR, "mainwindow.ui"), self)

        # Attributes
        self.db = db
        self.search_actions = [
                self.searchByNameAction,
                self.searchByDateAction,
                self.searchByIngredAction,
                self.searchByAllAction]
        self.recipe_table_model = QtSql.QSqlTableModel(self, self.db)
        self.recipe_proxy_model = QtCore.QSortFilterProxyModel()
        self.recipe_proxy_model.setFilterCaseSensitivity(
                QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self.recipe_proxy_model.setDynamicSortFilter(True)
        self.recipe_proxy_model.setFilterKeyColumn(-1)
        self.searchByAllAction.setChecked(True)
        self.mainViewTV.setModel(self.recipe_proxy_model)

        self.searchByNameAction.setCheckable(True)
        self.searchByDateAction.setCheckable(True)
        self.searchByIngredAction.setCheckable(True)
        self.searchByAllAction.setCheckable(True)

        # Signals
        self.searchLE.textChanged.connect(self.recipe_search)
        self.mainViewTV.doubleClicked.connect(self.select)
        self.addRecipeAction.triggered.connect(self.add_recipe)
        self.removeRecipeAction.triggered.connect(self.remove_recipe)
        self.searchByNameAction.triggered.connect(self.set_search_filter)
        self.searchByDateAction.triggered.connect(self.set_search_filter)
        self.searchByIngredAction.triggered.connect(self.set_search_filter)
        self.searchByAllAction.triggered.connect(self.set_search_filter)
        self.quitAction.triggered.connect(self.close)

        # Methods
        self.load_recipes()

    def load_recipes(self):
        rc = RecipeColumns()
        query = f"SELECT * FROM recipe;"
        query_model = QtSql.QSqlQueryModel()
        query_model.setQuery(query, self.db)
        self.recipe_proxy_model.setSourceModel(query_model)
        self.mainViewTV.setColumnHidden(rc.id, True)
        self.mainViewTV.setColumnHidden(rc.ingredients, True)
        self.mainViewTV.setColumnHidden(rc.instructions, True)
        self.mainViewTV.setColumnHidden(rc.created_at, True)
        self.mainViewTV.setColumnHidden(rc.updated_at, True)
        self.mainViewTV.setSortingEnabled(True)
        self.mainViewTV.sortByColumn(rc.name, 
                                     QtCore.Qt.SortOrder.AscendingOrder)
        self.mainViewTV.resizeColumnsToContents()
        self.mainViewTV.resizeRowsToContents()
        self.mainViewTV.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeMode.Stretch)

    def recipe_search(self, text):
        if text == "":
            self.searchLE.clear()
        self.recipe_proxy_model.setFilterFixedString(text)

    def set_search_filter(self):
        try:
            if self.sender().isChecked():
                sender = self.sender()
                for i in self.search_actions:
                    i.setChecked(False)
                sender.setChecked(True)
                checked = sender.text()
            match checked:
                case "Search by Name":
                    self.recipe_proxy_model.setFilterKeyColumn(1)
                case "Search by Date":
                    self.recipe_proxy_model.setFilterKeyColumn(2)
                case "Search by Ingredients":
                    self.recipe_proxy_model.setFilterKeyColumn(3)
                case "Search by All":
                    self.recipe_proxy_model.setFilterKeyColumn(-1)
        except UnboundLocalError:
            self.searchByAllAction.setChecked(True)
            self.recipe_proxy_model.setFilterKeyColumn(-1)

    def select(self):
        dialog = ViewRecipe(self.db, FORMS_DIR, self.mainViewTV)
        dialog.exec()

    def add_recipe(self):
        dialog = AddRecipe(self.db, FORMS_DIR)
        dialog.exec()
        self.load_recipes()

    def remove_recipe(self):
        rc = RecipeColumns()
        dialog = RemoveRecipe(self.db, FORMS_DIR, rc)
        dialog.exec()
        self.load_recipes()

    def closeEvent(self, event):
        event.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)
    db = DB()
    window = MainWindow(db.connect)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
