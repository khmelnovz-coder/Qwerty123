import sqlite3
from PyQt6.QtWidgets import QMessageBox


class DatabaseManager:
    def __init__(self, db_name="qwerty.db"):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            self.create_tables()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Ошибка базы данных", f"Не удалось подключиться к БД:\n{e}")

    def create_tables(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS categories
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                name
                                TEXT
                                NOT
                                NULL
                            )
                            ''')

        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS master
                            (
                                salt
                                BLOB,
                                ciphertext
                                BLOB
                            )
                            ''')

        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS accounts
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                service_name
                                TEXT,
                                login
                                TEXT,
                                encrypted_pass
                                TEXT,
                                website
                                TEXT,
                                category_id
                                INTEGER
                                DEFAULT
                                1,
                                FOREIGN
                                KEY
                            (
                                category_id
                            ) REFERENCES categories
                            (
                                id
                            )
                                )
                            ''')
        default_categories = [
            (1, "Личные"),
            (2, "Работа"),
            (3, "Соцсети"),
            (4, "Другие")
        ]
        for cat_id, cat_name in default_categories:
            self.cursor.execute('''
                                INSERT
                                OR IGNORE INTO categories (id, name) VALUES (?, ?)
                                ''', (cat_id, cat_name))

        self.conn.commit()

    def get_all_categories(self):
        try:
            self.cursor.execute("SELECT id, name FROM categories")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка чтения данных: {e}")
            return []

    def save_master_password(self, salt, ciphertext):
        try:
            self.cursor.execute('DELETE FROM master')
            self.cursor.execute('INSERT INTO master (salt, ciphertext) VALUES (?, ?)', (salt, ciphertext))
            self.conn.commit()
        except sqlite3.Error as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка чтения данных: {e}")

    def add_category(self, name):
        try:
            self.cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка чтения данных: {e}")

    def close(self):
        try:
            self.conn.close()
        except sqlite3.Error as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка чтения данных: {e}")

    def get_all_accounts(self):
        try:
            self.cursor.execute('SELECT id, service_name, login, encrypted_pass, website, category_id FROM accounts')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка чтения данных: {e}")
            return []

    def add_account(self, service_name, login, encrypted_pass, website, category_id=1):
        try:
            self.cursor.execute('''
                                INSERT INTO accounts (service_name, login, encrypted_pass, website, category_id)
                                VALUES (?, ?, ?, ?, ?)
                                ''', (service_name, login, encrypted_pass, website, category_id))
            self.conn.commit()
        except sqlite3.Error as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка чтения данных: {e}")

    def get_master_password(self):
        try:
            self.cursor.execute('SELECT salt, ciphertext FROM master')
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка чтения данных: {e}")
            return []

    def sort_accounts_by_category(self, name):
        if name != "все":
            res = self.cursor.execute('''SELECT *
                                         FROM accounts
                                         WHERE category_id = (SELECT id FROM categories WHERE name = ?)''',
                                      (name,)).fetchall()

            return res

        else:
            res = self.get_all_accounts()
            return res

    def resave(self, acc_id, service_name, login, encrypted_pass, website, category_id):
        try:
            self.cursor.execute('''
                                UPDATE accounts
                                SET service_name   = ?,
                                    login          = ?,
                                    encrypted_pass = ?,
                                    website        = ?,
                                    category_id    = ?
                                WHERE id = ?
                                ''', (service_name, login, encrypted_pass, website, category_id, acc_id))
            self.conn.commit()
        except sqlite3.Error as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка обновления данных: {e}")
    def delete_account(self, acc_id):
        try:
            self.cursor.execute("DELETE FROM accounts WHERE id = ?", (acc_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка при удалении записи: {e}")

