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
        self.db_delete = f'''DELETE from '{self.name_of_table}' WHERE account = ?'''
        self.db_update = f'''UPDATE '{self.name_of_table}' SET user_email = ?, password = ? WHERE account = ?'''
        self.db_query = f'''SELECT * FROM '{self.name_of_table}' '''
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
        conection = sqlite3.connect(self.name_of_db)
        cursor = conection.cursor()
        cursor.execute(self.db_connect)
        result = cursor.fetchall()

        if result:
            log.info(f"The table '{self.name_of_table}' exists.")
        else:
            log.warning(f"The table '{self.name_of_table}' does not exist. Creating it now...")
            cursor.execute(self.db_create)
            conection.commit()
        conection.close()

    def add_new_user(self, user_email, password):
        print("Conecting to DB..")
        conection = sqlite3.connect(self.name_of_db)
        cursor = conection.cursor()

        #account = self.encoder.encode(account)
        #user_email = self.user_encoder.encode(user_email)
        print("Encoding information")
        password = self.user_encoder.encode(password)

        #Insert in tablee
        cursor.execute(self.db_insert, (user_email, password))

        #To commit the changes
        conection.commit()

        #Close the connection to data base
        conection.close()
   
    def look_for_user(self, user_email):
        # Connect to the SQLite database
        connection = sqlite3.connect(self.name_of_db)
        cursor = connection.cursor()
        
        # Execute the query
        cursor.execute(self.check_query, (user_email,))
        
        # Fetch one result
        result = cursor.fetchone()
        log.info(result)
        
        if result is not None:
            # User exists
            connection.close()
            log.info(f"User {user_email} already exists in the table {self.name_of_table}.")
            return True
        else:
            # User does not exist, insert the user
            connection.close()
            log.info(f"User {user_email} doesn't exists in the table {self.name_of_table}.")
            return False
        
    def compare_password(self, user_email, password):

        conection = sqlite3.connect(self.name_of_db)
        cursor = conection.cursor()

        log.info("|---------------------------------------------|")
        print("Retriving data")

        cursor.execute(self.retrive_password, (user_email,))
        encrypt_password = cursor.fetchone()[0]
        decrypt_password = self.user_encoder.decode(encrypt_password)

        log.info(cursor.fetchone())

        correct_password = True

        #print(encrypt_password)
        #print(decrypt_password)

        if decrypt_password == password:
            log.info("This is a correct password")
        else:
            log.warning("This isn't a correct password")
            correct_password = False

        #To commit the changes
        conection.commit()

        #Close the connection to data base
        conection.close()
        return correct_password
