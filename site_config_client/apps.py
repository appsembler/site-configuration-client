from django.apps import AppConfig
from openedx.core.djangoapps.plugins.constants import PluginSettings, ProjectType, SettingsType


class SiteConfigApp(AppConfig):
    name = 'site_config_client'
    label = 'site_config_client'
    verbose_name = 'Site configuration API client and Open edX plugin.'

    plugin_app = {
        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                SettingsType.COMMON: {PluginSettings.RELATIVE_PATH: 'openedx.settings.common'},
            }
        },
    }
