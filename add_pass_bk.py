import sys
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem
from ui.Add_password_frontend import Ui_Add_password

class Add_pass(QMainWindow, Ui_Add_password):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


