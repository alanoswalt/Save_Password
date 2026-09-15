import sqlite3

import pytest
from cryptography.fernet import Fernet

from database.user_db import user_database


@pytest.fixture
def user_database_instance(tmp_path):
    return user_database(
        "test_user",
        Fernet.generate_key(),
        db_path=str(tmp_path / "user.db"),
    )


@pytest.mark.user_database
def test_database_is_created(user_database_instance):
    assert user_database_instance.name_of_db

    with sqlite3.connect(user_database_instance.name_of_db) as connection:
        table = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='password_table'"
        ).fetchone()

    assert table == ("password_table",)


@pytest.mark.user_database
def test_submit(user_database_instance):
    user_database_instance.submit("test_account", "test_username", "test_password")

    with sqlite3.connect(user_database_instance.name_of_db) as connection:
        result = connection.execute(
            "SELECT account FROM password_table WHERE account = ?",
            ("test_account",),
        ).fetchone()

    assert result == ("test_account",)


@pytest.mark.user_database
def test_update(user_database_instance):
    user_database_instance.submit("account", "old_user", "old_password")
    user_database_instance.update("account", "new_user", "new_password")

    with sqlite3.connect(user_database_instance.name_of_db) as connection:
        encrypted_user = connection.execute(
            "SELECT user_email FROM password_table WHERE account = ?",
            ("account",),
        ).fetchone()[0]

    assert user_database_instance.encoder.decode(encrypted_user) == "new_user"


@pytest.mark.user_database
def test_get_password(user_database_instance):
    user_database_instance.submit("account", "user", "secret-password")

    assert user_database_instance.get_password("account") == "secret-password"


@pytest.mark.user_database
def test_delete(user_database_instance):
    user_database_instance.submit("account", "user", "password")
    user_database_instance.delete("account")

    with sqlite3.connect(user_database_instance.name_of_db) as connection:
        result = connection.execute(
            "SELECT account FROM password_table WHERE account = ?",
            ("account",),
        ).fetchone()

    assert result is None
