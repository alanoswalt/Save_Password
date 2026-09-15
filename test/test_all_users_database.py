import sqlite3

import pytest

from database.all_users_db import all_users_database


@pytest.fixture
def users_database_instance(tmp_path):
    return all_users_database(
        db_path=str(tmp_path / "all_user.db"),
    )


@pytest.mark.users_database
def test_database_uses_new_vault_schema(users_database_instance):
    with sqlite3.connect(users_database_instance.name_of_db) as connection:
        columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(all_user)")
        }

    assert columns == {"user_email", "salt", "encrypted_vault_key"}


@pytest.mark.users_database
def test_add_user_and_unlock_vault(users_database_instance):
    vault_key = users_database_instance.add_new_user("test_username", "test_password")

    assert vault_key
    assert users_database_instance.look_for_user("test_username")
    assert users_database_instance.unlock_user("test_username", "test_password") == vault_key


@pytest.mark.users_database
def test_wrong_password_does_not_unlock_vault(users_database_instance):
    users_database_instance.add_new_user("test_username", "test_password")

    assert users_database_instance.unlock_user("test_username", "wrong") is None


@pytest.mark.users_database
def test_missing_user_is_not_found(users_database_instance):
    assert not users_database_instance.look_for_user("missing")
    assert users_database_instance.unlock_user("missing", "password") is None
