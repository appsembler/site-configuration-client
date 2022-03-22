"""
External Open edX Python API helpers goes here.

### API Contract:
 * Those APIs should be stable and abstract internal changes.

 * Non-stable and internal APIs should be placed in other modules.

 * The parameters of existing functions should change in a backward compatible way:
   - No parameters should be removed from the function
   - New parameters should have safe defaults
 * For breaking changes, new functions should be created
"""


try:
    from crum import get_current_request
except ImportError:
    # Silence the initial import error, but runtime errors will occur in tests and non-Open edX environments.
    # In tests, `get_current_request` can be mocked.
    get_current_request = None

try:
    from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
except ImportError:
    # Silence the initial import error, but runtime errors will occur in tests and non-Open edX environments.
    # In tests, `configuration_helpers` can be mocked.
    configuration_helpers = None


from .adapter import SiteConfigAdapter


def get_current_configuration():
    """
    Gets current site configuration.
    """
    return configuration_helpers.get_current_site_configuration()


def get_current_site_config_client_adapter(request=None):
    if not request:
        request = get_current_request()

    if not request:
        raise RuntimeError('get_current_site_config_client_adapter: request needs to be provided')

    api_adapter = getattr(request, 'site_config_client_adapter', None)
    if not api_adapter:
        # Tahoe: Import is placed here to avoid model import at project startup
        from openedx.core.djangoapps.appsembler.sites import (
            site_config_client_helpers as site_helpers,
        )
        if site_helpers.is_enabled_for_site(instance.site):
            api_adapter = SiteConfigAdapter(uuid)

    return api_adapter


def get_setting_value(name, default=None, site_configuration=None):
    """
    Return Configuration value for the key specified as name argument.

    Function logs a message if configuration is not enabled or if there is an error retrieving a key.

    Args:
        name (str): Name of the key for which to return configuration value.
        default: default value tp return if key is not found in the configuration
        site_configuration: The SiteConfiguration instance, defaults to `get_current_configuration()`.

    Returns:
        Configuration value for the given key or returns `None` if configuration is not enabled.
    """
    if not site_configuration:
        site_configuration = get_current_configuration()
    
    return site_configuration.get_value(name, default)


def get_admin_value(name, default=None, site_configuration=None):
    """
    Get `admin` setting from the site configuration service.

    If SiteConfiguration adapter isn't in use, fallback to the deprecated `SiteConfiguration.site_values` field.

    Args:
        name (str): Name of the setting to fetch.
        default: default value to return if setting is not found in the configuration.
        site_configuration: The SiteConfiguration instance, defaults to `get_current_configuration()`.

    Returns:
        Value for the given key or returns `None` if not configured.
    """
    if site_configuration.api_adapter:
        # Tahoe: Use `SiteConfigAdapter` if available.
        return site_configuration.api_adapter.get_value_of_type(SiteConfigAdapter.TYPE_ADMIN, name, default)
    else:
        return site_configuration.site_values.get(name, default)


def get_page_value(name, default=None, site_configuration=None):
    """
    Get page content from Site Configuration service settings.

    If SiteConfiguration adapter isn't in use, fallback to the deprecated `SiteConfiguration.page_elements` field.

    Args:
        name (str): Name of the page to fetch.
        default: default value to return if page is not found in the configuration.
        site_configuration: The SiteConfiguration instance, defaults to `get_current_configuration()`.

    Returns:
        Page content `dict`.
    """
    if not site_configuration:
        site_configuration = get_current_configuration()

    if site_configuration.api_adapter:
        # Tahoe: Use `SiteConfigAdapter` if available.
        return site_configuration.api_adapter.get_value_of_type(SiteConfigAdapter.TYPE_PAGE, name, default)
    else:
        return site_configuration.page_elements.get(name, default)


def get_secret_value(name, default=None, site_configuration=None):
    """
    Tahoe: Get `secret` value from the site configuration service.

    If SiteConfiguration adapter isn't in use, fallback to the deprecated `SiteConfiguration.site_values` field.

    Args:
        name (str): Name of the secret to fetch.
        default: default value to return if secret is not found in the configuration.
        site_configuration: The SiteConfiguration instance, defaults to `get_current_configuration()`.

    Returns:
        Value for the given key or returns `None` if not configured.
    """
    if site_configuration.api_adapter:
        # Tahoe: Use `SiteConfigAdapter` if available.
        return site_configuration.api_adapter.get_value_of_type(SiteConfigAdapter.TYPE_SECRET, name, default)
    else:
        return site_configuration.site_values.get(name, default)

