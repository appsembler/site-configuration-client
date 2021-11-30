"""
Empty pytest settings.
"""

SECRET_KEY = 'dummy secret key'  # nosec

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'site_config_client',
]

FEATURES = {}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
