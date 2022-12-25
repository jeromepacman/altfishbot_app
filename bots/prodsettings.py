from settings import *

DEBUG = False

import dj_database_url

DATABASES['default'] = dj_database_url.config(conn_max_age=600)

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

#CSRF_TRUSTED_ORIGIN = []

#SECURE_SSL_REDIRECT = True