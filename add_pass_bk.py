import sys
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem
from ui.Add_password_frontend import Ui_Add_password


class Add_pass(QMainWindow, Ui_Add_password):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cancel.clicked.connect(self.cancel_new)
        self.save_new_pass.clicked.connect(self.save_new_pass_def)

    def cancel_new(self):
        sys.exit(0)

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
            self.statusBar().showMessage("Не забудь ввести данные", 5000)

