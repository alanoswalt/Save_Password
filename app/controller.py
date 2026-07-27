
from ui.login import login_window
from ui.main_menu import main_window


class Save_Password:
    def __init__(self) -> None:
        self.login_window_object = login_window()
        self.name_of_user = self.login_window_object.gui()
        self.main_window_object = main_window(self.name_of_user)

    def run_main_window(self):
        while True:
            self.main_window_object.gui()
