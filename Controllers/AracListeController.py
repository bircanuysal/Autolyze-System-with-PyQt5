from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from Views.aracliste.AracListeView import Ui_CarList_Widget
from Models.Database import Database

class AracListeController(QWidget):
    def __init__(self, user):
        super().__init__()
        self.ui = Ui_CarList_Widget()
        self.ui.setupUi(self)

        self.user = user
        self.db = Database()

        self.load_table()

    def load_table(self):
        cars = self.db.get_cars_by_user(self.user.id)
        self.ui.tableWidget.setRowCount(len(cars))
        for row, car in enumerate(cars):
            self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(str(car.id)))
            self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(str(car.carNo)))
            self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(f"{car.brand} / {car.model}"))
            self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(str(car.km)))
            self.ui.tableWidget.setItem(row, 4, QTableWidgetItem(str(car.year)))
            self.ui.tableWidget.setItem(row, 5, QTableWidgetItem(str(car.painted_count)))
            self.ui.tableWidget.setItem(row, 6, QTableWidgetItem(str(car.changed_count)))
            self.ui.tableWidget.setItem(row, 7, QTableWidgetItem(str(car.score)))
