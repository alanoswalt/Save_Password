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

The application creates its runtime directories and files under `data/` on
first use. Test data is kept under temporary pytest directories.

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
