from . import settings

import dj_database_url

DATABASES = {'default': dj_database_url.config(conn_max_age=600)}


#SECURE_SSL_REDIRECT = True