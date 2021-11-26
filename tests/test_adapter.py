"""
Tests for adapter
"""
import pytest
from mock import Mock


CONFIGS = {
    "site": {
        "uuid": "77d4ee4e-6888-4965-b246-b8629ac65bce",
    },
    "status": "live",
    "configuration": {
        "css": {
            "selected_font": "lato",
            "text_color": "#0a0a0a",
            "header_logo_height": "110",
            "header_buttons_color": "#164be0",
            "header_font_size": "17",
        },
        "page": {
            "course-card": "course-tile-01",
            "privacy": {
                "content": [
                    {
                     "element-type": "layout-50:50",
                     "element-path": "page-builder/layouts/_two-col-50-50.html"
                    }
                ]
            }
        },
        "setting": {
            "PLATFORM_NAME": "My New Platform Name!",
            "footer_copyright_text": "© Appsembler 2021. All rights reserved.",
            "display_footer_powered_by": "false",
            "display_footer_legal": "false",
            "google_verification_code": "GoogleVerify!",
            "site_title": "My site title"
        },
        "integration": {},
        "secret": {
            "SEGMENT_KEY": "so secret",
        },
        "admin": {},
        }
}


@pytest.mark.openedx
def test_adapater(settings):
    '''
    I want to mock the return value for `get_backend_config` as CONFIGS
    and test the return values of:
     `get_value`,  `get_amc_v1_theme_css_variables`, `get_amc_v1_page`
    '''
    from site_config_client.openedx import adapter

    uuid = "77d4ee4e-6888-4965"

    mock = Mock()
    mock.get_backend_configs.return_value = CONFIGS
    settings.SITE_CONFIG_CLIENT = mock
    assert adapter.get_backend_config(uuid) == CONFIGS

    setting_platform_name = adapter.get_value(uuid, 'PLATFORM_NAME', None)
    assert setting_platform_name == CONFIGS['configuration']['setting']['PLATFORM_NAME']
    assert adapter.get_value(uuid, 'SEGMENT_KEY') == 'so secret'

    css_vars = adapter.get_amc_v1_theme_css_variables(uuid)
    assert css_vars == CONFIGS['configuration']['css']

    privacy_page_vars = adapter.get_amc_v1_page(uuid, 'privacy')
    assert privacy_page_vars == CONFIGS['configuration']['page']['privacy']
