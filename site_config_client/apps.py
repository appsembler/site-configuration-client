from django.apps import AppConfig



class SiteConfigApp(AppConfig):
    """
    Django app configs.
    """
    name = 'site_config_client'
    label = 'site_config_client'
    verbose_name = 'Site configuration API client and Open edX plugin.'


class OpenedXSiteConfigApp(SiteConfigApp):
    """
    Open edX app configs.
    """

    @property
    def plugin_app(self):
        from openedx.core.djangoapps.plugins.constants import (
    PluginSettings, ProjectType, SettingsType)

        return {
            PluginSettings.CONFIG: {
                ProjectType.LMS: {
                    SettingsType.PRODUCTION: {
                        PluginSettings.RELATIVE_PATH: 'settings.production'},
                    SettingsType.COMMON: {
                        PluginSettings.RELATIVE_PATH: 'settings.common'},
                }
            },
        }
