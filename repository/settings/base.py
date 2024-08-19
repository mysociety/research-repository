"""
Django settings for repository project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from pathlib import Path

from conf import config

from .paths import PARENT_DIR, PROJECT_DIR, PROJECT_ROOT

DEBUG = bool(int(config.STAGING))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config.REPOSITORY_DB_NAME,
        "USER": config.REPOSITORY_DB_USER,
        "PASSWORD": config.REPOSITORY_DB_PASS,
        "HOST": config.REPOSITORY_DB_HOST,
        "PORT": config.REPOSITORY_DB_PORT,
    }
}

SECRET_KEY = config.DJANGO_SECRET_KEY

ADMINS = ()

if hasattr(config, "ADMIN_NAME"):
    ADMINS = ((config.ADMIN_NAME, config.ADMIN_EMAIL),)

MANAGERS = ADMINS

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "rest_framework",
    "rest_framework.authtoken",
    "pipeline",
    "autoslug",
    "markitup",
    "import_export",
    "sorl.thumbnail",
    "haystack",
    "repository",
    "pages",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",  # <-- And here
    ],
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "repository.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "repository.context_processors.add_settings",
            ],
            "debug": DEBUG,
        },
    },
]

WSGI_APPLICATION = "repository.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True


USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PARENT_DIR, "collected_static")
ZIP_ROOT = os.path.join(PARENT_DIR, "zip_uploads")
SITES_ROOT = os.path.join(PARENT_DIR, "sites")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
ZIP_URL = "/html/"
SITES_URL = "/sites/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, "web"),
)

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "pipeline.storage.PipelineManifestStorage",
    },
}

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pipeline.finders.PipelineFinder",
)

# Django-Pipeline configuration
# https://django-pipeline.readthedocs.io/en/latest/configuration.html
PIPELINE = {
    "STYLESHEETS": {
        "main": {
            "source_filenames": ("sass/global.scss",),
            "output_filename": "css/main.css",
        },
    },
    "CSS_COMPRESSOR": "django_pipeline_csscompressor.CssCompressor",
    "DISABLE_WRAPPER": True,
    "COMPILERS": ("pipeline.compilers.sass.SASSCompiler",),
    # Use the libsass commandline tool (that's bundled with libsass) as our
    # sass compiler, so there's no need to install anything else.
    "SASS_BINARY": config.SASSC_LOCATION,
}

# Uploaded files

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PARENT_DIR, "uploads")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"


# Logging

# Log WARN and above to stderr; ERROR and above by email when DEBUG is False.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "console": {
            "level": "WARN",
            "class": "logging.StreamHandler",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["mail_admins", "console"],
            "level": "WARN",
            "propagate": True,
        },
    },
}


# Cookies

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True


# Allowed hosts

ALLOWED_HOSTS = config.ALLOWED_HOSTS


# Use mailcatcher in development
if DEBUG:
    EMAIL_HOST = "127.0.0.1"
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    EMAIL_PORT = 1025
    EMAIL_USE_TLS = False


# MarkItUp settings
MARKITUP_FILTER = ("markdown.markdown", {"safe_mode": True})

# Thumbnails
THUMBNAIL_ALTERNATIVE_RESOLUTIONS = [1.5, 2]

THUMBNAIL_FONT = config.THUMBNAIL_FONT

# mySociety-specific settings
GOOGLE_ANALYTICS_ACCOUNT = config.GOOGLE_ANALYTICS_ACCOUNT

MAILCHIMP_API_KEY = config.MAILCHIMP_API_KEY

# mySociety-specific settings
SITE_BASE_URL = config.SITE_BASE_URL

# settings for social sharing
DEFAULT_SHARE_IMAGE = config.DEFAULT_SHARE_IMAGE
DEFAULT_SHARE_IMAGE_LARGE = "/static/img/mysoc_research_logo.png"

MARKITUP_FILTER = ("markdown.markdown", {"safe_mode": True})

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

X_FRAME_OPTIONS = "SAMEORIGIN"

HAYSTACK_CUSTOM_HIGHLIGHTER = "repository.search_funcs.PhraseHighlighter"

HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.RealtimeSignalProcessor"

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": os.path.join(Path(__file__).parent.parent.parent, "whoosh_index"),
    },
}
