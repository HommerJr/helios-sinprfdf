"""
Django settings for silver project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import sys

import json
from pathlib import Path
import ldap
from django_auth_ldap.config import LDAPSearch

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TESTING = 'test' in sys.argv


# go through environment variables and override them
def get_from_env(var, default):
    if not TESTING and var in os.environ:
        return os.environ[var]
    else:
        return default


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_from_env('SECRET_KEY', 'replace-me')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (get_from_env('DEBUG', '1') == '1')

ALLOWED_HOSTS = get_from_env('ALLOWED_HOSTS', 'localhost').split(",")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    ## HELIOS stuff
    'anymail',
    'helios_auth',
    'helios',
    'server_ui',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'helios.security.HSTSMiddleware',
]

CSRF_TRUSTED_ORIGINS = get_from_env('CSRF_TRUSTED_ORIGINS', 'https://localhost').split(",")

ROOT_URLCONF = 'helios.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR,
            BASE_DIR / 'templates',
            BASE_DIR / 'helios' / 'templates' / 'helios',
            BASE_DIR / 'helios_auth' / 'templates' / 'helios_auth',
            BASE_DIR / 'server_ui' / 'templates' / 'server_ui',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    },
]

WSGI_APPLICATION = 'helios.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_from_env('DB_NAME', 'helios'),
        'USER': get_from_env('DB_USER', 'helios'),
        'PASSWORD': get_from_env('DB_PWD', 'heliosteste'),
        'HOST': get_from_env('POSTGRES_HOST', 'localhost'),
        'PORT': get_from_env('POSTGRES_PORT', '5432'),
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'options': '-c timezone=UTC',
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'
# TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

# USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'admin' / 'static'
]
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# override if we have an env variable
if get_from_env('DATABASE_URL', None):
    import dj_database_url

    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=False)
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'

DATE_FORMAT = 'd/m/Y'  # Formato de data: dia/mês/ano
TIME_FORMAT = 'H:i'  # Formato de hora: 24 horas
DATETIME_FORMAT = 'd/m/Y H:i'  # Formato de data e hora

# set up celery
CELERY_BROKER_URL = get_from_env('CELERY_BROKER_URL', 'amqp://localhost')
if TESTING:
    CELERY_TASK_ALWAYS_EAGER = True

# email server
EMAIL_HOST = get_from_env('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(get_from_env('EMAIL_PORT', "2525"))
EMAIL_HOST_USER = get_from_env('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = get_from_env('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = (get_from_env('EMAIL_USE_TLS', '0') == '1')

# to use AWS Simple Email Service
# in which case environment should contain
# AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
if get_from_env('EMAIL_USE_AWS', '0') == '1':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

ANYMAIL = {
    "MAILGUN_API_KEY": get_from_env('MAILGUN_API_KEY', None),
}

if ANYMAIL["MAILGUN_API_KEY"]:
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

# add admins of the form:
#    ('Ben Adida', 'ben@adida.net'),
# if you want to be emailed about errors.
admin_email = get_from_env('ADMIN_EMAIL', None)
if admin_email:
    ADMINS = [(get_from_env('ADMIN_NAME', ''), admin_email)]
else:
    ADMINS = []

MANAGERS = ADMINS

# is this the master Helios web site?
MASTER_HELIOS = (get_from_env('MASTER_HELIOS', '0') == '1')

# show ability to log in? (for example, if the site is mostly used by voters)
# if turned off, the admin will need to know to go to /auth/login manually
SHOW_LOGIN_OPTIONS = (get_from_env('SHOW_LOGIN_OPTIONS', '1') == '1')

# sometimes, when the site is not that social, it's not helpful
# to display who created the election
SHOW_USER_INFO = (get_from_env('SHOW_USER_INFO', '1') == '1')

SITE_ID = 1

# Secure Stuff
if get_from_env('SSL', '0') == '1':
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True

    # tuned for Heroku
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_HTTPONLY = True

# let's go with one year because that's the way to do it now
STS = False
if get_from_env('HSTS', '0') == '1':
    STS = True
    # we're using our own custom middleware now
    # SECURE_HSTS_SECONDS = 31536000
    # not doing subdomains for now cause that is not likely to be necessary and can screw things up.
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

SILENCED_SYSTEM_CHECKS = ['urls.W002']

##
## HELIOS
##


# a relative path where voter upload files are stored
VOTER_UPLOAD_REL_PATH = "voters/%Y/%m/%d"

# Change your email settings
DEFAULT_FROM_EMAIL = get_from_env('DEFAULT_FROM_EMAIL', '')
DEFAULT_FROM_NAME = get_from_env('DEFAULT_FROM_NAME', '')
SERVER_EMAIL = '%s <%s>' % (DEFAULT_FROM_NAME, DEFAULT_FROM_EMAIL)

LOGIN_URL = '/auth/'
LOGOUT_ON_CONFIRMATION = False

# The two hosts are here so the main site can be over plain HTTP
# while the voting URLs are served over SSL.
URL_HOST = get_from_env("URL_HOST", "http://localhost:8000").rstrip("/")

# IMPORTANT: you should not change this setting once you've created
# elections, as your elections' cast_url will then be incorrect.
# SECURE_URL_HOST = "https://localhost:8443"
SECURE_URL_HOST = get_from_env("SECURE_URL_HOST", URL_HOST).rstrip("/")

# election stuff
SITE_TITLE = get_from_env('SITE_TITLE', 'Plataforma de Eleições Helios')
MAIN_LOGO_URL = get_from_env('MAIN_LOGO_URL', '/static/server_ui/logo.png')
TINY_LOGO_URL = get_from_env('TINY_LOGO_URL', '/static/server_ui/tinylogo.png')
ALLOW_ELECTION_INFO_URL = (get_from_env('ALLOW_ELECTION_INFO_URL', '0') == '1')

# FOOTER links
FOOTER_LINKS = json.loads(get_from_env('FOOTER_LINKS', '[]'))
FOOTER_LOGO_URL = get_from_env('FOOTER_LOGO_URL', None)

WELCOME_MESSAGE = get_from_env('WELCOME_MESSAGE',
                               "Seja bem-vindo(a) à plataforma de eleições Helios!<br />Vote com consciência e contribua para a democracia acadêmica.")

HELP_EMAIL_ADDRESS = get_from_env('HELP_EMAIL_ADDRESS', 'help@heliosvoting.org')

AUTH_TEMPLATE_BASE = "server_ui/templates/server_ui/base.html"
HELIOS_TEMPLATE_BASE = "server_ui/templates/server_ui/base.html"
HELIOS_ADMIN_ONLY = False
HELIOS_VOTERS_UPLOAD = True
HELIOS_VOTERS_EMAIL = True

# are elections private by default?
HELIOS_PRIVATE_DEFAULT = False

# authentication systems enabled
# AUTH_ENABLED_SYSTEMS = ['password','ldap','facebook','twitter','google','yahoo']
AUTH_ENABLED_SYSTEMS = get_from_env('AUTH_ENABLED_SYSTEMS',
                                    get_from_env('AUTH_ENABLED_AUTH_SYSTEMS', 'password,google')).split(",")
AUTH_DEFAULT_SYSTEM = get_from_env('AUTH_DEFAULT_SYSTEM',
                                   get_from_env('AUTH_DEFAULT_AUTH_SYSTEM', 'google'))

# google
GOOGLE_CLIENT_ID = get_from_env('GOOGLE_CLIENT_ID', '')
GOOGLE_CLIENT_SECRET = get_from_env('GOOGLE_CLIENT_SECRET', '')

# facebook
FACEBOOK_APP_ID = get_from_env('FACEBOOK_APP_ID', '')
FACEBOOK_API_KEY = get_from_env('FACEBOOK_API_KEY', '')
FACEBOOK_API_SECRET = get_from_env('FACEBOOK_API_SECRET', '')

# twitter
TWITTER_API_KEY = ''
TWITTER_API_SECRET = ''
TWITTER_USER_TO_FOLLOW = 'heliosvoting'
TWITTER_REASON_TO_FOLLOW = "we can direct-message you when the result has been computed in an election in which you participated"

# the token for Helios to do direct messaging
TWITTER_DM_TOKEN = {"oauth_token": "", "oauth_token_secret": "", "user_id": "", "screen_name": ""}

# LinkedIn
LINKEDIN_API_KEY = ''
LINKEDIN_API_SECRET = ''

# CAS (for universities)
CAS_USERNAME = get_from_env('CAS_USERNAME', "")
CAS_PASSWORD = get_from_env('CAS_PASSWORD', "")
CAS_ELIGIBILITY_URL = get_from_env('CAS_ELIGIBILITY_URL', "")
CAS_ELIGIBILITY_REALM = get_from_env('CAS_ELIGIBILITY_REALM', "")

# Clever
CLEVER_CLIENT_ID = get_from_env('CLEVER_CLIENT_ID', "")
CLEVER_CLIENT_SECRET = get_from_env('CLEVER_CLIENT_SECRET', "")

# GitHub
GH_CLIENT_ID = get_from_env('GH_CLIENT_ID', '')
GH_CLIENT_SECRET = get_from_env('GH_CLIENT_SECRET', '')

# ldap
# see configuration example at https://pythonhosted.org/django-auth-ldap/example.html
AUTH_LDAP_SERVER_URI = "ldap://ldap.forumsys.com"  # replace by your Ldap URI
AUTH_LDAP_BIND_DN = "cn=read-only-admin,dc=example,dc=com"
AUTH_LDAP_BIND_PASSWORD = "password"
AUTH_LDAP_USER_SEARCH = LDAPSearch("dc=example,dc=com", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}

AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = True

AUTH_LDAP_ALWAYS_UPDATE_USER = True

# database_url = DATABASES['default']

# set up logging
import logging

logging.basicConfig(
    level=logging.DEBUG if TESTING else logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Rollbar Error Logging
ROLLBAR_ACCESS_TOKEN = get_from_env('ROLLBAR_ACCESS_TOKEN', None)
if ROLLBAR_ACCESS_TOKEN:
    print("setting up rollbar")
    MIDDLEWARE += ['rollbar.contrib.django.middleware.RollbarNotifierMiddleware', ]
    ROLLBAR = {
        'access_token': ROLLBAR_ACCESS_TOKEN,
        'environment': 'development' if DEBUG else 'production',
    }