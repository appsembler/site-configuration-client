"""
"""
from django.conf import settings


AMC_V1_STRUCTURE_VERSION = 'amc-v1'


def get_backend_config(site_uuid, status='live'):
    client = settings.SITE_CONFIG_CLIENT
    return client.get_backend_configs(site_uuid, status)


def get_value(site_uuid, name, default=None):
    '''
    Returns config value for config type `setting`

    ** STEPS **
    1. Config retrieved via the Client.get_backend_configs()
       Example Response:
            {
                "site": {...},
                "status": "live",
                "configuration": {...}
                "integration": {...},
                "secret": {...},
                "admin": {...}
            }

    2. Get `configuration` field from response
        Example `configuration`:
            {
                "css": {
                    "selected_font “": "lato",
                    "text_color": "#0a0a0a",
                    "header_logo_height": "110",
                },
                "page": {},
                "setting": {
                    "PLATFORM_NAME": "My New Platform Name!",
                    "site_name": "My site name",
                    "footer_copyright_text": "© Appsembler 2021. All rights reserved.1",
                    "display_footer_powered_by": "false",
                    }
                }
            }

    3. Return values for configuration['setting']
        Example:
            {
                "PLATFORM_NAME": "My New Platform Name!",
                "site_name": "My site name",
                "footer_copyright_text": "© Appsembler 2021. All rights reserved.1",
                "display_footer_powered_by": "false",
            }


    '''
    config = get_backend_config(site_uuid)['configuration']
    openedx_compatible_json = config['setting']

    # TODO: Update out segment classes to use secrets and remove this line
    openedx_compatible_json['SEGMENT_KEY'] = config['secret'].get('SEGMENT_KEY')

    return openedx_compatible_json.get(name, default)


def get_amc_v1_theme_css_variables(site_uuid):
    config = get_backend_config(site_uuid)['configuration']

    openedx_theme_compatible_css_vars = config['css']
    # NOTE: This function assumes that all varialbes are compativle with v1 theme.
    return openedx_theme_compatible_css_vars


def get_amc_v1_page(site_uuid, page_name):
    config = get_backend_config(site_uuid)['configuration']
    openedx_theme_compatible_page_vars = config['page'][page_name]
    return openedx_theme_compatible_page_vars
