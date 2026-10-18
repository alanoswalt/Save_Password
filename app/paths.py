"""Application paths shared by the runtime and the database layer.

Source runs deliberately keep using the repository's ``data`` directory so
development and tests remain easy to inspect.  A PyInstaller build sets
``sys.frozen``; in that case, user data is stored outside the executable in a
per-Windows-user application-data directory.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


APP_NAME = "SavePassword"
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _application_data_root() -> Path:
    """Return the writable root intended for this user's application data."""

    override = os.environ.get("SAVE_PASSWORD_DATA_DIR")
    if override:
        return Path(override).expanduser()

    if sys.platform == "win32":
        base = Path(
            os.environ.get(
                "LOCALAPPDATA",
                Path.home() / "AppData" / "Local",
            )
        )
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(
            os.environ.get(
                "XDG_DATA_HOME",
                Path.home() / ".local" / "share",
            )
        )

    return base / APP_NAME


def _data_directory() -> Path:
    if getattr(sys, "frozen", False):
        return _application_data_root()
    return PROJECT_ROOT / "data"


DATA_DIR = _data_directory()
USERS_DIR = DATA_DIR / "users"
ALL_USERS_DB = DATA_DIR / "all_user.db"
LOG_FILE = DATA_DIR / "save_password.log"


def ensure_data_directories() -> None:
    """Create writable application directories before a file is opened."""

    USERS_DIR.mkdir(parents=True, exist_ok=True)

