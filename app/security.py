from cryptography.fernet import Fernet
from passlib.context import CryptContext

from app import config


class Cryptographer:
    def __init__(self):
        self.cryptographer = Fernet(config.ENCRYPT_KEY)

    def encrypt(self, value: str):
        value = value.encode('utf-8')
        return self.cryptographer.encrypt(value)

    def decrypt(self, value: str):
        value = self.cryptographer.decrypt(value)
        return value.decode('utf-8')


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


