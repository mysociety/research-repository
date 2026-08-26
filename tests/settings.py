"""Settings used by the pytest suite.

SQLite keeps the suite runnable without services. Set TEST_DATABASE=postgres to
exercise the same database backend used by the application (for example in CI).
"""

import os
import tempfile

try:
    from conf import config
except ImportError as error:
    raise RuntimeError(
        "Missing conf/config.py. Run script/bootstrap before running tests."
    ) from error

# Older local config files predate this setting.
if not hasattr(config, "MEASUREMENT_SECRET_KEY"):
    config.MEASUREMENT_SECRET_KEY = ""

for variable in (
    "REPOSITORY_DB_HOST",
    "REPOSITORY_DB_PORT",
    "REPOSITORY_DB_USER",
    "REPOSITORY_DB_NAME",
    "REPOSITORY_DB_PASS",
):
    if variable in os.environ:
        setattr(config, variable, os.environ[variable])

from repository.settings.base import *  # noqa: E402,F403

DEBUG = False
SECRET_KEY = "pytest-secret-key"
ALLOWED_HOSTS = ["testserver", "localhost"]

if os.environ.get("TEST_DATABASE", "sqlite") != "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

_TEST_ROOT = os.path.join(tempfile.gettempdir(), "research-repository-tests")
MEDIA_ROOT = os.path.join(_TEST_ROOT, "media")
ZIP_ROOT = os.path.join(_TEST_ROOT, "zip")
SITES_ROOT = os.path.join(_TEST_ROOT, "sites")

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

PIPELINE_ENABLED = False
HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.BaseSignalProcessor"
HAYSTACK_CONNECTIONS = {
    "default": {"ENGINE": "haystack.backends.simple_backend.SimpleEngine"}
}
