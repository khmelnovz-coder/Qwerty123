from PyQt6 import QtCore
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from ui.Qwerty_main_frontend import Ui_Qwerty_main
from database import DatabaseManager
from password import SecurityManager
from add_pass_bk import Add_pass


class Qwerty123_m(QMainWindow, Ui_Qwerty_main):
    def __init__(self, db_manager, security_manager, master_key):
        super().__init__()
        self.db = db_manager
        self.sec = security_manager
        self.master_key = master_key
        self.setupUi(self)
        self.listWidget.itemClicked.connect(self.display_account_details)
        self.no_item = True
        self.accounts = self.db.get_all_accounts()
        self.cr_new_pass.clicked.connect(self.create_pass)

        self.load_accounts()

    def load_accounts(self):
        self.listWidget.clear()

        if self.no_item:
            self.title.setText("")
            self.label_6.setText("")
            self.label_7.setText("")
            self.label_8.setText("")
            self.website.setText("")
            self.password.setText("")
            self.user.setText("")

            for acc in self.accounts:
                service_name = acc[1]
                item = QListWidgetItem(service_name)
                item.setData(QtCore.Qt.ItemDataRole.UserRole, acc)
                self.listWidget.addItem(item)


    def display_account_details(self, item):
        acc_data = item.data(QtCore.Qt.ItemDataRole.UserRole)

        service_name = acc_data[1]
        login = acc_data[2]
        encrypted_pass = acc_data[3]
        decrypted_pass = self.sec.decoding(encrypted_pass, self.master_key)
        self.no_item = False
        self.no_item_choosen.hide()
        self.title.setText(service_name)
        self.user.setText(login)
        self.password.setText(decrypted_pass)
        self.website.setText(service_name)





    def create_pass(self):
        self.add_pass = Add_pass(self.sec)
        self.add_pass.show()

