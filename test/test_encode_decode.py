import pytest
from cryptography.fernet import Fernet

from encryption.encoder import (
    InvalidMasterPassword,
    create_vault,
    derive_key,
    unlock_vault,
    vault_encoder,
)


@pytest.mark.encode_decode
def test_vault_encrypts_and_decrypts():
    salt, encrypted_vault_key, vault_key = create_vault("master-password")
    encoder = vault_encoder(vault_key)

    encrypted_value = encoder.encode("Hello")

    assert encoder.decode(encrypted_value) == "Hello"
    assert encrypted_vault_key != vault_key
    assert len(salt) == 16


@pytest.mark.encode_decode
def test_master_password_unlocks_vault():
    salt, encrypted_vault_key, vault_key = create_vault("master-password")

    assert unlock_vault("master-password", salt, encrypted_vault_key) == vault_key


@pytest.mark.encode_decode
def test_wrong_master_password_cannot_unlock_vault():
    salt, encrypted_vault_key, _ = create_vault("master-password")

    with pytest.raises(InvalidMasterPassword):
        unlock_vault("wrong-password", salt, encrypted_vault_key)


@pytest.mark.encode_decode
def test_different_salts_derive_different_keys():
    assert derive_key("same-password", b"1" * 16) != derive_key(
        "same-password", b"2" * 16
    )
