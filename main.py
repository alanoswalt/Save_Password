from tkinter import *
import sqlite3
import sys



class main_window:

    def __init__(self) -> None:
        #root = Tk()
        #root.title('Save Passwords')
        #root.geometry("400x200")

        #Database variables
        self.name_of_db = "password_db.db"
        self.name_of_table = "password_table"
        self.create_or_connect_dbs(self.name_of_table)

        self.gui_main_page = '''
                        
                        Enter a number
                        1. Add entry
                        2. Print table
                        3. Delete entry
                        4. Close app
                    '''

        self.db_insert = f'''INSERT INTO '{self.name_of_table}'(account, user_email, password) VALUES (?, ?, ?)'''
        self.db_delete = f'''DELETE from '{self.name_of_table}' WHERE account = ?'''
        #root.mainloop()

    def create_or_connect_dbs(self, table_name):
        conection = sqlite3.connect(self.name_of_db)
        cursor = conection.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        result = cursor.fetchall()

        if result:
            print(f"The table '{table_name}' exists.")
        else:
            print(f"The table '{table_name}' does not exist. Creating it now...")
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (account TEXT, user_email TEXT, password TEXT)")
            conection.commit()
        conection.close()
        print(result)

    def query(self):

        connection = sqlite3.connect("password_db.db")
        #connection.row_factory = sqlite3.Row #This returns the data as a dictionary

        #Create a cursur, like a pointer, does stuff
        cursor = connection.cursor()

        #Query Data base
        cursor.execute("SELECT * FROM password_table")
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
        print(self.db_insert)
        cursor.execute(self.db_insert, (account, user_email, password))

        #To commit the changes
        conection.commit()

        #Close the connection to data base
        conection.close()

    def delete(self, account):
            #This needs to happend again inside the function
        connection = sqlite3.connect("password_db.db")

        #Create a cursur, like a pointer, does stuff
        cursor = connection.cursor()

        #Insert in tablee
        cursor.execute(self.db_delete, (account,))

        #To commit the changes
        connection.commit()

        #Close the connection to data base
        connection.close()

    def gui(self):

        print(self.gui_main_page)
        user_input = input("Please enter your answer: ")

        if user_input == '1':
            account = input("Please enter the accoun: ")
            user_email = input("Please enter your user: ")
            password = input("Please enter your password: ")
            self.submit(account, user_email, password)

        elif user_input == '2':
            self.query()

        elif user_input == '3':
            account = input("Please enter the account to delete: ")
            self.delete(account)
            print("Record deleted")
            self.query()

        elif user_input == '4':
            sys.exit()   

def main():
    new = main_window()

    while True:
        new.gui()




if __name__ == "__main__":
    main()


