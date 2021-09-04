"""
Django settings for skeleton project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import json
import os
import logging
import textwrap
import random
from pathlib import Path
from typing import Type


logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

REPO_DIR = os.path.dirname(BASE_DIR)

# ENVIRONMENT = 'development'
APP_ENVIRONMENT = os.environ.get("APP_ENVIRONMENT", "development")

SETTINGS_FILE = "settings.%s.json" % APP_ENVIRONMENT


_env_file = os.path.join(REPO_DIR, "config", SETTINGS_FILE)


def read_env_file(path_to_env_file, mode="r"):
    with open(path_to_env_file, mode) as f:
        data = f.read()

    return data


if os.path.exists(_env_file):
    # Decrypt settings file exists, proceed
    _env = read_env_file(_env_file)
    _env = json.loads(_env)
else:
    _env = {}

ENV = _env

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# TODO: generate new secret key: python ./scripts/gen_secret_key.py
SECRET_KEY = "h(vl^c^q7heqsv-qq(=3u@*p=nh+ch2l$^*i)hpowu!v8e#&5g"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV.get("DEBUG", False)

ALLOWED_HOSTS = ["*"]

RUNNING_ON_LOCALHOST = ENV.get("RUNNING_ON_LOCALHOST", False)

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "django_filters",
    "simple_history",
    # TODO: Add apps here
]

if DEBUG:
    try:
        # Install django-extensions if it exists
        import django_extensions  # noqa

        INSTALLED_APPS.append("django_extensions")
    except ImportError:
        pass

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "skeleton.middleware.check_domain_middleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

if DEBUG:
    MIDDLEWARE.insert(0, "skeleton.middleware.db_query_count_middleware")

ROOT_URLCONF = "skeleton.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]

WSGI_APPLICATION = "skeleton.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

if ENV.get("USE_DATABASE", False):
    logger.info("Using PostgreSQL database")
    DATABASES["default"] = {
        "ATOMIC_REQUESTS": True,
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": ENV["DATABASE_NAME"],
        "USER": ENV["DATABASE_USER"],
        "PASSWORD": ENV["DATABASE_PASSWORD"],
        "HOST": ENV["DATABASE_HOST"],
        "TEST": {
            "NAME": "test_" + ENV["DATABASE_NAME"] + "_%x" % random.randrange(16 ** 6)
        },
    }
else:
    logger.info("Using SQLite database")


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {"level": "INFO", "filters": [], "class": "logging.StreamHandler"},
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "INFO"},
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

FIXTURE_DIRS = ["src/skeleton/fixtures"]

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
]

CORS_ORIGIN_WHITELIST = ENV.get("DOMAINS", [])
