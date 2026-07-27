import sqlite3
import logging as log
import os
from encryption.encoder import encode_decode

class all_users_database:
    def __init__(self, name_of_db="all_user", db_path=None, key_path=None) -> None:
        #Name of database and table
        self.name_of_db = db_path or os.path.join("data", "all_user.db")
        self.name_of_table = "all_user"


        #Sql commands
        self.db_insert = f'''INSERT INTO '{self.name_of_table}'(user_email, password) VALUES (?, ?)'''
        self.db_connect = f'''SELECT name FROM sqlite_master WHERE type='table' AND name='{self.name_of_table}' '''
        self.db_create = f'''CREATE TABLE IF NOT EXISTS {self.name_of_table} (user_email TEXT, password TEXT)'''
        self.check_query = f'''SELECT 1 FROM {self.name_of_table} WHERE user_email = ? LIMIT 1'''
        self.retrive_password = f'''SELECT password FROM {self.name_of_table} WHERE user_email = ?'''

        #Name of key file and create object of encoder for users
        self.users_db_key = f"{name_of_db}"
        self.user_encoder = encode_decode(self.users_db_key, key_path=key_path)

        #Call function to connect to DB
        self.create_or_connect_dbs()

        #root.mainloop()

    def create_or_connect_dbs(self):
        log.info("Conecting to dbs")
        os.makedirs(os.path.dirname(self.name_of_db) or ".", exist_ok=True)
        try:
            with sqlite3.connect(self.name_of_db) as connection:
                cursor = connection.cursor()
                cursor.execute(self.db_connect)
                result = cursor.fetchone()

                if result:
                    log.info(f"The table '{self.name_of_table}' exists.")
                else:
                    log.warning(f"The table '{self.name_of_table}' does not exist. Creating it now...")
                    cursor.execute(self.db_create)
        except sqlite3.Error as exc:
            log.exception("Could not initialize the users database")
            raise RuntimeError(f"Could not initialize database '{self.name_of_db}'") from exc

    def add_new_user(self, user_email, password):
        print("Conecting to DB..")
        try:
            password = self.user_encoder.encode(password)
            with sqlite3.connect(self.name_of_db) as connection:
                connection.execute(self.db_insert, (user_email, password))
        except sqlite3.Error as exc:
            log.exception("Could not add user '%s'", user_email)
            raise RuntimeError("Could not add user") from exc
   
    def look_for_user(self, user_email):
        # Connect to the SQLite database
        try:
            with sqlite3.connect(self.name_of_db) as connection:
                result = connection.execute(self.check_query, (user_email,)).fetchone()
        except sqlite3.Error as exc:
            log.exception("Could not look up user '%s'", user_email)
            raise RuntimeError("Could not look up user") from exc

        exists = result is not None
        log.info("User %s %s in the table %s.", user_email,
                 "already exists" if exists else "does not exist", self.name_of_table)
        return exists
        
    def compare_password(self, user_email, password):

        try:
            with sqlite3.connect(self.name_of_db) as connection:
                result = connection.execute(self.retrive_password, (user_email,)).fetchone()
        except sqlite3.Error as exc:
            log.exception("Could not retrieve password for '%s'", user_email)
            raise RuntimeError("Could not retrieve user password") from exc

        if result is None:
            return False

        try:
            return self.user_encoder.decode(result[0]) == password
        except Exception:
            log.exception("Could not decode password for '%s'", user_email)
            raise RuntimeError("Could not decode user password")
