"""
Django 許多初始化的定義都在這邊
"""

import os
from log import logger

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v!1n#$97dvwqai!vjwm3588%2p2g!w+*zgc*%q%m9-3c6ff%pg2x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('ENV') != 'prod'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (),
    'DEFAULT_PERMISSION_CLASSES': (),
}

# Application definition
# import 一些套件進來
INSTALLED_APPS = [
    'import_export',
    'django.contrib.gis',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
    'django_crontab',
    'django.contrib.sitemaps',
    'django_user_agents',
]
coordinates = {
    'JAL': {
        "type": "FeatureCollection",

        "features": [
            {"type": "Feature", "properties": {"Name": "jalandhar", "Description": ""}, "geometry": {"type": "Polygon",
                                                                                                     "coordinates": [[[
                                                                                                                          75.510571,
                                                                                                                          31.384717,
                                                                                                                          0.0],
                                                                                                                      [
                                                                                                                          75.515237,
                                                                                                                          31.270770,
                                                                                                                          0.0],
                                                                                                                      [
                                                                                                                          75.683574,
                                                                                                                          31.264225,
                                                                                                                          0.0],
                                                                                                                      [
                                                                                                                          75.672656,
                                                                                                                          31.390200,
                                                                                                                          0.0],
                                                                                                                      [
                                                                                                                          75.510571,
                                                                                                                          31.384717,
                                                                                                                          0.0]]]}}
        ]
    }
}
MIDDLEWARE = [
    # 'django_samesite_none.middleware.SameSiteNoneMiddleware',
    # middleware 才可以加log
    'api.middleware.defaultmiddleware',
    'api.middleware.CatchErrorMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# cache setting
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://coupon3-redis:6379/0",
        "TIMEOUT": 60 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = 'default'

# 此專案 目前用不到cron jobs
CRONJOBS = [
]

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

ROOT_URLCONF = 'web.urls'
# CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ['*']

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['web/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'web.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
#
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DB 設定
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'NAME': 'ezgo',
        'USER': 'root',
        'PASSWORD': 'conquers666',
        "DEFAULT-CHARACTER-SET": 'utf8',
        'HOST': 'coupon-db',
        'PORT': '3306',
        'TEST': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'test.db'),
        },
        # 'OPTIONS': {'charset': 'utf8mb4'},
        'OPTIONS': {
            'charset': 'utf8',
            'use_unicode': True,
            'init_command': 'SET '
                            'storage_engine=INNODB,'
                            'character_set_connection=utf8,'
                            'collation_connection=utf8mb4_unicode_ci'
            # 'sql_mode=STRICT_TRANS_TABLES,'    # see note below
            # 'SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED',
        },
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8mb4_unicode_ci',
    }
}

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'web/templates/static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '3CP@conquers.co'
EMAIL_HOST_PASSWORD = '3cp285582'
EMAIL_FROM = '3CP@conquers.co'
