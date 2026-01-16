import os
from pathlib import Path
from datetime import timedelta
import logging
from django.utils.log import DEFAULT_LOGGING

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# LOGS DIRECTORY: ./logs/ (same level as manage.py) - CREATED AUTOMATICALLY
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# SECURITY WARNING: Development key only - generate your own for production
SECRET_KEY = 'django-insecure-dev-key-change-in-production-2026x9zqwk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Django REST Framework
    'rest_framework',

    # Swagger/OpenAPI Documentation
    'drf_spectacular',

    # JWT Authentication
    'rest_framework_simplejwt',

    # Custom Apps
    'products',
    'contacts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'config.middleware.DRFRequestResponseLoggingMiddleware',  
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',  # default open, override in views
    ),
    # Very important for drf-spectacular!
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Products & Contacts API",
    "DESCRIPTION": "API with JWT authentication and Swagger documentation",
    "VERSION": "1.0.0",
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ====================================================================
# ADVANCED LOGGING CONFIGURATION
# Files saved to ./logs/ directory (created automatically)
# ====================================================================
LOGGING = DEFAULT_LOGGING.copy()
LOGGING['version'] = 1
LOGGING['disable_existing_loggers'] = False

# Custom formatter for API logs
LOGGING.setdefault('formatters', {})
LOGGING['formatters']['api'] = {
    'format': '[{levelname}] {asctime} {name} {message}',
    'style': '{',
}

# API log handler - saves to ./logs/api.log
LOGGING.setdefault('handlers', {})
LOGGING['handlers']['api_file'] = {
    'level': 'INFO',
    'class': 'logging.FileHandler',
    'filename': str(LOG_DIR / 'api.log'),
    'formatter': 'api',
}

# Django framework log handler - saves to ./logs/django.log
LOGGING['handlers']['django_file'] = {
    'level': 'INFO',
    'class': 'logging.FileHandler',
    'filename': str(LOG_DIR / 'django.log'),
    'formatter': 'api',
}

# Error log handler - saves to ./logs/errors.log
LOGGING['handlers']['error_file'] = {
    'level': 'ERROR',
    'class': 'logging.FileHandler',
    'filename': str(LOG_DIR / 'errors.log'),
    'formatter': 'api',
}

# API requests logger
LOGGING.setdefault('loggers', {})
LOGGING['loggers']['api.requests'] = {
    'handlers': ['api_file'],
    'level': 'INFO',
    'propagate': False,
}

# Django logger
LOGGING['loggers']['django'] = {
    'handlers': ['console', 'django_file'],
    'level': 'INFO',
    'propagate': False,
}

# Django request errors logger
LOGGING['loggers']['django.request'] = {
    'handlers': ['error_file'],
    'level': 'ERROR',
    'propagate': False,
}
