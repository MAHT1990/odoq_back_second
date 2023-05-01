from .base import *

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'awslearner',
#         'USER': 'awslearner',
#         'PASSWORD': 'v3nop101slk#',
#         'HOST': 'awslearner.clbg2pjhuyja.ap-northeast-2.rds.amazonaws.com',
#         'PORT': '3306',
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         }
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'odoqtestrds2',
        'USER': 'odoqtestrds2',
        'PASSWORD': 'v3nop101slk#',
        'HOST': 'odoqtestrds2.clbg2pjhuyja.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

WSGI_APPLICATION = 'odoq_backend_second.wsgi_deploy.application'