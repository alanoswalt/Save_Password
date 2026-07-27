
import sys
import logging as log
from database.all_users_db import all_users_database


class login_window:
    def __init__(self) -> None:
        self.gui_login_page = '''
                Enter a number
                1. Log in
                2. Sign Up
                3. Exit
            '''        
        self.user_name_app = ""
        self.user_db = all_users_database("all_user")

    def gui(self):
        """Run the login menu until authentication succeeds or the user exits."""
        while True:
            print(self.gui_login_page)
            user_input = input("Please enter your answer: ").strip()

            # Exit before asking for credentials.
            if user_input == "3":
                print("Goodbye")
                sys.exit()

            if user_input not in {"1", "2"}:
                print("Invalid option. Please choose 1, 2, or 3.")
                continue

            user_email = input("Please enter your user: ").strip()
            password = input("Please enter your password: ")

            if not user_email or not password:
                print("User and password are required.")
                continue

            if user_input == "2":
                new_user = self._sign_up(user_email, password)
                if new_user:
                    return new_user
                continue

            if self._log_in(user_email, password):
                return self.user_name_app

    def _sign_up(self, user_email, password):
        if self.user_db.look_for_user(user_email):
            print("User already exists. Please log in.")
            return None

        log.info("Adding new user")
        self.user_db.add_new_user(user_email, password)
        print("Account created successfully.")
        self.user_name_app = user_email
        return self.user_name_app

    def _log_in(self, user_email, password):
        if not self.user_db.look_for_user(user_email):
            print("User does not exist. Please sign up first.")
            return False

        if self.user_db.compare_password(user_email, password):
            self.user_name_app = user_email
            return True

        print("Incorrect credentials.")
        return False
