from .base import *

# DATABASE
DATABASES = secrets['DATABASES']['DEPLOY']

# WSGI
WSGI_APPLICATION = 'odoq_backend_second.wsgi_deploy.application'