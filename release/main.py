from PyQt6.QtWidgets import QWidget, QApplication, QTableWidgetItem, QDialog, QLineEdit, QPushButton
from UI import dialog_ui, main_ui
import sqlite3
import sys


class Dialog(QDialog, dialog_ui.Ui_Dialog):
    def __init__(self, dicters):
        super().__init__()
        self.setupUi(self)
        self.dicters = dicters
        # self.tabWidget.tab.sort_name.setText(dicters['name'])
        # self.tabWidget.tab.degree_roating.setText(dicters['color'])
        # self.tabWidget.tab.ground.setText(dicters['bools'])
        # self.tabWidget.tab.description.setText(dicters['dsecr'])
        # self.tabWidget.tab.price.setText(dicters['price'])
        # self.tabWidget.tab.volume.setText(dicters['volume'])
        self.sp_name = ['sort_name', 'degree_roating', 'ground', 'description', 'price', 'volume']
        self.sp_name_2 = list(map(lambda x: x + '1', self.sp_name))
        self.tab1 = self.tabWidget.widget(0)
        self.tab2 = self.tabWidget.widget(1)
        self.dicters_1 = {elem: self.tab1.findChild(QLineEdit, elem) for elem in self.sp_name}
        self.dicters_2 = {elem: self.tab2.findChild(QLineEdit, elem) for elem in self.sp_name_2}
        btn_1 = self.tab1.findChild(QPushButton, 'save_btn')
        btn_2 = self.tab2.findChild(QPushButton, 'save_btn1')
        if dicters.get('id'):
            for key in self.sp_name:
                self.dicters_1[key].setText(self.dicters[key])
        self.con = sqlite3.connect('release/data/coffee.sql')
        self.cur = self.con.cursor()
        btn_1.clicked.connect(self.updates)
        btn_2.clicked.connect(self.save_s)



    def updates(self):
        new_dc = {e: self.dicters_1[e].text() for e in self.sp_name}
        car = tuple(list(new_dc.values())  + [self.dicters['id']])
        self.cur.execute('''UPDATE COFFEE SET Название_сорта = ?, Степень_обжарки = ?, Тип_кофе = ?, Описание_вкуса = ?, Цена = ?, Объем_упаковки = ? WHERE ID = ?''', car)
        self.con.commit()
        self.close()

    def save_s(self):
        self.cur.execute('''SELECT * FROM COFFEE''')
        id_s = len(self.cur.fetchall())
        new_dc = {e: self.dicters_2[e].text() for e in self.sp_name_2}
        car = tuple(list(new_dc.values())  + [id_s])
        self.cur.execute('''UPDATE COFFEE SET Название_сорта = ?, Степень_обжарки = ?, Тип_кофе = ?, Описание_вкуса = ?, Цена = ?, Объем_упаковки = ? WHERE ID = ?''', car)
        self.con.commit()
        self.close()


class Coffe(QWidget, main_ui.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('release/data/coffee.sql', )
        self.cur = self.con.cursor()
        self.cur.execute('''SELECT * FROM Coffee''')
        res = self.cur.fetchall()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(res))
        for row_index, row_data in enumerate(res):
            for col_index, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
        self.upd.clicked.connect(self.update_coffe)

    def update_coffe(self):
        a = self.tableWidget.selectedIndexes()
        if a:
            a = self.tableWidget.item(a[0].row(), 0).text()
            self.cur.execute('''SELECT * FROM Coffee WHERE ID = ?''', (int(a), ))
            res = self.cur.fetchall()[0]
            q = Dialog({'id': res[0], 'sort_name': res[1], 'degree_roating': res[2], 'ground': res[3], 'description': res[4], 'price': str(res[5]), 'volume': str(res[6])})
        else:
            q = Dialog({})
        q.exec()
        self.cur.execute('''SELECT * FROM Coffee''')
        res = self.cur.fetchall()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(res))
        for row_index, row_data in enumerate(res):
            for col_index, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
        self.upd.clicked.connect(self.update_coffe)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffe()
    ex.show()
    sys.exit(app.exec())