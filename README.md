# Save Password

This is a small command-line password manager written in Python. It uses
SQLite for storage and Fernet encryption for saved credentials.

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
first use. Test data is kept under `test/`.

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

## Current security note

The current version encrypts values with Fernet keys stored locally. This
protects the database from casual inspection but is not yet a complete
password-manager key hierarchy. Master-password-based key derivation and key
storage improvements are planned separately.
