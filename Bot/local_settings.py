import os

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-n9migz)217a6yucwbzds92t77wmr)co@^%*q+c!^v84l_twz6b"

#settings.pyからそのままコピー
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DEBUG = True
