import logging as log
from app.controller import Save_Password

def main():
    log.basicConfig(level=log.DEBUG) #How to move this later
    new = Save_Password()
    new.run_main_window()

if __name__ == "__main__":
    main()


