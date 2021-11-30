"""
"""
from django.conf import settings


AMC_V1_STRUCTURE_VERSION = 'amc-v1'


class SiteConfigAdapter:
    """
    Adapter for Open edX translates the values in a format that Open edX can use.
    """

    backend_configs = None

    def __init__(self, site_uuid):
        self.site_uuid = site_uuid

    def get_backend_configs(self, status='live'):
        if not self.backend_configs:
            client = settings.SITE_CONFIG_CLIENT
            self.backend_configs = client.get_backend_configs(self.site_uuid, status)
        return self.backend_configs

    def get_value(self, name, default=None):
        """
        Returns config value for config type `setting`.
        """
        site_values = self.get_site_values()
        return site_values.get(name, default)

    def get_site_values(self):
        config = self.get_backend_configs()['configuration']
        openedx_compatible_json = config['setting']

        # TODO: Update our segment classes to use secrets and remove this line
        openedx_compatible_json['SEGMENT_KEY'] = config['secret'].get('SEGMENT_KEY')
        return openedx_compatible_json

    def get_amc_v1_theme_css_variables(self):
        config = self.get_backend_configs()['configuration']
        openedx_theme_compatible_css_vars = config['css']
        # NOTE: This function assumes that all varialbes are compativle with v1 theme.
        return openedx_theme_compatible_css_vars

    def get_amc_v1_page(self, page_name):
        config = self.get_backend_configs()['configuration']
        openedx_theme_compatible_page_vars = config['page'][page_name]
        return openedx_theme_compatible_page_vars
