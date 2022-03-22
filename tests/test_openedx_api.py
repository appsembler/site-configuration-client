"""
Tests for the openedx.api module.
"""

import pytest


backend_configs = {
    'page': {
        'about': {
            'title': 'About page from site configuration service',
        }
    },
    'secret': {
        'SEGMENT_KEY': 'test-secret-from-service',
    },
    'admin': {
        'IDP_TENANT_ID': 'dummy-tenant-id',
    },
}


def site_config_factory(**kwargs):
    """
    Mock an Open edX SiteConfiguration model instance.
    """


def test_page_content_without_adapter(self):
    """
    Test `get_page_content()` without the SiteConfig adapter.
    """
    site_configuration = SiteConfigurationFactory.create(
        site=self.site,
        page_elements={
            'about': {
                'title': 'About page in Django model.',
            },
        },
    )
    assert site_configuration.get_page_content('about') == {
        'title': 'About page in Django model.',
    }


def test_page_content_with_adapter(self):
    """
    Ensure `get_page_content()` uses the SiteConfig adapter when available.
    """
    site_configuration = SiteConfigurationFactory.create(
        site=self.site,
        page_elements={
            'about': {
                'title': 'About page in Django model.',
            },
        },
    )
    site_configuration.api_adapter = self.api_adapter
    assert site_configuration.get_page_content('about') == {
        'title': 'About page from site configuration service',
    }


def test_secret_without_adapter(self):
    """
    Test `get_secret_value()` without the SiteConfig adapter.
    """
    site_configuration = SiteConfigurationFactory.create(
        site=self.site,
        site_values={
            'SEGMENT_KEY': 'dummy-secret-from-model'
        }
    )
    assert site_configuration.get_secret_value('SEGMENT_KEY') == 'dummy-secret-from-model'


def test_secret_with_adapter(self):
    """
    Ensure `get_secret_value()` uses the SiteConfig adapter when available.
    """
    site_configuration = SiteConfigurationFactory.create(
        site=self.site,
    )
    site_configuration.api_adapter = self.api_adapter
    assert site_configuration.get_secret_value('SEGMENT_KEY') == 'test-secret-from-service'


def test_admin_config_without_adapter(self):
    """
    Test `get_admin_setting()` without the SiteConfig adapter.
    """
    site_configuration = SiteConfigurationFactory.create(
        site=self.site,
        site_values={
            'IDP_TENANT_ID': 'dummy-tenant-in-model'
        }
    )
    assert site_configuration.get_admin_setting('IDP_TENANT_ID') == 'dummy-tenant-in-model'


def test_admin_config_with_adapter(self):
    """
    Ensure `get_admin_setting()` uses the SiteConfig adapter when available.
    """
    site_configuration = SiteConfigurationFactory.create(
        site=self.site,
    )
    site_configuration.api_adapter = self.api_adapter
    assert site_configuration.get_admin_setting('IDP_TENANT_ID') == 'dummy-tenant-id'
