from tkinter import *
import sqlite3
import sys
import os
import logging as log
from cryptography.fernet import Fernet

class encode_decode:
    def __init__(self, name_of_key) -> None:
        self.file_path = f"{name_of_key}.txt"
        self.key = ""
        self.check_or_create_key()

    def encode(self, field):
        fernet = Fernet(self.key)
        encrypted_field = fernet.encrypt(field.encode())
        #print(f"Password saved: {encrypted_field}")
        return encrypted_field

    def decode(self, encrypted_field):
        fernet = Fernet(self.key)
        decrypted_field = fernet.decrypt(encrypted_field).decode()    
        #print(f"Show password: {decrypted_field}")
        return decrypted_field

    def read_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            return None

    #Escribir la llave en texto, no en binario
    def write_key(self, file_path, data):
        log.info(f"File '{file_path}' does not exist. Creating it...")
        with open(file_path, 'w') as file:
            file.write(data.decode())
        log.info(f"File '{file_path}' created with initial data:\n{self.key}") #La imprime en binario

    #Crea la llave en binario
    def create_new_key(self):
        log.info("Creating key")
        key = Fernet.generate_key()
        return key

    def check_or_create_key(self):
         # Check if the file exists
        if os.path.exists(self.file_path):
            self.key = self.read_file(self.file_path).encode()
            if self.key:
                log.info(f"File '{self.file_path}' exists and contains:\n{self.key}")
            else:
                log.warning(f"File '{self.file_path}' exists but is empty.")
        else:
            self.key = self.create_new_key()
            self.write_key(self.file_path, self.key)

class user_database:
    def __init__(self, name_of_db) -> None:
        #root = Tk()
        #root.title('Save Passwords')
        #root.geometry("400x200")

        #Database variables
        self.name_of_db = f"{name_of_db}.db"
        self.name_of_table = "password_table"

        self.db_insert = f'''INSERT INTO '{self.name_of_table}'(account, user_email, password) VALUES (?, ?, ?)'''
        self.db_delete = f'''DELETE from '{self.name_of_table}' WHERE account = ?'''
        self.db_update = f'''UPDATE '{self.name_of_table}' SET user_email = ?, password = ? WHERE account = ?'''
        self.db_query = f'''SELECT * FROM '{self.name_of_table}' '''

        self.db_connect = f'''SELECT name FROM sqlite_master WHERE type='table' AND name='{self.name_of_table}' '''

        self.db_create = f'''CREATE TABLE IF NOT EXISTS {self.name_of_table} (account TEXT, user_email TEXT, password TEXT)'''

        #Have an ecoder for the database
        self.encoder = encode_decode(self.name_of_db)

        #Call function to connect to DB
        self.create_or_connect_dbs()

        #root.mainloop()

    def create_or_connect_dbs(self):
        conection = sqlite3.connect(self.name_of_db)
        cursor = conection.cursor()
        cursor.execute(self.db_connect)
        result = cursor.fetchall()

        if result:
            print(f"The table '{self.name_of_table}' exists.")
        else:
            print(f"The table '{self.name_of_table}' does not exist. Creating it now...")
            cursor.execute(self.db_create)
            conection.commit()
        conection.close()
        print(result)

    def query(self):

        connection = sqlite3.connect(self.name_of_db)
        #connection.row_factory = sqlite3.Row #This returns the data as a dictionary

        #Create a cursur, like a pointer, does stuff
        cursor = connection.cursor()

        #Query Data base
        cursor.execute(self.db_query )
        records = cursor.fetchall()
        #records = cur.fetchone()
        #records = cur.fetchmany(2)

        for record in records:
            #print(f"All fileds are {record[0]}, {record[1]}, {record[2]}")
            print(record)
            record0=record[0]
            record1=self.encoder.decode(record[1])
            record2=self.encoder.decode(record[2])

            print(f"This are the filds {record0}, {record1}, {record2}")

        #To commit the changes
        connection.commit()

        #Close the connection to data base
        connection.close()
    
    def submit(self, account, user_email, password):

        conection = sqlite3.connect(self.name_of_db)
        cursor = conection.cursor()


        #account = self.encoder.encode(account)
        user_email = self.encoder.encode(user_email)
        password = self.encoder.encode(password)


        #Insert in tablee
        cursor.execute(self.db_insert, (account, user_email, password))

        #To commit the changes
        conection.commit()

        #Close the connection to data base
        conection.close()

    def delete(self, account):
            #This needs to happend again inside the function
        connection = sqlite3.connect(self.name_of_db)

        #Create a cursur, like a pointer, does stuff
        cursor = connection.cursor()
        #Insert in tablee
        cursor.execute(self.db_delete, (account,))

        #To commit the changes
        connection.commit()

        #Close the connection to data base
        connection.close()

    def update(self, account, user_email, password):

        #This needs to happend again inside the function
        connection = sqlite3.connect(self.name_of_db)

        #Create a cursur, like a pointer, does stuff
        cur = connection.cursor()

        #Insert in tablee

        cur.execute(self.db_update, (user_email, password, account))

        #To commit the changes
        connection.commit()

        #Close the connection to data base
        connection.close()

class main_window:

    def __init__(self, user_app) -> None:
        #root = Tk()
        #root.title('Save Passwords')
        #root.geometry("400x200")

        #Database variables
        self.gui_main_page = '''
                
                Enter a number
                1. Add entry
                2. Print table
                3. Delete entry
                4. Update entry
                5. Close app
            '''
        self.user_app = user_app
        self.data = user_database(self.user_app)

        #root.mainloop()

    def gui(self):

        print(self.gui_main_page)
        user_input = input("Please enter your answer: ")

        if user_input == '1':
            account = input("Please enter the account: ")
            user_email = input("Please enter your user: ")
            password = input("Please enter your password: ")
            self.data.submit(account, user_email, password)

        elif user_input == '2':
            self.data.query()

        elif user_input == '3':
            account = input("Please enter the account to delete: ")
            self.data.delete(account)
            print("Record deleted")
            self.data.query()

        elif user_input == '4':
            account = input("Please enter the account to update: ")
            user_email = input("Please enter your new user: ")
            password = input("Please enter your new password: ")
            self.data.update(account, user_email, password)
        
        elif user_input == '5':
            sys.exit()   

class all_users_database:
    def __init__(self) -> None:
        #Name of database and table
        self.name_of_db = "all_user.db"
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
        self.users_db_key = "all_users_key"
        self.user_encoder = encode_decode(self.users_db_key)

        #Call function to connect to DB
        self.create_or_connect_dbs()

        #root.mainloop()

    def create_or_connect_dbs(self):
        log.info("Conecting to dbs")
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

        log.indo("|---------------------------------------------|")
        print("Retriving data")

        cursor.execute(self.retrive_password, (user_email,))
        encrypt_password = cursor.fetchone()[0]
        decrypt_password = self.user_encoder.decode(encrypt_password)

        log.info(cursor.fetchone())

        #print(encrypt_password)
        #print(decrypt_password)

        if decrypt_password == password:
            log.info("This is a correct password")
        else:
            log.warning("This isn't a correct password")

        #To commit the changes
        conection.commit()

        #Close the connection to data base
        conection.close()

class login_window:
    def __init__(self) -> None:
        self.gui_login_page = '''
                
                Enter a number
                1. Log in
                2. Sing Up
                3. Exit
            '''        
        self.user_name_app = ""
        self.valid_user_in_database = False
        self.user_db = all_users_database()
        self.gui()

    def gui(self):
        '''
        user_input: Number to chose what to do
        user_email: user name
        password: password of account
        user_exists: True if account is in data base
        question_create_one: if account doesn't exists ask if you want to create one
        
        '''
        print(self.gui_login_page)
        user_input = input("Please enter your answer: ")
        user_email = input("Please enter your user: ")
        password = input("Please enter your password: ")
        
        if user_input == '1':
            log.info("Looking for user")
            user_exists = self.user_db.look_for_user(user_email)
            if user_exists:
                log.info("User exist, comparing password")
                self.user_db.compare_password(user_email, password)
                #FALTA PONER QUE PASA SI EL PASSWORD NO ESTA BIEN
            else:
                print("User doesn't exists, create one?")
                question_create_one = input("Please enter your answer: yes/no")
                if question_create_one.lower().strip() == "yes":
                    log.info("Adding new user")
                    self.user_db.add_new_user(user_email, password)
                else:
                    print("Login with correct user")

        elif user_input == '2':
            user_exists = self.user_db.look_for_user(user_email)
            if user_exists:
                print("User already exists, please login")
            else:
                print("User doesn't exists, create one")
                self.user_db.add_new_user(user_email, password)
        elif user_input == '3':
            sys.exit()
        self.user_name_app = user_email
        print(self.user_name_app)
    




class Save_Password:
    def __init__(self) -> None:
        self.login_window_object = login_window()
        self.name_of_user = self.login_window_object.user_name_app
        self.main_window_object = main_window(self.name_of_user)
        self.run_main_window()
    
    def run_main_window(self):
        while True:
            self.main_window_object.gui()






def main():
    log.basicConfig(level=log.DEBUG) #How to move this later
    new = Save_Password()
    new.run_main_window()

if __name__ == "__main__":
    main()


