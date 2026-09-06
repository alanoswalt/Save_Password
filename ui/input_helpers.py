import os
from getpass import getpass


def read_password(prompt="Password: "):
    """Read a password across regular terminals and Git Bash on Windows.

    Git Bash's MinTTY terminal does not always work with Python's hidden
    password input. In that environment, fall back to normal input so the
    application remains usable. PowerShell and other terminals keep hidden
    password input.
    """
    if os.name == "nt" and os.environ.get("MSYSTEM"):
        print("Git Bash cannot hide password input; use PowerShell for hidden input.")
        return input(prompt)

    return getpass(prompt)
