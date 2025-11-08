
import sys
from database.user_db import user_database

class main_window:

    def __init__(self, user_app) -> None:
        #root = Tk()
        #root.title('Save Passwords')
        #root.geometry("400x200")

        #Database variables
        self.user_app = user_app
        self.gui_main_page = f'''
                Welcome {self.user_app}
                Enter a number
                1. Add entry
                2. Print table
                3. Delete entry
                4. Update entry
                5. Close app
            '''
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