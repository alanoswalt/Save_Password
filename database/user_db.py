import sqlite3
import os
from encryption.encoder import encode_decode

class user_database:
    def __init__(self, name_of_db, db_path=None, key_path=None) -> None:
        #root = Tk()
        #root.title('Save Passwords')
        #root.geometry("400x200")

        #Database variables
        self.name_of_db = db_path or os.path.join("data", "users", f"{name_of_db}.db")
        self.name_of_table = "password_table"

        self.db_insert = f'''INSERT INTO '{self.name_of_table}'(account, user_email, password) VALUES (?, ?, ?)'''
        self.db_delete = f'''DELETE from '{self.name_of_table}' WHERE account = ?'''
        self.db_update = f'''UPDATE '{self.name_of_table}' SET user_email = ?, password = ? WHERE account = ?'''
        self.db_query = f'''SELECT * FROM '{self.name_of_table}' '''

        self.db_connect = f'''SELECT name FROM sqlite_master WHERE type='table' AND name='{self.name_of_table}' '''

        self.db_create = f'''CREATE TABLE IF NOT EXISTS {self.name_of_table} (account TEXT, user_email TEXT, password TEXT)'''

        #Have an ecoder for the database
        self.encoder = encode_decode(name_of_db, key_path=key_path)

        #Call function to connect to DB
        self.create_or_connect_dbs()

        #root.mainloop()

    def create_or_connect_dbs(self):
        os.makedirs(os.path.dirname(self.name_of_db) or ".", exist_ok=True)
        try:
            with sqlite3.connect(self.name_of_db) as connection:
                cursor = connection.cursor()
                cursor.execute(self.db_connect)
                result = cursor.fetchone()

                if result:
                    print(f"The table '{self.name_of_table}' exists.")
                else:
                    print(f"The table '{self.name_of_table}' does not exist. Creating it now...")
                    cursor.execute(self.db_create)
        except sqlite3.Error as exc:
            raise RuntimeError(f"Could not initialize database '{self.name_of_db}'") from exc

    def query(self):

        try:
            with sqlite3.connect(self.name_of_db) as connection:
                records = connection.execute(self.db_query).fetchall()

            for record in records:
                record0 = record[0]
                record1 = self.encoder.decode(record[1])
                record2 = self.encoder.decode(record[2])
                print(f"{record0}, {record1}, {record2}")
        except sqlite3.Error as exc:
            raise RuntimeError("Could not read password records") from exc

    def submit(self, account, user_email, password):

        try:
            user_email = self.encoder.encode(user_email)
            password = self.encoder.encode(password)
            with sqlite3.connect(self.name_of_db) as connection:
                connection.execute(self.db_insert, (account, user_email, password))
        except sqlite3.Error as exc:
            raise RuntimeError("Could not save password record") from exc

    def delete(self, account):
            #This needs to happend again inside the function
        try:
            with sqlite3.connect(self.name_of_db) as connection:
                connection.execute(self.db_delete, (account,))
        except sqlite3.Error as exc:
            raise RuntimeError("Could not delete password record") from exc

    def update(self, account, user_email, password):

        #This needs to happend again inside the function
        try:
            user_email = self.encoder.encode(user_email)
            password = self.encoder.encode(password)
            with sqlite3.connect(self.name_of_db) as connection:
                connection.execute(self.db_update, (user_email, password, account))
        except sqlite3.Error as exc:
            raise RuntimeError("Could not update password record") from exc
