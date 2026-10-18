import logging as log
import sys
from tkinter import messagebox

from app.paths import LOG_FILE, ensure_data_directories
from app.controller import Save_Password


def main():
    ensure_data_directories()
    log.basicConfig(
        filename=LOG_FILE,
        level=log.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    try:
        new = Save_Password()
        new.run_main_window()
    except Exception:
        log.exception("The application stopped unexpectedly")
        if getattr(sys, "frozen", False):
            messagebox.showerror(
                "Save Password",
                "The application could not continue. "
                f"See the log file for details:\n{LOG_FILE}",
            )
            return
        raise

if __name__ == "__main__":
    main()


