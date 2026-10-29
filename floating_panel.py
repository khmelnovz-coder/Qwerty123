from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6 import QtGui


class FloatingPanel(QWidget):
    def __init__(self, security_manager):
        super().__init__()
        self.sec = security_manager

        self.setWindowTitle("Быстрый доступ")
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.resize(300, 180)

        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto;
                font-size: 13px;
            }
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005999;
            }
            QLineEdit {
                background-color: #3c3f41;
                color: white;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px;
            }
        """)

        layout = QVBoxLayout()

        self.label = QLabel("Быстрый генератор паролей")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.pass_input = QLineEdit()
        self.pass_input.setReadOnly(True)
        layout.addWidget(self.pass_input)

        self.gen_btn = QPushButton("Сгенерировать пароль")
        self.gen_btn.clicked.connect(self.generate_new)
        layout.addWidget(self.gen_btn)

        self.copy_btn = QPushButton("Скопировать")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_btn)

        self.setLayout(layout)
        self.generate_new()

    def generate_new(self):
        try:
            new_pass = self.sec.generate_pass(1)
            self.pass_input.setText(new_pass)
        except Exception as e:
            self.pass_input.setText("Ошибка генерации")

    def copy_to_clipboard(self):
        text = self.pass_input.text()
        if text:
            QtGui.QGuiApplication.clipboard().setText(text)
            self.gen_btn.setText("Скопировано!")
            QTimer.singleShot(1500, lambda: self.gen_btn.setText("Сгенерировать пароль"))
