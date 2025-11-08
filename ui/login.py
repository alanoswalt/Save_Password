
import sys
import logging as log
from database.all_users_db import all_users_database


class login_window:
    def __init__(self) -> None:
        self.gui_login_page ='''
                
                Enter a number
                1. Log in
                2. Sing Up
                3. Exit
            '''        
        self.user_name_app = ""
        self.valid_user_in_database = False
        self.user_db = all_users_database("all_user")
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
            for i in range(2):
                user_exists = self.user_db.look_for_user(user_email)
                if user_exists:
                    log.info("User exist, comparing password")
                    correct_password = self.user_db.compare_password(user_email, password)
                    
                    if not correct_password:
                        print("Provide correct credentials")
                        user_email = input("Please enter your user: ")
                        password = input("Please enter your password: ")
                    else:
                        break
                        
                else:
                    print("User doesn't exists, create one?")
                    question_create_one = input("Please enter your answer: yes/no")
                    if question_create_one.lower().strip() == "yes":
                        log.info("Adding new user")
                        self.user_db.add_new_user(user_email, password)
                        break
                    else:
                        print("Login with correct user")
                        sys.exit()

            else:
                print('Closing app please provide correct input')
                sys.exit()
                

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