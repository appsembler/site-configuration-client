"""
Test SiteConfigApp
"""

from site_config_client import apps


def test_plugin_config():
    """
    Check for syntax or other severe errors in SiteConfigApp.plugin_app
    """
    config = apps.SiteConfigApp('siteconfig', apps)
    assert type(config.plugin_app) == dict
