import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem, QWidget


class Detailed(QMainWindow):
    def __init__(self):
        super(Detailed, self).__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        cur = self.con.cursor()
        self.result = cur.execute("SELECT * FROM info_about_coffe").fetchall()
        self.tableWidget.setColumnCount(len(self.result[0]))
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                                                    'описание вкуса', 'цена', 'объем упаковки'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()
        self.pushButton.clicked.connect(self.new)

    def new(self):
        self.New = New()
        self.New.show()


class New(QWidget):
    def __init__(self):
        super(New, self).__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.result = self.cur.execute("SELECT * FROM info_about_coffe").fetchall()
        self.pushButton_change.clicked.connect(self.change)
        self.pushButton_add.clicked.connect(self.add)

    def change(self):
        name = self.lineEdit_ch_name.text()
        id = self.lineEdit_ch_id.text()
        step = self.lineEdit_ch_stepen.text()
        zerno = self.lineEdit_ch_zerno.text()
        opis = self.lineEdit_ch_opisanie.text()
        cost = self.lineEdit_ch_cost.text()
        v = self.lineEdit_ch_V.text()
        self.cur.execute(f"""UPDATE info_about_coffe
            SET Name = ? WHERE ID = ? and ? != ?""", (name, id, name, ''))
        self.cur.execute(f"""UPDATE info_about_coffe
                    SET Degree_of_roasting = ? WHERE ID = ? and ? != ?""", (step, id, step, ''))
        self.cur.execute(f"""UPDATE info_about_coffe
                    SET mill_inGrains = ? WHERE ID = ? and ? != ?""", (zerno, id, zerno, ''))
        self.cur.execute(f"""UPDATE info_about_coffe
                    SET Taste_description = ? WHERE ID = ? and ? != ?""", (opis, id, opis, ''))
        self.cur.execute(f"""UPDATE info_about_coffe
                    SET Price = ? WHERE ID = ? and ? != ?""", (cost, id, cost, ''))
        self.cur.execute(f"""UPDATE info_about_coffe
                    SET Volume = ? WHERE ID = ? and ? != ?""", (v, id, v, ''))
        self.con.commit()
        self.con.close()

    def add(self):
        name1 = self.lineEdit_add_name.text()
        step1 = self.lineEdit_add_stepen.text()
        zerno1 = self.lineEdit_add_zerno.text()
        opis1 = self.lineEdit_add_opisanie.text()
        cost1 = self.lineEdit_add_cost.text()
        v1 = self.lineEdit_add_V.text()
        self.cur.execute("""INSERT INTO info_about_coffe (Name, Degree_of_roasting, mill_inGrains, Taste_description,
        Price, Volume) VALUES(?, ?, ?, ?, ?, ?)""", (name1, step1, zerno1, opis1, cost1, v1))
        self.con.commit()
        self.con.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Detailed()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
