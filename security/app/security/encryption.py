import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

_key = os.getenv("FIELD_ENCRYPTION_KEY")
if not _key:
    raise RuntimeError("FIELD_ENCRYPTION_KEY not set in .env")

fernet = Fernet(_key.encode())

def encrypt_field(value: str) -> str:
    if value is None:
        return None
    return fernet.encrypt(value.encode()).decode()

def decrypt_field(token: str) -> str:
    if token is None:
        return None
    return fernet.decrypt(token.encode()).decode()