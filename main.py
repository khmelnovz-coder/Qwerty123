import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsOpacityEffect
from PyQt6.QtCore import QPropertyAnimation
from ui.Qwerty123_frontend import Ui_Qwerty1234
from password import SecurityManager
from database import DatabaseManager
from Qwerty123_main import Qwerty123_m
import datetime as dt
import webbrowser


class Qwerty123(QMainWindow, Ui_Qwerty1234):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cnt_wrong_pass_inputed = 0
        self.stackedWidget.setCurrentIndex(0)
        self.use_pass_btn.clicked.connect(self.use_pass)
        self.input_pass_1.returnPressed.connect(self.proverochka_na_slitogo_boticka_cheek)
        self.db = DatabaseManager()
        self.sec = SecurityManager()
        self.setCentralWidget(self.stackedWidget)
        self.master_data = self.db.get_master_password()

        if not self.master_data:
            self.input_pass_1.setPlaceholderText("Придумайте пароль")
            self.is_registration = True
        else:
            self.is_registration = False

    def proverochka_na_slitogo_boticka_cheek(self, n=None):
        if n is None:
            with open("proverka_na_slitogo_boticka.txt", "a+", encoding='utf-8') as f:
                print(f"Попытка входа/регистрации: {dt.datetime.now()}", file=f)
            return self.check_pass()
        else:
            if n == 1:
                with open("proverka_na_slitogo_boticka.txt", "a+", encoding='utf-8') as f:
                    print(f"Неверный пароль ({self.cnt_wrong_pass_inputed}): {dt.datetime.now()}", file=f)

    def change_page_smooth(self, target_index):
        self.opacity_effect = QGraphicsOpacityEffect(self.stackedWidget)
        self.stackedWidget.setGraphicsEffect(self.opacity_effect)

        self.animation_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation_out.setDuration(150)
        self.animation_out.setStartValue(1.0)
        self.animation_out.setEndValue(0.0)

        def on_fade_out_finished():
            self.stackedWidget.setCurrentIndex(target_index)

            self.animation_in = QPropertyAnimation(self.opacity_effect, b"opacity")
            self.animation_in.setDuration(150)
            self.animation_in.setStartValue(0.0)
            self.animation_in.setEndValue(1.0)
            self.animation_in.start()

        self.animation_out.finished.connect(on_fade_out_finished)
        self.animation_out.start()

    def use_pass(self):
        self.change_page_smooth(1)

    def check_pass(self):
        if self.is_registration:
            password = self.input_pass_1.text()
            if password:
                salt, ciphertext = self.sec.setup(password)
                self.db.save_master_password(salt, ciphertext)

                self.main_window = Qwerty123_m(self.db, self.sec, password)
                self.main_window.show()
                self.close()
        else:
            salt, ciphertext = self.master_data
            if self.sec.check_password(self.input_pass_1.text(), salt, ciphertext):
                self.main_window = Qwerty123_m(self.db, self.sec, self.input_pass_1.text())
                self.main_window.show()
                self.close()
            else:
                self.input_pass_1.setText("")
                self.input_pass_1.setPlaceholderText("Неверный пароль")
                self.cnt_wrong_pass_inputed += 1
                self.proverochka_na_slitogo_boticka_cheek(n=1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Qwerty123()
    ex.show()
    sys.exit(app.exec())
