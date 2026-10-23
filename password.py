import base64
import os
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import random


class SecurityManager:
    def __init__(self):
        self.key = None
        self.lowercase = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        ]
        self.uppercase = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]
        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def generate_key(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def setup(self, password):
        self.salt = os.urandom(16)
        self.key = self.generate_key(password, self.salt)
        f = Fernet(self.key)

        ciphertext = f.encrypt(b"VALID_MASTER_PASSWORD")
        return self.salt, ciphertext

    def check_password(self, password, salt, ciphertext):
        try:
            key = self.generate_key(password, salt)
            f = Fernet(key)
            f.decrypt(ciphertext)
            self.key = key
            return True
        except InvalidToken:
            return False

    def decoding(self, password_sql, salt):
        if not self.key:
            raise ValueError("Ключ шифрования не задан!")
        f = Fernet(self.key)
        return f.decrypt(password_sql).decode()

    def encode(self, password_sql, salt):
        if not self.key:
            raise ValueError("Ключ шифрования не задан!")
        f = Fernet(self.key)
        return f.encrypt(password_sql.encode())

    def generate_pass(self, level=1):
        if level == 1:
            data = []

            for _ in range(3):
                f = ''
                for _ in range(6):
                    f += random.choice(self.uppercase + self.digits + self.lowercase)
                data.append(f)
            return "-".join(data)

        if level == 2:
            data = []
            for _ in range(2):
                f = ''
                for _ in range(6):
                    f += random.choice(self.digits + self.lowercase)
                data.append(f)
            return "-".join(data)
        if level == 3:
            f = ''
            for _ in range(8):
                rand = random.randint(0, 1)
                if rand == 1:
                    f += random.choice(self.digits)
                else:
                    f += random.choice(self.lowercase)
            return f
