import sqlite3


class DatabaseManager:
    def __init__(self, db_name="qwerty.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

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

    def save_master_password(self, salt, ciphertext):
        self.cursor.execute('DELETE FROM master')
        self.cursor.execute('INSERT INTO master (salt, ciphertext) VALUES (?, ?)', (salt, ciphertext))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def get_all_accounts(self):
        self.cursor.execute('SELECT id, service, login, password FROM accounts')
        return self.cursor.fetchall()

    def add_account(self, service, login, encrypted_password, website):
        self.cursor.execute(
            'INSERT INTO accounts (service, login, password, website) VALUES (?, ?, ?, ?)',
            (service, login, encrypted_password, website)
        )
        self.conn.commit()

    def get_master_password(self):
        self.cursor.execute('SELECT salt, ciphertext FROM master')
        return self.cursor.fetchone()
