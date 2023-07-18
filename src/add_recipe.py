import os
from PyQt6 import uic
from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6 import QtSql


class AddRecipe(QtWidgets.QDialog):
    def __init__(self, db, forms_dir):
        super().__init__()
        uic.load_ui.loadUi(os.path.join(forms_dir, "add_recipe.ui"), self)
        self.db = db
        self.setWindowFlags(
            QtCore.Qt.WindowType.CustomizeWindowHint
            | QtCore.Qt.WindowType.WindowTitleHint
            | QtCore.Qt.WindowType.WindowMaximizeButtonHint
            | QtCore.Qt.WindowType.WindowMinimizeButtonHint)

        # Signals
        self.nameLE.textChanged.connect(self.reset)
        self.savePB.clicked.connect(self.save)
        self.closePB.clicked.connect(self.close)

    def reset(self):
        self.sender().setStyleSheet("background: white")

    def save(self):
        if self.nameLE.text() == "":
            self.nameLE.setStyleSheet("background: red")
            self.nameLE.setFocus()
            return
        name = self.nameLE.text()
        ingredients = self.ingredientsTE.toHtml()
        instructions = self.ingredientsTE.toHtml()
        query_str = f"INSERT INTO recipe (name, date, ingredients, \
                instructions, created_at, updated_at) VALUES ($${name}$$, \
                now(), $${ingredients}$$, $${instructions}$$, now(), now())"
        query = QtSql.QSqlQuery(self.db)
        success = query.exec(query_str)
        if success:
            QtWidgets.QMessageBox.information(self, "Success", "Your recipe \
                    has been saved")
            self.nameLE.clear()
            self.ingredientsTE.clear()
            self.instructionsTE.clear()
            self.nameLE.setFocus()
        else:
            print(f"Failed Query: {query_str}")
            print(f"THIS ERROR: {query.lastError().text()}")


    def closeEvent(self, event):
        event.accept()

