"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import logging

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production  
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '88x0xv73$foz%p#_u23+c%(psc^@m5)!n)4fvwiw%wl6a7kg=a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'haystack',
    #My app
    'blog',
    'account',
    'article',
    'mptt',
    'contact',
    'news',
    'image',
    'sorl.thumbnail',
    'pdfs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

import pymysql
pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysite',
        'USER': 'root',
        'password': 'bwt4850694',
        'HOST':'152.136.109.221',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'ASIA/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

LOGIN_REDIRECT_URL = '/home/'
LOGIN_URL = '/account/login/'

EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '1927552890@qq.com'
with open('/home/ubuntu/djang_rockfracturegroup/rockfracturegroup/my_password/email_host_password.txt','r') as f:
	EMAIL_HOST_PASSWORD = f.read().strip()
DEFAULT_FROM_EMAIL = "1927552890@qq.com"


REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_DB = 0

HAYSTACK_CONNECTIONS = {
	'default':{
		'ENGINE':'article.whoosh_cn_backend.WhooshEngine',
		'PATH':os.path.join(BASE_DIR, 'whoosh_index'),
	},
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
#设置每页显示的数目，默认为20，可以自己修改
HAYSTACK_SEARCH_RESULTS_PER_PAGE  =  2

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

ADMINS = (('1927552890', '1927552890@qq.com'),)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL = EMAIL_HOST_USER

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'verbose':{
			'format': '{levelname} {asctime} {process:d} {thread:d} {message}',
			'style': '{',
		},
		'simple': {
			'format': '{levelname} {message}',
			'style': '{',
		},
	},
	'filters':{
		'require_debug_true': {
			'()': 'django.utils.log.RequireDebugTrue',
		},
	},
	'handlers': {
		'console': {
			'level': 'INFO',
			'filters': ['require_debug_true'],
			'class': 'logging.StreamHandler',
			'formatter': 'simple'
		},
		'mail_admins': {
			'level': 'ERROR',
			'class': 'django.utils.log.AdminEmailHandler',
			'formatter': 'verbose',
		},
		'file': {
			'level': 'WARNING',
			#'class': 'logging.FileHandler',
			'class': 'logging.handlers.TimedRotatingFileHandler',
			'when': 'midnight',
			'backupCount': 30,
			'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
			'formatter': 'verbose',
		},
	},
	'loggers': {
		'django':{
			'handlers': ['console'],
			'propagate': True,
		},
		'django.request': {
			'handlers': ['file', 'mail_admins'],
			'level': 'WARNING',
			'propagate': False,
		},
	}
}

	
		
