from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt6.QtGui import QShortcut, QKeySequence
from ui.Qwerty_main_frontend import Ui_Qwerty_main
from password import SecurityManager
from add_pass_bk import Add_pass
from resave_pass_bk import ResavePassWindow
from floating_panel import FloatingPanel


class Qwerty123_m(QMainWindow, Ui_Qwerty_main):
    def __init__(self, db_manager, security_manager, master_key):
        super().__init__()
        self.db = db_manager
        self.sec = security_manager
        self.floating_window = None
        self.master_key = master_key
        self.setupUi(self)
        self.listWidget.itemClicked.connect(self.display_account_details)
        self.no_item = True
        self.update_button.clicked.connect(self.open_resave_window)
        self.delete_pass.clicked.connect(self.delete_pass_dialog)

        self.accounts = self.db.get_all_accounts()
        self.cr_new_pass.clicked.connect(self.create_pass)
        self.hide_details()
        self.menubar = self.menuBar()
        self.password.setReadOnly(True)
        self.password.setMouseTracking(True)
        self.password.installEventFilter(self)
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.init_category_menu()
        for field in (self.user, self.password, self.website):
            field.setReadOnly(True)
            field.setMouseTracking(True)
            field.installEventFilter(self)
        self.load_accounts()
        self.shortcut = QShortcut(QKeySequence("Ctrl+P"), self)
        self.shortcut.activated.connect(self.toggle_floating_panel)

    def init_category_menu(self):
        self.view_menu = self.menubar.addMenu("Вид")

        floating_action = self.view_menu.addAction("Плавающая панель (Ctrl+P)")
        floating_action.triggered.connect(self.toggle_floating_panel)
        self.view_menu.addSeparator()

        self.sort_menu = QtWidgets.QMenu("Сортировать по категориям", self)

        reset_action = self.sort_menu.addAction("Все категории")
        reset_action.triggered.connect(self.reset_category_filter)
        self.sort_menu.addSeparator()

        for i in self.db.get_all_categories():
            category_name = str(i[1])
            action = self.sort_menu.addAction(category_name)
            action.triggered.connect(lambda checked, name=category_name: self.sort_accounts_by_category(name))

        self.view_menu.addMenu(self.sort_menu)

    def toggle_floating_panel(self):
        if self.floating_window is not None and self.floating_window.isVisible():
            self.floating_window.close()
            self.floating_window = None
        else:
            self.floating_window = FloatingPanel(self.sec)
            self.floating_window.show()

    def init_category_menu(self):
        self.view_menu = self.menubar.addMenu("Вид")
        self.sort_menu = QtWidgets.QMenu("Сортировать по категориям", self)

        reset_action = self.sort_menu.addAction("Все категории")
        reset_action.triggered.connect(self.reset_category_filter)
        self.sort_menu.addSeparator()

        for i in self.db.get_all_categories():
            category_name = str(i[1])
            action = self.sort_menu.addAction(category_name)
            action.triggered.connect(lambda checked, name=category_name: self.sort_accounts_by_category(name))

        self.view_menu.addMenu(self.sort_menu)

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
        website = acc_data[4] if len(acc_data) > 4 else ""
        cat_id = acc_data[5] if len(acc_data) > 5 else 1

        self.db.cursor.execute("SELECT name FROM categories WHERE id = ?", (cat_id,))
        cat_result = self.db.cursor.fetchone()
        category_name = cat_result[0] if cat_result else "Без категории"
        self.no_item = False
        self.no_item_choosen.hide()
        self.title.setText(service_name)
        self.user.setText(login)
        self.password.setText(decrypted_pass)
        self.website.setText(website)
        self.current_categoriya.setText(category_name)
        self.show_details()

    def load_updated_accounts(self):
        self.accounts = self.db.get_all_accounts()
        self.load_accounts()

    def create_pass(self):
        self.add_pass = Add_pass(
            self.sec,
            self.db,
            on_account_added=self.load_updated_accounts,
            on_category_added=self.init_category_menu
        )
        self.add_pass.show()

    def update_load_catigories(self):
        self.view_menu = self.menubar.addMenu("Вид")
        self.sort_menu = QtWidgets.QMenu("Сортировать по категориям", self)

        reset_action = self.sort_menu.addAction("Все категории")
        reset_action.triggered.connect(self.reset_category_filter)
        self.sort_menu.addSeparator()

    def hide_details(self):
        self.title.hide()
        self.user.hide()
        self.password.hide()
        self.website.hide()
        self.label_6.hide()
        self.label_7.hide()
        self.label_8.hide()
        self.no_item_choosen.show()
        self.delete_pass.hide()
        self.update_button.hide()
        self.current_categoriya.hide()

    def show_details(self):
        self.title.show()
        self.user.show()
        self.password.show()
        self.website.show()
        self.label_6.show()
        self.label_7.show()
        self.label_8.show()
        self.no_item_choosen.hide()
        self.delete_pass.show()
        self.update_button.show()
        self.current_categoriya.show()

    def sort_accounts_by_category(self, name):
        self.accounts = self.db.sort_accounts_by_category(name)
        self.load_accounts()

    def reset_category_filter(self):
        self.accounts = self.db.get_all_accounts()
        self.load_accounts()

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

    def open_resave_window(self):
        selected_item = self.listWidget.currentItem()
        if not selected_item:
            self.statusbar.showMessage("Сначала выберите элемент для изменения!", 3000)
            return

        acc_data = selected_item.data(QtCore.Qt.ItemDataRole.UserRole)
        if not acc_data:
            return

        self.resave_window = ResavePassWindow(
            security_manager=self.sec,
            database_manager=self.db,
            account_data=acc_data,
            master_key=self.master_key,
            on_account_updated=self.load_updated_accounts
        )
        self.resave_window.show()

    def delete_pass_dialog(self):
        selected_item = self.listWidget.currentItem()
        if not selected_item:
            self.statusbar.showMessage("Сначала выберите элемент для удаления!", 3000)
            return

        acc_data = selected_item.data(QtCore.Qt.ItemDataRole.UserRole)
        if not acc_data:
            return

        acc_id = acc_data[0]
        service_name = acc_data[1]

        reply = QtWidgets.QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы действительно хотите удалить учетную запись «{service_name}»?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self.db.delete_account(acc_id)
            self.accounts = self.db.get_all_accounts()
            self.load_accounts()
            self.hide_details()
            self.statusbar.showMessage(f"Запись «{service_name}» успешно удалена.", 3000)
