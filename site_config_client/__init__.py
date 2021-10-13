import json

import requests
import uuid
from typing import Union
from urllib.parse import urljoin

from .exceptions import SiteConfigurationError


class Client:
    def __init__(self, base_url, api_token, read_only_storage=None, cache=None):
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

    def list_sites(self):
        """
        Returns a list of all Sites
        """
        response = requests.get(self.build_url('v1/site/'))
        if response.status == 200:
            return response.json()
        else:
            raise SiteConfigurationError((
                'Something went wrong with the site configuration API '
                '`v1/site/` with status_code="{}" body="{}"'
            ).format(response.status, response.content))

    def list_active_sites(self):
        """
        Returns a list of all active Sites
        """
        data = {
            "is_active": "True"
        }
        response = requests.get(self.build_url('v1/site/'), data=data)
        if response.status == 200:
            return response.json()
        else:
            raise SiteConfigurationError((
                'Something went wrong with the site configuration API '
                '`v1/site/?is_active=True` with status_code="{}" body="{}"'
            ).format(response.status, response.content))

    def get_backend_configs(self, site_uuid: Union[str, uuid.UUID],
                            status: str):
        """
        Returns a combination of Site information and `live` or `draft`
        Configurations (backend secrets included)
        """
        cache_key = 'site_config_client.{}'.format(site_uuid)
        if self.cache:
            config = self.cache.get(cache_key)
            if config:
                return config

        if self.read_only_storage:
            config = self.read_only_storage.read('v1/combined-configuration/backend/{}-{}.json'.format(
                site_uuid, status
            ))
            config = json.loads(config)
        else:
            endpoint = 'v1/combined-configuration/backend/{}/{}/'.format(
                site_uuid, status)
            response = requests.get(self.build_url(endpoint))
            if response.status == 200:
                config = response.json()
            else:
                raise SiteConfigurationError((
                    'Something went wrong with the site configuration API '
                    '`v1/combined-configuration/backend/` with '
                    'status_code="{}" body="{}"'
                ).format(response.status, response.content))

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
        response = requests.get(self.build_url(endpoint), data=data)
        if response.status == 200:
            return response.json()
        else:
            raise SiteConfigurationError((
                'Something went wrong with the site configuration API '
                '`v1/configuration/` with status_code="{}" body="{}"'
            ).format(response.status, response.content))

    def override_configs(self, site_uuid: Union[str, uuid.UUID], configs):
        """
        Override all live configs in a single pass.

        This uses the v0 API which should be deprecated after the initial
        rollout.
        """
        endpoint = 'v0/configuration-override/{}/'.format(site_uuid)
        response = requests.put(self.build_url(endpoint), data=configs)
        if response.status == 200:
            return response.json()
        else:
            raise SiteConfigurationError((
                'Something went wrong with the site configuration API '
                '`v0/configuration-override/` with status_code="{}" body="{}"'
            ).format(response.status, response.content))