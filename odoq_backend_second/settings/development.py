from .base import *

# DATABASE
DATABASES = secrets['DATABASES']['DEVELOPMENT']

# WSGI
WSGI_APPLICATION = 'odoq_backend_second.wsgi_deploy.application'