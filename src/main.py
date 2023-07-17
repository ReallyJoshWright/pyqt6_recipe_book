import sys
import os
from PyQt6 import uic
from PyQt6 import QtWidgets
from PyQt6 import QtSql

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(SRC_DIR, os.pardir))
FORMS_DIR = os.path.join(PARENT_DIR, "forms")
CONFIG_DIR = os.path.join(PARENT_DIR, "config")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.load_ui.loadUi(os.path.join(FORMS_DIR, "mainwindow.ui"), self)

        self.recipe_query_model = QtSql.QSqlQueryModel()

        self.searchLE.textChanged.connect(self.recipe_search)
        self.quitAction.triggered.connect(self.close)

    def recipe_search(self):
        query = f"SELECT * FROM city;"
        self.recipe_query_model.setQuery(query, db)
        print(self.recipe_query_model.record(0).value('name'))

    def closeEvent(self, event):
        event.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
