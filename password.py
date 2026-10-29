import base64
import os
import secrets
import string
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class SecurityManager:
    def __init__(self):
        self.key = None
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits

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
        salt = os.urandom(16)
        key = self.generate_key(password, salt)
        self.key = key
        f = Fernet(key)
        ciphertext = f.encrypt(b"VALID_MASTER_PASSWORD")
        return salt, ciphertext

    def check_password(self, password, salt, ciphertext):
        try:
            key = self.generate_key(password, salt)
            f = Fernet(key)
            f.decrypt(ciphertext)
            self.key = key
            return True
        except InvalidToken:
            return False

    def decoding(self, password_sql, salt=None):
        if not self.key:
            raise ValueError("Ключ шифрования не задан!")
        f = Fernet(self.key)
        return f.decrypt(password_sql).decode()

    def encode(self, password_sql, salt=None):
        if not self.key:
            raise ValueError("Ключ шифрования не задан!")
        f = Fernet(self.key)
        return f.encrypt(password_sql.encode())

    def generate_pass(self, level=1):
        if level == 1:
            alphabet = self.uppercase + self.lowercase + self.digits

            part1 = []
            for _ in range(6):
                part1.append(secrets.choice(alphabet))
            p1 = "".join(part1)

            part2 = []
            for _ in range(6):
                part2.append(secrets.choice(alphabet))
            p2 = "".join(part2)

            part3 = []
            for _ in range(6):
                part3.append(secrets.choice(alphabet))
            p3 = "".join(part3)

            return f"{p1}-{p2}-{p3}"

        elif level == 2:
            alphabet = self.lowercase + self.digits

            part1 = []
            for _ in range(6):
                part1.append(secrets.choice(alphabet))
            p1 = "".join(part1)

            part2 = []
            for _ in range(6):
                part2.append(secrets.choice(alphabet))
            p2 = "".join(part2)

            return f"{p1}-{p2}"

        elif level == 3:
            length = 8
            chars = []

            if secrets.choice([True, False]):
                for _ in range(length):
                    chars.append(secrets.choice(self.digits))
            else:
                for _ in range(length):
                    chars.append(secrets.choice(self.lowercase))

            return "".join(chars)

        default_chars = []
        for _ in range(8):
            default_chars.append(secrets.choice(self.lowercase))
        return "".join(default_chars)



