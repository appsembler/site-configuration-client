import mock
from site_config_client.openedx.common import plugin_settings
from site_config_client import Client


@mock.patch('google.cloud.storage.Client')
def test_plugin_settings(client):
    base_url = "http://service"
    token = "some-token"
    read_only_storage = "random-bucket"
    cache_name = "default"
    settings = mock.Mock(
        SITE_CONFIG_CACHE_NAME='default',
        SITE_CONFIG_CACHE_TIMEOUT=3600,
        SITE_CONFIG_BASE_URL=base_url,
        SITE_CONFIG_API_TOKEN=token,
        SITE_CONFIG_CLIENT=Client(
            base_url=base_url,
            api_token=token,
            read_only_storage=read_only_storage,
            cache=cache_name)
    )

    plugin_settings(settings)

    assert settings.SITE_CONFIG_CLIENT.read_only_storage, (
        'GCP storage is initialized')
    assert settings.SITE_CONFIF_CLIENT.cache, 'Cache is initialized'
