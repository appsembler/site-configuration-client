"""
Common settings for the Open edX
"""
import logging

from site_config_client import Client
from site_config_client.django_cache import DjangoCache
from site_config_client.google_cloud_storage import GoogleCloudStorage


def plugin_settings(settings):
    bucket_name = getattr(settings, 'SITE_CONFIG_READ_ONLY_BUCKET', None)
    read_only_storage = None

    if bucket_name:
        read_only_storage = GoogleCloudStorage(
            bucket_name=settings.SITE_CONFIG_READ_ONLY_BUCKET,
        )

    cache = DjangoCache(
        cache_name=getattr(settings, 'SITE_CONFIG_CACHE_NAME', 'default'),
        cache_timeout=getattr(settings, 'SITE_CONFIG_CACHE_TIMEOUT', None),
    )

    base_url = getattr(settings, 'SITE_CONFIG_BASE_URL', None)
    if base_url:
        settings.SITE_CONFIG_CLIENT = Client(
            base_url=settings.SITE_CONFIG_BASE_URL,
            api_token=settings.SITE_CONFIG_API_TOKEN,
            read_only_storage=read_only_storage,
            cache=cache,
        )
    else:
        log.warn('.xxxxx')