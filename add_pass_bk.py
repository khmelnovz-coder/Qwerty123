import sys
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem, QLineEdit, QMessageBox, QApplication, QInputDialog
from PyQt6.QtCore import QEvent
from ui.Add_password_frontend import Ui_Add_password
from password import SecurityManager
from database import DatabaseManager
import random
import sqlite3
from PyQt6 import QtCore, QtWidgets



class Add_pass(QMainWindow, Ui_Add_password):
    def __init__(self, security_manager, database_manager, on_account_added=None):
        super().__init__()
        self.setupUi(self)
        self.cancel.clicked.connect(self.cancel_new)
        self.save_new_pass.clicked.connect(self.save_new_pass_def)
        self.level_1.setChecked(True)
        self.current_level = 1 if self.level_1.isChecked() else (2 if self.level_2.isChecked() else 3)
        self.sec = security_manager
        self.db = database_manager
        self.pass_add.setText(self.sec.generate_pass(self.current_level))
        self.pass_add.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_add.installEventFilter(self)
        self.n = random.randint(0, 2)
        self.level_1.toggled.connect(self.cr_new_pass_def)
        self.level_2.toggled.connect(self.cr_new_pass_def)
        self.level_3.toggled.connect(self.cr_new_pass_def)
        self.load_categories()
        self.on_account_added = on_account_added

        self.cancel.clicked.connect(self.cancel_new)
        self.save_new_pass.clicked.connect(self.save_new_pass_def)



        self.pass_add.setText(self.sec.generate_pass(self.current_level))
        if self.n == 0:
            self.login_add.setPlaceholderText("example@gmail.com")
            self.site_add.setPlaceholderText("google.com")
        elif self.n == 1:
            self.login_add.setPlaceholderText("example@yandex.ru")
            self.site_add.setPlaceholderText("music.yanex.ru")
        else:
            self.login_add.setPlaceholderText("typer_666")
            self.site_add.setPlaceholderText("monkeytype.com")

    def cancel_new(self):
        self.close()

    def eventFilter(self, obj, event):
        if obj == self.pass_add:
            if event.type() == QEvent.Type.Enter:
                self.pass_add.setEchoMode(QLineEdit.EchoMode.Normal)
            elif event.type() == QEvent.Type.Leave:
                self.pass_add.setEchoMode(QLineEdit.EchoMode.Password)
            elif event.type() == QEvent.Type.MouseButtonPress:
                password_text = self.pass_add.text()
                if password_text:
                    QApplication.clipboard().setText(password_text)
                    self.statusbar.showMessage("Пароль скопирован в буфер обмена!", 3000)

        return super().eventFilter(obj, event)

    def cr_new_pass_def(self):
        btn = self.sender()
        if btn.isChecked():
            btm = self.sender()
            if self.level_1.isChecked():
                current_level = 1
            elif self.level_2.isChecked():
                current_level = 2
            else:
                current_level = 3

            self.pass_add.setText(str(self.sec.generate_pass(current_level)))

    def load_categories(self):
        self.categories.clear()
        all_categories = self.db.get_all_categories()

        for cat_id, cat_name in all_categories:
            self.categories.addItem(cat_name, cat_id)

    def save_new_pass_def(self):
        good_password = True
        if not self.title_add.text():
            good_password = False
            self.title_add.setStyleSheet("border: 1px solid red;")
        else:
            self.title_add.setStyleSheet("border: none;")

        if not self.login_add.text():
            good_password = False
            self.login_add.setStyleSheet("border: 1px solid red;")
        else:
            self.login_add.setStyleSheet("border: none;")

        if not self.site_add.text():
            good_password = False
            self.site_add.setStyleSheet("border: 1px solid red;")
        else:
            self.site_add.setStyleSheet("border: none;")

        if not self.pass_add.text():
            good_password = False
            self.pass_add.setStyleSheet("border: 1px solid red;")
        else:
            self.pass_add.setStyleSheet("border: none;")

        if not good_password:
            self.statusbar.showMessage("Не забудь ввести данные", 5000)

        else:
            if "@" in self.login_add.text():
                pass
            category_id = self.categories.currentData(QtCore.Qt.ItemDataRole.UserRole)
            salt, _ = self.db.get_master_password()
            service = self.title_add.text()
            login = self.login_add.text()
            password = self.sec.encode(self.pass_add.text(), salt=salt)
            website = self.site_add.text()
            self.db.add_account(service, login, password, website, category_id)
            if self.on_account_added:
                self.on_account_added()

            self.close()

    def load_categories(self):
        self.categories.clear()
        all_categories = self.db.get_all_categories()

        for cat_id, cat_name in all_categories:
            self.categories.addItem(cat_name, cat_id)

        self.categories.addItem("➕ Добавить категорию...", -999)

    def handle_category_selection(self, index):
        data = self.categories.currentData(QtCore.Qt.ItemDataRole.UserRole)

        if data == -999:
            text, ok = QtWidgets.QInputDialog.getText(
                self, "Новая категория", "Введите название новой категории:"
            )

            if ok and text.strip():
                new_cat_id = self.db.add_category(text.strip())
                self.load_categories()

                idx = self.categories.findData(new_cat_id)
                if idx != -1:
                    self.categories.setCurrentIndex(idx)
            else:
                self.categories.setCurrentIndex(0)
