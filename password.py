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
        if level == 3:
            if secrets.choice([True, False]):
                return ''.join(secrets.choice(self.digits) for _ in range(8))
            else:
                return ''.join(secrets.choice(self.lowercase) for _ in range(8))

        elif level == 2:
            alphabet = self.uppercase + self.lowercase + self.digits
            return ''.join(secrets.choice(alphabet) for _ in range(10))

        elif level == 1:
            alphabet = self.uppercase + self.lowercase + self.digits + string.punctuation
            return ''.join(secrets.choice(alphabet) for _ in range(12))

        return ''.join(secrets.choice(self.lowercase) for _ in range(8))
