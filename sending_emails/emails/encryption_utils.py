from cryptography.fernet import Fernet
from decouple import config

# Load encryption key from .env (must be 32 url-safe base64 bytes)
FERNET_KEY = config("OTP_FERNET_KEY").encode()
fernet = Fernet(FERNET_KEY)

def encrypt_data(data: str) -> str:
    """Encrypt sensitive data like OTP before sending through MQ."""
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt data when consuming from MQ."""
    return fernet.decrypt(encrypted_data.encode()).decode()
