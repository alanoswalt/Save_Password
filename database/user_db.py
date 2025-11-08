import sqlite3
import os
from encryption.encoder import encode_decode

class user_database:
    def __init__(self, name_of_db) -> None:
        #root = Tk()
        #root.title('Save Passwords')
        #root.geometry("400x200")

        #Database variables
        self.name_of_db = os.path.join("data", "users", f"{name_of_db}.db")
        self.name_of_table = "password_table"

        self.db_insert = f'''INSERT INTO '{self.name_of_table}'(account, user_email, password) VALUES (?, ?, ?)'''
        self.db_delete = f'''DELETE from '{self.name_of_table}' WHERE account = ?'''
        self.db_update = f'''UPDATE '{self.name_of_table}' SET user_email = ?, password = ? WHERE account = ?'''
        self.db_query = f'''SELECT * FROM '{self.name_of_table}' '''

        self.db_connect = f'''SELECT name FROM sqlite_master WHERE type='table' AND name='{self.name_of_table}' '''

        self.db_create = f'''CREATE TABLE IF NOT EXISTS {self.name_of_table} (account TEXT, user_email TEXT, password TEXT)'''

        #Have an ecoder for the database
        self.encoder = encode_decode(name_of_db)

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
        user_email = self.encoder.encode(user_email)
        password = self.encoder.encode(password)

        cur.execute(self.db_update, (user_email, password, account))

        #To commit the changes
        connection.commit()

        #Close the connection to data base
        connection.close()