from django.apps import AppConfig

try:
    from openedx.core.djangoapps.plugins.constants import (
        PluginSettings,
        ProjectType,
        SettingsType,
    )
    OPENEDX_ENVIRONMENT = True
except ImportError:
    OPENEDX_ENVIRONMENT = False


class SiteConfigApp(AppConfig):
    """
    Django and Open edX app configs.
    """
    name = 'site_config_client'
    label = 'site_config_client'
    verbose_name = 'Site configuration API client and Open edX plugin.'

    if OPENEDX_ENVIRONMENT:
        # Open edX-specific configurations. This is not used by Django-only environment.
        plugin_app = {
            PluginSettings.CONFIG: {
                ProjectType.LMS: {
                    SettingsType.PRODUCTION: {
                        PluginSettings.RELATIVE_PATH: 'settings.production'},
                    SettingsType.COMMON: {
                        PluginSettings.RELATIVE_PATH: 'settings.common'},
                },
            },
        }
