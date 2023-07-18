import os
from PyQt6 import uic
from PyQt6 import QtWidgets
from PyQt6 import QtCore


class ViewRecipe(QtWidgets.QDialog):
    def __init__(self, db, forms_dir, mainViewTV):
        super().__init__()
        uic.load_ui.loadUi(os.path.join(forms_dir, "view_recipe.ui"), self)
        self.db = db
        self.mainViewTV = mainViewTV
        self.setWindowFlags(
            QtCore.Qt.WindowType.CustomizeWindowHint
            | QtCore.Qt.WindowType.WindowTitleHint
            | QtCore.Qt.WindowType.WindowMaximizeButtonHint
            | QtCore.Qt.WindowType.WindowMinimizeButtonHint)

        # Signals
        self.closePB.clicked.connect(self.close)

        # Methods
        self.show_data()

    def get_data_list(self):
        data_list = []
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
            data_list.append(list[1]) # name
            data_list.append(list[2]) # date
            data_list.append(list[3]) # ingredients
            data_list.append(list[4]) # instructions
        return data_list

    def show_data(self):
        data_list = self.get_data_list()
        self.nameLB.setText(data_list[0])
        self.dateLB.setText(data_list[1].toString())
        self.ingredientsTE.setHtml(data_list[2])
        self.instructionsTE.setHtml(data_list[3])

    def closeEvent(self, event):
        event.accept()

