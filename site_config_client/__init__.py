import json
import requests
from typing import Union
import uuid
from urllib.parse import urljoin

from .exceptions import SiteConfigurationError


class Client:
    def __init__(self, base_url, api_token,
                 read_only_storage=None, cache=None):
        """
        Instantiate a new API Client
        """
        self.base_url = base_url
        self.api_token = api_token
        self.read_only_storage = read_only_storage
        self.cache = cache

    def build_url(self, endpoint):
        full_path = urljoin(self.base_url, endpoint)
        return full_path

    def create_site(self, domain_name, site_uuid=None):
        """
        Create a new site.
        """
        params = {'domain_name': domain_name}
        if site_uuid:
            params['uuid'] = site_uuid

        auth_headers = {'Authorization': 'Token {}'.format(self.api_token)}
        response = requests.post(self.build_url('v1/site/'),
                                 headers=auth_headers, json=params)
        if response.status_code == 201:
            return response.json()
        else:
            raise SiteConfigurationError((
                'Something went wrong with the site configuration API '
                '`v1/site/` with status_code="{}" body="{}"'
            ).format(response.status_code, response.content))

    def list_sites(self):
        """
        Returns a list of all Sites
        """
        auth_headers = {'Authorization': 'Token {}'.format(self.api_token)}
        response = requests.get(self.build_url('v1/site/'),
                                headers=auth_headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise SiteConfigurationError((
                'Something went wrong with the site configuration API '
                '`v1/site/` with status_code="{}" body="{}"'
            ).format(response.status_code, response.content))

    def list_active_sites(self):
        """
        Returns a list of all active Sites
        """
        auth_headers = {'Authorization': 'Token {}'.format(self.api_token)}
        response = requests.get(self.build_url('v1/site/?is_active=True'),
                                headers=auth_headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise SiteConfigurationError((
                'Something went wrong with the site configuration API '
                '`v1/site/?is_active=True` with status_code="{}" body="{}"'
            ).format(response.status_code, response.content))

    def get_backend_configs(self, site_uuid: Union[str, uuid.UUID],
                            status: str):
        """
        Returns a combination of Site information and `live` or `draft`
        Configurations (backend secrets included)

        [Client Configuration]
        - Django Cache
            - if cache key exists: return config from cache
            - if cache key does not exist: call endpoint to get config, set
              cache with config, return config
        """
        cache_key = 'site_config_client.{}.{}'.format(site_uuid, status)
        if self.cache:
            config = self.cache.get(key=cache_key)
            if config:
                return config

        endpoint = 'v1/combined-configuration/backend/{}/{}/'.format(
            site_uuid, status)
        auth_headers = {'Authorization': 'Token {}'.format(self.api_token)}
        response = requests.get(self.build_url(endpoint),
                                headers=auth_headers)
        if response.status_code == 200:
            config = response.json()
        else:
            raise SiteConfigurationError((
                'Something went wrong with the site configuration API '
                '`v1/combined-configuration/backend/` with '
                'status_code="{}" body="{}"'
            ).format(response.status_code, response.content))

        if self.cache:
            self.cache.set(cache_key, config)
        return config

    def get_config(self, site_uuid: Union[str, uuid.UUID],
                   type: str, name: str, status: str):
        """
        Returns a single configuration object for Site
        """
        endpoint = 'v1/configuration/{}/'.format(site_uuid)
        data = {
            "type": type,
            "name": name,
            "status": status
        }
        auth_headers = {'Authorization': 'Token {}'.format(self.api_token)}
        response = requests.get(self.build_url(endpoint),
                                headers=auth_headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise SiteConfigurationError((
                'Something went wrong with the site configuration API '
                '`v1/configuration/` with status_code="{}" body="{}"'
            ).format(response.status_code, response.content))

    def override_configs(self, site_uuid: Union[str, uuid.UUID], configs):
        """
        Override all live configs in a single pass.

        This uses the v0 API which should be deprecated after the initial
        rollout.
        """
        endpoint = 'v0/configuration-override/{}/'.format(site_uuid)
        auth_headers = {'Authorization': 'Token {}'.format(self.api_token),
                        'content-type': 'application/json'}
        response = requests.put(self.build_url(endpoint),
                                data=json.dumps(configs),
                                headers=auth_headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise SiteConfigurationError((
                'Something went wrong with the site configuration API '
                '`v0/configuration-override/` with status_code="{}" body="{}"'
            ).format(response.status_code, response.content))
