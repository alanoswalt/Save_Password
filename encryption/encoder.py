import base64
import os

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


class InvalidMasterPassword(ValueError):
    """Raised when a master password cannot unlock a user's vault."""


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible key from a master password and salt."""
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    derived_key = kdf.derive(password.encode("utf-8"))
    return base64.urlsafe_b64encode(derived_key)


def create_vault(password: str) -> tuple[bytes, bytes, bytes]:
    """Create salt, encrypted vault key, and the in-memory vault key."""
    salt = os.urandom(16)
    derived_key = derive_key(password, salt)
    vault_key = Fernet.generate_key()
    encrypted_vault_key = Fernet(derived_key).encrypt(vault_key)
    return salt, encrypted_vault_key, vault_key


def unlock_vault(password: str, salt: bytes, encrypted_vault_key: bytes) -> bytes:
    """Unlock and return a vault key using the master password."""
    derived_key = derive_key(password, salt)
    try:
        return Fernet(derived_key).decrypt(encrypted_vault_key)
    except InvalidToken as exc:
        raise InvalidMasterPassword("Incorrect master password") from exc


class vault_encoder:
    """Encrypt and decrypt vault fields using an unlocked vault key."""

    def __init__(self, vault_key: bytes) -> None:
        self.fernet = Fernet(vault_key)

    def encode(self, field: str) -> bytes:
        return self.fernet.encrypt(field.encode("utf-8"))

    def decode(self, encrypted_field: bytes) -> str:
        return self.fernet.decrypt(encrypted_field).decode("utf-8")
