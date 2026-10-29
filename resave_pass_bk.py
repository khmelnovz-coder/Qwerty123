from PyQt6.QtWidgets import QMainWindow
from ui.resave_pass_frontend import Ui_resave_pass


class ResavePassWindow(QMainWindow, Ui_resave_pass):
    def __init__(self, security_manager, database_manager, account_data, master_key, on_account_updated=None,
                 on_category_added=None):
        super().__init__()
        self.setupUi(self)
        self.sec = security_manager
        self.db = database_manager
        self.acc_data = account_data
        self.master_key = master_key
        self.on_account_updated = on_account_updated
        self.on_category_added = on_category_added

        self.load_categories_to_combo()

        self.populate_fields()

        self.cancel.clicked.connect(self.cancel_action)
        self.save_new_pass.clicked.connect(self.save_edited_pass_def)

        self.level_1.setChecked(True)
        self.current_level = 1
        self.level_1.toggled.connect(self.cr_new_pass_def)
        self.level_2.toggled.connect(self.cr_new_pass_def)
        self.level_3.toggled.connect(self.cr_new_pass_def)

    def load_categories_to_combo(self):
        self.categories.clear()
        cats = self.db.get_all_categories()
        for cat_id, cat_name in cats:
            self.categories.addItem(str(cat_name), cat_id)

    def populate_fields(self):
        if not self.acc_data:
            return

        acc_id, service_name, login, encrypted_pass, website, category_id = self.acc_data[:6]

        self.title_add.setText(str(service_name))
        self.login_add.setText(str(login))

        try:
            decrypted_pass = self.sec.decoding(encrypted_pass, self.master_key)
            self.pass_add.setText(decrypted_pass)
        except Exception:
            self.pass_add.setText("")

        self.site_add.setText(str(website) if website else "")

        index = self.categories.findData(category_id)
        if index >= 0:
            self.categories.setCurrentIndex(index)

    def cancel_action(self):
        self.close()

    def save_edited_pass_def(self):
        try:
            acc_id = self.acc_data[0]
            service_name = self.title_add.text()
            login = self.login_add.text()
            plain_pass = self.pass_add.text()
            website = self.site_add.text()
            category_id = self.categories.currentData()

            encrypted_pass = self.sec.encode(plain_pass)

            self.db.resave(acc_id, service_name, login, encrypted_pass, website, category_id)

            self.on_account_updated()

            self.close()
        except Exception as e:
            print(f"Ошибка при сохранении измененной записи: {e}")

    def cr_new_pass_def(self):
        if self.level_1.isChecked():
            self.current_level = 1
        elif self.level_2.isChecked():
            self.current_level = 2
        elif self.level_3.isChecked():
            self.current_level = 3

        try:
            new_pass = self.sec.generate_pass(self.current_level)
            self.pass_add.setText(new_pass)
        except Exception as e:
            print(f"Ошибка генерации пароля: {e}")
