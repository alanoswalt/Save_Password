import logging as log
import os
import sqlite3

from encryption.encoder import InvalidMasterPassword, create_vault, unlock_vault


class all_users_database:
    def __init__(self, name_of_db="all_user", db_path=None) -> None:
        self.name_of_db = db_path or os.path.join("data", "all_user.db")
        self.name_of_table = "all_user"
        self.db_insert = (
            f"INSERT INTO {self.name_of_table} "
            "(user_email, salt, encrypted_vault_key) VALUES (?, ?, ?)"
        )
        self.db_connect = (
            "SELECT name FROM sqlite_master "
            f"WHERE type='table' AND name='{self.name_of_table}'"
        )
        self.db_create = f"""
            CREATE TABLE IF NOT EXISTS {self.name_of_table} (
                user_email TEXT PRIMARY KEY,
                salt BLOB NOT NULL,
                encrypted_vault_key BLOB NOT NULL
            )
        """
        self.check_query = (
            f"SELECT 1 FROM {self.name_of_table} "
            "WHERE user_email = ? LIMIT 1"
        )
        self.user_query = (
            f"SELECT salt, encrypted_vault_key FROM {self.name_of_table} "
            "WHERE user_email = ?"
        )
        self.create_or_connect_dbs()

    def create_or_connect_dbs(self):
        os.makedirs(os.path.dirname(self.name_of_db) or ".", exist_ok=True)
        try:
            with sqlite3.connect(self.name_of_db) as connection:
                table_exists = connection.execute(self.db_connect).fetchone()
                if not table_exists:
                    connection.execute(self.db_create)
                    return

                columns = {
                    row[1]
                    for row in connection.execute(
                        f"PRAGMA table_info({self.name_of_table})"
                    )
                }
                required_columns = {
                    "user_email",
                    "salt",
                    "encrypted_vault_key",
                }
                if not required_columns.issubset(columns):
                    raise RuntimeError(
                        "The existing users database uses the old key format. "
                        "Back it up and create a new data database."
                    )
        except sqlite3.Error as exc:
            log.exception("Could not initialize the users database")
            raise RuntimeError(f"Could not initialize database '{self.name_of_db}'") from exc

    def add_new_user(self, user_email: str, password: str) -> bytes:
        salt, encrypted_vault_key, vault_key = create_vault(password)
        try:
            with sqlite3.connect(self.name_of_db) as connection:
                connection.execute(
                    self.db_insert,
                    (user_email, salt, encrypted_vault_key),
                )
        except sqlite3.IntegrityError as exc:
            raise ValueError("User already exists") from exc
        except sqlite3.Error as exc:
            log.exception("Could not add user")
            raise RuntimeError("Could not add user") from exc
        return vault_key

    def look_for_user(self, user_email: str) -> bool:
        try:
            with sqlite3.connect(self.name_of_db) as connection:
                result = connection.execute(self.check_query, (user_email,)).fetchone()
        except sqlite3.Error as exc:
            log.exception("Could not look up user")
            raise RuntimeError("Could not look up user") from exc
        return result is not None

    def unlock_user(self, user_email: str, password: str) -> bytes | None:
        try:
            with sqlite3.connect(self.name_of_db) as connection:
                result = connection.execute(self.user_query, (user_email,)).fetchone()
        except sqlite3.Error as exc:
            log.exception("Could not retrieve user vault")
            raise RuntimeError("Could not retrieve user vault") from exc

        if result is None:
            return None

        try:
            return unlock_vault(password, result[0], result[1])
        except InvalidMasterPassword:
            return None

    def compare_password(self, user_email: str, password: str) -> bool:
        return self.unlock_user(user_email, password) is not None
