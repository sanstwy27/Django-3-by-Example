from .base import *


DEBUG = True


ADMINS = (
    ('Antonio M', 'email@mydomain.com'),
)


ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'XXXX',
        'USER': 'XXXX',
        'PASSWORD': 'XXXX',
    }
}


#SECURE_SSL_REDIRECT = True
#CSRF_COOKIE_SECURE = True