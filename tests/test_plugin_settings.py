import mock
import pytest


@mock.patch('google.cloud.storage.Client')
@pytest.mark.openedx
def test_plugin_production_settings(client):
    # Local import to avoid test failures for non-openedx tests
    from site_config_client.openedx.settings.production import plugin_settings

    settings = mock.Mock(
        SITE_CONFIG_CLIENT=None,
        SITE_CONFIG_CACHE_NAME='default',
        SITE_CONFIG_CACHE_TIMEOUT=3600,
        SITE_CONFIG_BASE_URL="http://service",
        SITE_CONFIG_API_TOKEN="some-token",
        SITE_CONFIG_READ_ONLY_BUCKET="random-bucket",
    )

    plugin_settings(settings)

    assert settings.SITE_CONFIG_CLIENT, 'Client should be initialized'
    assert settings.SITE_CONFIG_CLIENT.read_only_storage, (
        'GCP storage is initialized')
    assert settings.SITE_CONFIF_CLIENT.cache, 'Cache is initialized'


@pytest.mark.openedx
def test_plugin_test_settings(client):
    # Local import to avoid test failures for non-openedx tests
    from site_config_client.openedx.settings.test import plugin_settings

    settings = mock.Mock(
        SITE_CONFIG_CLIENT=None,
    )

    plugin_settings(settings)

    assert settings.SITE_CONFIG_CLIENT, 'Client should be initialized'
    assert not settings.SITE_CONFIG_CLIENT.read_only_storage
    assert not settings.SITE_CONFIG_CLIENT.cache
