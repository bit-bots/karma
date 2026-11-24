"""Isolated settings for application tests; no deployment configuration needed."""

from pathlib import Path
from runpy import run_path

globals().update(
    {
        key: value
        for key, value in run_path(
            str(Path(__file__).with_name("settings.py.example"))
        ).items()
        if key.isupper()
    }
)

SECRET_KEY = "karma-tests-only"
DEBUG = False
ALLOWED_HOSTS = ["testserver"]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
OPENID_ISSUER = "https://openid.invalid"
OPENID_CLIENT_ID = "karma-tests"
OPENID_CLIENT_SECRET = "tests-only"
OPENID_BASE_URI = "http://testserver"
