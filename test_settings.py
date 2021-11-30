"""
Empty pytest settings.
"""

SECRET_KEY = 'dummy secret key'  # nosec

INSTALLED_APPS = [
    'site_config_client',
]

FEATURES = {}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
