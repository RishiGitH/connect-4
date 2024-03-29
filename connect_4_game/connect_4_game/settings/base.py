# -*- coding: utf-8 -*-
"""
Django settings for connect_4_game project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import re
import sys
import urllib
import logging.config, logging

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = lambda *x: os.path.join(BASE_DIR, *x)
sys.path.insert(0, root('apps'))

try:
    from .prelocal import *
except:
    redis_host = os.environ.get('REDIS_HOST', 'localhost')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i7*po9$q$puqp7=s=&+idxu592qy^94xnf76fs2(y-1ve$ws!-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    LOG_FILENAME='connect_4_game.log'
else:
    LOG_FILENAME='/var/log/connect_4_game.log'

ALLOWED_HOSTS = ['127.0.0.1', '*']

IN_TESTING = sys.argv[1:2] == ['test']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cache_fallback',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_jinja',
    'django_extensions',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'cacheops',
    'storages',

]

PROJECT_APPS = [
    'utils',
    'api',

]

INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'utils.middleware.CachedTemplateMiddleware',

]

ROOT_URLCONF = 'connect_4_game.urls'
CORS_ORIGIN_ALLOW_ALL =  True


TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': [
            root('templates'),
        ],
        'OPTIONS': {
            "match_extension": ".jinja",
            "context_processors": [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.common',

            ]
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            root('templates'),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

WSGI_APPLICATION = 'connect_4_game.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'connect_4_db',
       'USER': 'root',
       'PASSWORD': 'root',
       'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
       'PORT': '',  # Set to empty string for default.
       'OPTIONS': {'charset': 'utf8mb4'},
   }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = root('../static')
MEDIA_ROOT = root('../media')

STATICFILES_DIRS = (
    root('../assets'),
)

SITE_ID = 1

ROOT_URLCONF = 'connect_4_game.urls'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'pipeline.finders.PipelineFinder',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'pipeline.finders.PipelineFinder',
)

# STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

SUBDOMAIN_URLCONFS = {
    None: 'connect_4_game.urls',
    'www': 'connect_4_game.urls',
}


LOGIN_REDIRECT_URL = '/'





API_LOGGER = logging.getLogger('connect_4_game')
API_LOGGER.propagate = False

CACHES = {

    'default': {
            'BACKEND': 'cache_fallback.FallbackCache',
        },

    'main_cache': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://' + redis_host + ':6379',
        'TIMEOUT': 5*60,
        'OPTIONS': {
            'DB': 0,
        },
    },

    'fallback_cache': {
         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
     }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': LOG_FILENAME,
            'formatter': 'json',
        },
        'json':{
            'class': 'logging.FileHandler',
            'filename': LOG_FILENAME,
            'formatter': 'json',
        },
        'console': {
            'level': 'NOTSET',
            'class': 'logging.StreamHandler',
        }
    },
    'formatters': {
        'json': {
            'format': '%(pathname)s %(asctime)s %(name)s %(process)s %(levelname)s %(lineno)d  %(message)s',
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter'
        }
    },
    'loggers': {

        'django': {
            'handlers': ['logfile', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        # Your own app - this assumes all your logger names start with "myapp."
        'connect_4_game': {
            'handlers': ['logfile', 'json', 'console'],
            'level': 'INFO', # Or maybe INFO or DEBUG
            'propagate': False
        },
    },
}


logging.config.dictConfig(LOGGING)

CACHED_VIEWS = {
    'home': 86400,
}

CACHEOPS_REDIS = "redis://"+redis_host+":6379"
CACHEOPS_PREFIX = lambda _: "connect_4_cacheops_"


CACHEOPS = {
    'api.*': {'ops': 'all', 'timeout': 60*15},

    # '*.*': {'ops': 'all','timeout': 60*60},
}

CACHEOPS_DEGRADE_ON_FAILURE = True

LOGIN_URL = '/login/'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}




