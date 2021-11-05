"""
Tests for Cache
"""

from site_config_client.django_cache import DjangoCache


def test_empty_get(settings):
    settings.CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }
    cache = DjangoCache(cache_name='default')
    cache_key = 'client.040e0ec3-2578-4fcf-b5db-030dadf68f30.live'
    assert cache.get(key=cache_key) is None


def test_set_get(settings):
    settings.CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

    cache = DjangoCache(cache_name='default')

    configs = {
     "site": {
            "uuid": "77d4ee4e-6888-4965-b246-b8629ac65bce",
            "domain_name": "croissant.edu",
            "tier": "trial",
            "always_active": False,
            "subscription_ends": "2021-10-31T16:44:45+0000",
            "is_active": True},
     "status": "live",
     "configuration": {
            "admin": [
                {
                    "name": "features",
                    "value": ["bi_connector", "google_tag_manageer"]
                }
            ],
            "css": [
                {
                    "name": "accent-font",
                    "value": "monospace"
                }
            ],
            "page": [],
            "setting": [
                {
                    "name": "PLATFORM_NAME",
                    "value": "Momofuku Academy"
                }
            ],
            "integration": [],
            "secret": [
                {
                    "name": "SEGMENT_KEY",
                    "value": "orc"
                },
                {
                    "name": "SECRET_KEY",
                    "value": "hobbit"
                }
            ]}
    }
    cache_key = 'client.040e0ec3-2578-4fcf-b5db-030dadf68f30.live'
    cache.set(key=cache_key, value=configs)
    assert cache.get(key=cache_key) == configs
