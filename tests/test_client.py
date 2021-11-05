"""
Tests for Client
"""
import pytest
import requests

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


def test_client():
    base = "http://127.0.0.1:8000"
    token = "abcaseasyas123"
    bucket = "http://storage.googleapis.com/appsembler/site_config"
    c = Client(base_url=base,
               api_token=token,
               read_only_base_url=bucket)

    assert c.base_url == base
    assert c.api_token == token
    assert c.read_only_base_url == bucket


@pytest.fixture
def site_config_client():
    client = Client(
                base_url="http://service",
                api_token="some-token",
                read_only_base_url="http://some-bucket",
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


def test_list_active_sites(requests_mock):
    active_sites_path = "http://127.0.0.1:8000/v1/site/?is_active=True"
    sites = {
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
    requests_mock.get(active_sites_path, json=sites, status_code=200)
    r = requests.get(active_sites_path)
    assert r.json() == sites
    assert r.status_code == 200


def test_get_backend_configs(requests_mock):
    backend_draft_configs_path = (
        "http://127.0.0.1:8000/v1/combined-configuration/backend/"
        "77d4ee4e-6888-4965-b246-b8629ac65bce/draft/")
    configs = {
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
    requests_mock.get(backend_draft_configs_path,
                      json=configs, status_code=200)
    r = requests.get(backend_draft_configs_path)
    assert r.json() == configs


def test_get_config(requests_mock):
    config_path = (
        "http://127.0.0.1:8000/v1/configuration/"
        "77d4ee4e-6888-4965-b246-b8629ac65bce/"
        "?type=setting&name=PLATFORM_NAME&status=live")
    config = {
        "site_uuid": "77d4ee4e-6888-4965-b246-b8629ac65bce",
        "name": "PLATFORM_NAME",
        "value": "Academy of Modern Arts",
        "author_email": "test@example.com",
        "structure_version": "amc-v1",
        "modified": "2021-09-30T16:00:42+0000"
    }
    requests_mock.get(config_path,
                      json=config, status_code=200)
    r = requests.get(config_path)
    assert r.json() == config
    assert r.status_code == 200


def test_override_configs(requests_mock):
    override_path = (
        "http://127.0.0.1:8000/v0/configuration-override/"
        "77d4ee4e-6888-4965-b246-b8629ac65bce/")
    resp = {
        "developer_message": "Configurations has been overriden successfully."
        }
    requests_mock.put(override_path, json=resp, status_code=200)
    r = requests.put(override_path)
    assert r.json() == resp
    assert r.status_code == 200