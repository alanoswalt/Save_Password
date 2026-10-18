# Save Password

This is a local desktop password manager written in Python. It uses SQLite for
storage, Scrypt for master-password key derivation, and Fernet encryption for
saved credentials. The desktop interface uses CustomTkinter.

## Setup

From the repository directory, install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

On Bash/Linux/macOS, use:

```bash
python3 -m pip install -r requirements.txt
```

When running from source, the application creates its runtime directories and
files under the repository's `data/` directory. Test data is kept under
temporary pytest directories.

When running as a packaged Windows application, runtime data is stored in the
current Windows user's local application-data folder:

```text
%LOCALAPPDATA%\SavePassword\
```

This keeps each person's vault separate from the executable and avoids hard-
coded repository paths. The application creates this folder automatically.
The log is written to `save_password.log` in the same folder.

CustomTkinter is installed from `requirements.txt`; the source repository does
not need to be downloaded separately.

The application no longer stores Fernet keys in `data/keys/`. Instead, a
random vault key is encrypted with a key derived from the master password and
stored with the user's salt in the users database.

Existing databases created by an older version use the old key-file format and
are intentionally rejected. Back up the old `data/` directory before creating
a new vault. A migration tool can be added later to decrypt old records and
re-encrypt them using the new format.

## Run the application

```powershell
python main.py
```

On Bash/Linux/macOS:

```bash
python3 main.py
```

## Share the application with Windows users

The target computer does not need Python, the source repository, or the
project's virtual environment. Build the application on a Windows computer
with Python and the project dependencies installed, then share the complete
`dist\SavePassword` folder.

From PowerShell in the repository directory:

```powershell
python -m pip install -r requirements.txt
.\build.ps1
```

If PowerShell blocks local scripts, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\build.ps1
```

The executable will be created at:

```text
dist\SavePassword\SavePassword.exe
```

Send the whole `dist\SavePassword` folder as a ZIP file. The recipient can
extract it and double-click `SavePassword.exe`; Python is bundled inside the
build. Do not send only the `.exe`, because the `--onedir` build also needs its
support files.

To create a desktop shortcut, right-click `SavePassword.exe`, choose **Show
more options**, then **Send to > Desktop (create shortcut)**. The project
includes a shield-and-lock icon at `assets\save_password.ico`, and
`build.ps1` embeds it automatically. Its editable vector source is
`assets\save_password.svg`.

Each Windows user creates and owns their own local vault. Sharing the
executable does not share vault data between people. Back up the folder
`%LOCALAPPDATA%\SavePassword\` if a user needs to move their vault to another
computer.

For a single-file build, PyInstaller can also use `--onefile`, but the
directory build is easier to troubleshoot and distribute with CustomTkinter.
The application data location remains outside the executable in either mode.

## Run the tests

```powershell
python -m pytest -q
```

On Bash/Linux/macOS:

```bash
python3 -m pytest -q
```

Run one test module or marker:

```powershell
python -m pytest test/test_user_database.py -q
python -m pytest -m user_database -q
```

On Bash/Linux/macOS:

```bash
python3 -m pytest test/test_user_database.py -q
python3 -m pytest -m user_database -q
```

## Security design

The master password is never stored. Scrypt derives a key from the master
password and a random salt. That derived key unlocks a random per-user vault
key, and the vault key encrypts saved credentials. Forgetting the master
password means the vault cannot be unlocked.
