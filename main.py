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
                        2. Delete entry
                        3. Update entry
                        4. Close app
                    '''

        self.db_insert = f'''INSERT INTO '{self.name_of_table}'(account, user_email, password) VALUES (?, ?, ?)'''
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
    
 
    def gui(self):

        print(self.gui_main_page)
        user_input = input("Please enter your answer: ")

        if user_input == '1':
            account = input("Please enter the accoun: ")
            user_email = input("Please enter your user: ")
            password = input("Please enter your password: ")
            self.submit(account, user_email, password)

        elif user_input == '4':
            sys.exit()   
    
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





def main():
    new = main_window()

    while True:
        new.gui()




if __name__ == "__main__":
    main()


