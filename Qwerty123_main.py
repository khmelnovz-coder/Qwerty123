from PyQt6 import QtCore, QtWidgets
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
        self.hide_details()
        self.load_accounts()
        self.password.setReadOnly(True)
        self.password.setMouseTracking(True)
        self.password.installEventFilter(self)
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        for field in (self.user, self.password, self.website):
            field.setReadOnly(True)
            field.setMouseTracking(True)
            field.installEventFilter(self)

        self.load_accounts()

    def load_accounts(self):
        self.listWidget.clear()
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
        self.show_details()

    def create_pass(self):
        self.add_pass = Add_pass(self.sec, self.db)
        self.add_pass.show()

    def hide_details(self):
        self.title.hide()
        self.user.hide()
        self.password.hide()
        self.website.hide()
        self.label_6.hide()
        self.label_7.hide()
        self.label_8.hide()
        self.no_item_choosen.show()

    def show_details(self):
        self.title.show()
        self.user.show()
        self.password.show()
        self.website.show()
        self.label_6.show()
        self.label_7.show()
        self.label_8.show()
        self.no_item_choosen.hide()

    def eventFilter(self, obj, event):
        if obj == self.password:
            if event.type() == QtCore.QEvent.Type.Enter:
                self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            elif event.type() == QtCore.QEvent.Type.Leave:
                self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            elif event.type() == QtCore.QEvent.Type.MouseButtonPress:
                text = self.password.text()
                if text:
                    QApplication.clipboard().setText(text)
                    self.statusbar.showMessage("Пароль скопирован в буфер обмена!", 3000)

        elif obj == self.user:
            if event.type() == QtCore.QEvent.Type.MouseButtonPress:
                text = self.user.text()
                if text:
                    QApplication.clipboard().setText(text)
                    self.statusbar.showMessage("Логин скопирован в буфер обмена!", 3000)

        elif obj == self.website:
            if event.type() == QtCore.QEvent.Type.MouseButtonPress:
                text = self.website.text()
                if text:
                    QApplication.clipboard().setText(text)
                    self.statusbar.showMessage("Сайт скопирован в буфер обмена!", 3000)

        return super().eventFilter(obj, event)
