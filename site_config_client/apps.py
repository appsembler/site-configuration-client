from django.apps import AppConfig
from openedx.core.djangoapps.plugins.constants import (
    PluginSettings, ProjectType, SettingsType)


class SiteConfigApp(AppConfig):
    """
    Provides edX configuration for Site Configuration
    """
    name = 'site_config_client'
    label = 'site_config_client'
    verbose_name = 'Site configuration API client and Open edX plugin.'

    plugin_app = {
        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                SettingsType.PRODUCTION: {
                    PluginSettings.RELATIVE_PATH: 'settings.production'},
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: 'settings.common'},
            }
        },
    }
