"""

"""
from django.conf import settings


AMC_V1_STRUCTURE_VERSION = 'amc-v1'


def get_backend_config(site_uuid, status='live'):
    # TODO: cache that on request, so we don't do multiple requests
    client = settings.SITE_CONFIG_CLIENT
    return client.get_backend_configs(site_uuid, status)


def get_value(site_uuid, name, default):
    config = get_backend_config(site_uuid)

    # TODO: cache that on request, so we don't convert the json multiple times
    openedx_compatible_json = {
        config_value['name']: config_value['value']
        for config_value in config['settings']
    }

    # TODO: activate that
    # openedx_compatible_json['SEGMENT_KEY'] = config['secrets']['SEGMENT_KEY']

    return openedx_compatible_json.get(name, default)


def get_amc_v1_theme_css_variables(site_uuid):
    config = get_backend_config(site_uuid)

    openedx_theme_compatible_css_vars = {
        config_value['name']: config_value['value']
        for config_value in config['css']
        if config_value['structure_version'] == AMC_V1_STRUCTURE_VERSION
    }

    return openedx_theme_compatible_css_vars


def get_amc_v1_page(site_uuid, page_name):
    config = get_backend_config(site_uuid)

    # TODO: fix and activate this code
    # if config['pages'][page_name]['structure_version'] == AMC_V1_STRUCTURE_VERSION:
    #     return config['pages'][page_name]


"""

###
# Inside: openedx.core.djangoapps.site_configuration
def get_value(name, default):
    # ...
    if settings.SITE_CONFIG_CLEINT_ENABLED:
        site_uuid = 123
        return site_config_client.openedx.adapter.get_value(site_uuid, name, default)
    # ...

    value = 123
    return value

#####
# example code
# Inside: lms/courses/views.py
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
print(configuration_helpers.get_value(
        'ALLOW_AUTOMATED_SIGNUPS',
        settings.FEATURES.get('ALLOW_AUTOMATED_SIGNUPS', False),
))

"""
