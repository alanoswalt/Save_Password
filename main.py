from tkinter import *
import sqlite3
import sys
import os
from cryptography.fernet import Fernet

class database:
    def __init__(self) -> None:
        #root = Tk()
        #root.title('Save Passwords')
        #root.geometry("400x200")

        #Database variables
        self.name_of_db = "password_db.db"
        self.name_of_table = "password_table"

        self.db_insert = f'''INSERT INTO '{self.name_of_table}'(account, user_email, password) VALUES (?, ?, ?)'''
        self.db_delete = f'''DELETE from '{self.name_of_table}' WHERE account = ?'''
        self.db_update = f'''UPDATE '{self.name_of_table}' SET user_email = ?, password = ? WHERE account = ?'''
        self.db_query = f'''SELECT * FROM '{self.name_of_table}' '''

        self.db_connect = f'''SELECT name FROM sqlite_master WHERE type='table' AND name='{self.name_of_table}' '''

        self.db_create = f'''CREATE TABLE IF NOT EXISTS {self.name_of_table} (account TEXT, user_email TEXT, password TEXT)'''

        self.create_or_connect_dbs()

        #root.mainloop()

    def create_or_connect_dbs(self):
        conection = sqlite3.connect(self.name_of_db)
        cursor = conection.cursor()
        #cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        cursor.execute(self.db_connect)
        result = cursor.fetchall()

        if result:
            print(f"The table '{self.name_of_table}' exists.")
        else:
            print(f"The table '{self.name_of_table}' does not exist. Creating it now...")
            #cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (account TEXT, user_email TEXT, password TEXT)")
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
            print(record)
            #print_records += str(record[0]) + " " + str(record[1]) + "\n"

        #To commit the changes
        connection.commit()

        #Close the connection to data base
        connection.close()
    
    def submit(self, account, user_email, password):

        conection = sqlite3.connect(self.name_of_db)
        cursor = conection.cursor()

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

class encode_decode:
    def __init__(self) -> None:
        self.file_path = "my_file.txt"


        self.check_or_create_key()
        #self.decode()

    def decode(self):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        password = "hello"
        encrypted_password = fernet.encrypt(password.encode())
        decrypted_password = fernet.decrypt(encrypted_password).decode()
        print(f"Original password: {key}")
        print(f"Original password: {fernet}")
        print(f"Original password: {password}")
        print(f"Encrypted password: {encrypted_password}")
        print(f"Decrypted password: {decrypted_password}")

    def read_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            return None

    def write_key(self, file_path, data):
        with open(file_path, 'w') as file:
            file.write(data.decode())

    def create_new_key(self):
        key = Fernet.generate_key()
        return key

    def check_or_create_key(self):

         # Check if the file exists
        if os.path.exists(self.file_path):
            content = self.read_file(self.file_path)
            if content:
                print(f"File '{self.file_path}' exists and contains:\n{content}")
            else:
                print(f"File '{self.file_path}' exists but is empty.")
        else:
            print(f"File '{self.file_path}' does not exist. Creating it...")
            key = self.create_new_key()
            self.write_key(self.file_path, key)
            print(f"File '{self.file_path}' created with initial data:\n{key}")


class main_window:

    def __init__(self) -> None:
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
        self.data = database()

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


def main():
    #new = main_window()

    test = encode_decode()
    #while True:
    #    new.gui()

if __name__ == "__main__":
    main()


