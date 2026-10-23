import sqlite3


class DatabaseManager:
    def __init__(self):
        self.con = sqlite3.connect("qwerty.db")
        self.cursor = self.con.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor = self.con.cursor()

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS accounts
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                service_name
                                TEXT
                                NOT
                                NULL,
                                login
                                TEXT
                                NOT
                                NULL,
                                encrypted_password
                                TEXT
                                NOT
                                NULL
                            )
                            """)

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS master_password
                            (
                                salt
                                BLOB,
                                ciphertext
                                BLOB
                            )
                            """)
        self.con.commit()

    def save_master_password(self,  salt, ciphertext):
        self.cursor.execute("DELETE FROM master_password")
        self.cursor.execute(
            """
            INSERT INTO master_password (salt, ciphertext)
            VALUES (?, ?)
            """,
            (salt, ciphertext),
        )
        self.con.commit()

    def add_account(self, login, encrypted_password):
        self.cursor.execute(
            """
            INSERT INTO accounts (service_name, login, encrypted_password)
            VALUES (?, ?, ?)
            """,
            (login, encrypted_password),
        )
        self.con.commit()

    def get_all_accounts(self):
        self.cursor.execute("SELECT * FROM accounts")
        return self.cursor.fetchall()

    def get_master_password(self):
        self.cursor.execute('SELECT salt, ciphertext FROM master_password')
        return self.cursor.fetchone()
