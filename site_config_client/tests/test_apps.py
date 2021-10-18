"""
Test SiteConfigApp
"""

from site_config_client.apps import SiteConfigApp


def test_plugin_config(self):
    """
    Check for syntax or other severe errors in SiteConfigApp.plugin_app
    """
    config = SiteConfigApp('siteconfig', SiteConfigApp.apps)
    assert type(config.plugin_app) == dict
