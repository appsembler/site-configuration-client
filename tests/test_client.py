"""
Tests for Client
"""
import pytest

from site_config_client import Client
from site_config_client.exceptions import SiteConfigurationError


SITES = {
    "count": 2,
    "results": [
            {
                "uuid": "77d4ee4e-6888-4965-b246-b8629ac65bce",
                "domain_name": "croissant.edu",
                "tier": "trial",
                "always_active": "False",
                "subscription_ends": "2021-10-31T16:44:45+0000",
                "is_active": "True"
            },
            {
                "uuid": "040e0ec3-2578-4fcf-b5db-030dadf68f30",
                "domain_name": "test-site.com",
                "tier": "trial",
                "always_active": "False",
                "subscription_ends": "2021-10-31T16:44:45+0000",
                "is_active": "True"
            }
        ]
}


CONFIGS = {
    "site": {
                "uuid": "77d4ee4e-6888-4965-b246-b8629ac65bce",
                "domain_name": "croissant.edu",
                "tier": "trial",
                "always_active": "False",
                "subscription_ends": "2021-10-31T16:44:45+0000",
                "is_active": "True"
            },
    "status": "draft",
    "configuration":
        {
            "css": [
                    {"name": "accent-font",
                     "value": "monospace"}
                    ],
            "page": [],
            "setting": [
                        {"name": "PLATFORM_NAME",
                         "value": "Momofuku Academy"}
                        ],
            "integration": [],
            "secret": [],
            "admin": [
                      {"name": "features",
                       "value": ["bi_connector", "google_tag_manageer"]}
                    ]
        }
}


SINGLE_CONFIG = {
        "site_uuid": "77d4ee4e-6888-4965-b246-b8629ac65bce",
        "name": "PLATFORM_NAME",
        "value": "Academy of Modern Arts",
        "author_email": "test@example.com",
        "structure_version": "amc-v1",
        "modified": "2021-09-30T16:00:42+0000"
    }


OVERRIDE_CONFIGS = {
        'author_email': 'test@example.com',
        'css': [{
            'name': '$brand-primary-color',
            'value': ['rgba(0,1,1,1)', 'rgba(0,1,1,1)']
        }]
    }


PARAMS = {
    "uuid": "77d4ee4e-6888-4965-b246-b8629ac65bce"
}


def test_client():
    base = "http://127.0.0.1:8000"
    token = "abcaseasyas123"
    bucket = "http://storage.googleapis.com/appsembler/site_config"
    c = Client(base_url=base,
               api_token=token,
               read_only_storage=bucket)

    assert c.base_url == base
    assert c.api_token == token
    assert c.read_only_storage == bucket


@pytest.fixture
def site_config_client():
    client = Client(
                base_url="http://service",
                api_token="some-token",
                read_only_storage=None,
    )
    return client


def test_url(site_config_client):
    site_endpoint = site_config_client.build_url('v1/site/')
    assert site_endpoint == "http://service/v1/site/"


def test_list_sites(site_config_client, requests_mock):
    site_path = "http://service/v1/site/"
    requests_mock.get(site_path, json=SITES, status_code=200)
    response_sites = site_config_client.list_sites()
    assert response_sites == SITES


def test_list_sites_with_error(site_config_client, requests_mock):
    site_path = "http://service/v1/site/"
    requests_mock.get(site_path, json=SITES, status_code=404)

    with pytest.raises(SiteConfigurationError):
        site_config_client.list_sites()


def test_list_active_sites(site_config_client, requests_mock):
    active_sites_path = "http://service/v1/site/?is_active=True"
    requests_mock.get(active_sites_path, json=SITES, status_code=200)
    response_active_sites = site_config_client.list_active_sites()
    assert response_active_sites == SITES


def test_list_active_sites_error(site_config_client, requests_mock):
    active_sites_path = "http://service/v1/site/?is_active=True"
    requests_mock.get(active_sites_path, json=SITES, status_code=404)

    with pytest.raises(SiteConfigurationError):
        site_config_client.list_active_sites()


def test_get_backend_configs(requests_mock, site_config_client):
    backend_draft_configs_path = (
        'http://service/v1/combined-configuration/backend/{}/draft/'
        .format(PARAMS['uuid']))
    requests_mock.get(backend_draft_configs_path,
                      json=CONFIGS, status_code=200)
    response_configs = site_config_client.get_backend_configs(
        site_uuid=PARAMS['uuid'], status='draft')
    assert response_configs == CONFIGS, (
        'Neither cache nor google cloud storage configured')


def test_get_backend_configs_error(requests_mock, site_config_client):
    backend_draft_configs_path = (
        'http://service/v1/combined-configuration/backend/{}/draft/'
        .format(PARAMS['uuid']))
    requests_mock.get(backend_draft_configs_path,
                      json=CONFIGS, status_code=404)

    with pytest.raises(SiteConfigurationError):
        site_config_client.get_backend_configs(
            site_uuid=PARAMS['uuid'], status='draft')


def test_get_config(requests_mock, site_config_client):
    config_path = "http://service/v1/configuration/{}/".format(PARAMS['uuid'])
    requests_mock.get(config_path,
                      json=SINGLE_CONFIG, status_code=200)
    response_configs = site_config_client.get_config(
        site_uuid=PARAMS['uuid'],
        type="setting",
        name="PLATFORM_NAME",
        status="live")
    assert response_configs == SINGLE_CONFIG


def test_get_config_error(requests_mock, site_config_client):
    config_path = "http://service/v1/configuration/{}/".format(PARAMS['uuid'])

    requests_mock.get(config_path,
                      json=SINGLE_CONFIG, status_code=404)

    with pytest.raises(SiteConfigurationError):
        site_config_client.get_config(
            site_uuid=PARAMS['uuid'],
            type="setting",
            name="PLATFORM_NAME",
            status="live")


def test_override_configs(requests_mock, site_config_client):
    override_path = (
        "http://service/v0/configuration-override/{}/"
        .format(PARAMS['uuid']))
    success_response = {
        "developer_message": "Configurations has been overriden successfully."
        }
    requests_mock.put(override_path, json=success_response, status_code=200)
    override_response = site_config_client.override_configs(
        site_uuid=PARAMS['uuid'], configs=OVERRIDE_CONFIGS)
    assert override_response == success_response


def test_override_configs_error(requests_mock, site_config_client):
    override_path = (
        "http://service/v0/configuration-override/{}/"
        .format(PARAMS['uuid']))

    requests_mock.put(override_path, status_code=500)

    with pytest.raises(SiteConfigurationError):
        site_config_client.override_configs(
            site_uuid=PARAMS['uuid'], configs=OVERRIDE_CONFIGS)
