"""
Test SiteConfigApp
"""
import pytest


@pytest.mark.openedx
def test_plugin_config():
    """
    Check for syntax or other severe errors in SiteConfigApp.plugin_app
    """
    # Local import to avoid test failures for non-openedx tests
    from site_config_client import apps

    config = apps.SiteConfigApp('siteconfig', apps)
    assert type(config.plugin_app) == dict
