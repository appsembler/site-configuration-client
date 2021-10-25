"""
Tests for Cache
"""

from site_config_client.django_cache import DjangoCache


def test_django_cache():
    cache_name = "site_config_client.040e0ec3-2578-4fcf-b5db-030dadf68f30.live"
    cache = DjangoCache(cache_name=cache_name)

    assert cache.cache_name == cache_name
    assert cache.cache_timeout == 60
