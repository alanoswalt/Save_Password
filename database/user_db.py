import os
import sqlite3

from encryption.encoder import vault_encoder


class user_database:
    def __init__(self, name_of_db, vault_key, db_path=None) -> None:
        self.name_of_db = db_path or os.path.join("data", "users", f"{name_of_db}.db")
        self.name_of_table = "password_table"
        self.db_insert = (
            f"INSERT INTO {self.name_of_table} "
            "(account, user_email, password) VALUES (?, ?, ?)"
        )
        self.db_delete = f"DELETE FROM {self.name_of_table} WHERE account = ?"
        self.db_update = (
            f"UPDATE {self.name_of_table} SET user_email = ?, password = ? "
            "WHERE account = ?"
        )
        self.db_connect = (
            "SELECT name FROM sqlite_master "
            f"WHERE type='table' AND name='{self.name_of_table}'"
        )
        self.db_create = f"""
            CREATE TABLE IF NOT EXISTS {self.name_of_table} (
                account TEXT PRIMARY KEY,
                user_email BLOB NOT NULL,
                password BLOB NOT NULL
            )
        """
        self.encoder = vault_encoder(vault_key)
        self.create_or_connect_dbs()

    def create_or_connect_dbs(self):
        os.makedirs(os.path.dirname(self.name_of_db) or ".", exist_ok=True)
        try:
            with sqlite3.connect(self.name_of_db) as connection:
                if not connection.execute(self.db_connect).fetchone():
                    connection.execute(self.db_create)
                    return

                columns = {
                    row[1]: row for row in connection.execute(
                        f"PRAGMA table_info({self.name_of_table})"
                    )
                }
                if not columns.get("account", (None, None, None, None, None, 0))[5]:
                    raise RuntimeError(
                        "The existing vault database uses the old key format. "
                        "Back it up and create a new vault database."
                    )
        except sqlite3.Error as exc:
            raise RuntimeError(f"Could not initialize database '{self.name_of_db}'") from exc

    def query(self):
        for account, user_email in self.list_entries():
            print(f"Account: {account}, User: {user_email}, Password: [hidden]")

    def list_entries(self):
        try:
            with sqlite3.connect(self.name_of_db) as connection:
                encrypted_records = connection.execute(
                    f"SELECT account, user_email, password FROM {self.name_of_table}"
                ).fetchall()

            return [
                (account, self.encoder.decode(encrypted_user))
                for account, encrypted_user, _encrypted_password in encrypted_records
            ]
        except sqlite3.Error as exc:
            raise RuntimeError("Could not read password records") from exc

    def get_password(self, account):
        """Decrypt and return one password for an authenticated vault user."""
        try:
            with sqlite3.connect(self.name_of_db) as connection:
                record = connection.execute(
                    f"SELECT password FROM {self.name_of_table} WHERE account = ?",
                    (account,),
                ).fetchone()
        except sqlite3.Error as exc:
            raise RuntimeError("Could not retrieve password") from exc

        if record is None:
            return None
        return self.encoder.decode(record[0])

    def submit(self, account, user_email, password):
        try:
            with sqlite3.connect(self.name_of_db) as connection:
                connection.execute(
                    self.db_insert,
                    (
                        account,
                        self.encoder.encode(user_email),
                        self.encoder.encode(password),
                    ),
                )
        except sqlite3.IntegrityError as exc:
            raise ValueError("Account already exists") from exc
        except sqlite3.Error as exc:
            raise RuntimeError("Could not save password record") from exc

    def delete(self, account):
        try:
            with sqlite3.connect(self.name_of_db) as connection:
                connection.execute(self.db_delete, (account,))
        except sqlite3.Error as exc:
            raise RuntimeError("Could not delete password record") from exc

    def update(self, account, user_email, password):
        try:
            with sqlite3.connect(self.name_of_db) as connection:
                connection.execute(
                    self.db_update,
                    (self.encoder.encode(user_email), self.encoder.encode(password), account),
                )
        except sqlite3.Error as exc:
            raise RuntimeError("Could not update password record") from exc
