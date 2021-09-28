import uuid
from typing import Union


class Client:
    def __init__(self, base_url, api_token, read_only_base_url):
        """
        Instantiate a new API Client
        """
        self.base_url = base_url
        self.api_token = api_token
        self.read_only_base_url = read_only_base_url

    def list_sites(self):
        """
        Returns a list of all Sites
        """
        pass

    def list_active_sites(self):
        """
        Returns a list of all active Sites
        """
        pass

    def get_backend_configs(self, site_uuid: Union[str, uuid.UUID],
                            status: str):
        """
        Returns a combination of Site information, AdminConfiguration setting,
        and `live` or `draft` Configurations (backend secrets included)
        """
        pass

    def get_config(self, site_uuid: Union[str, uuid.UUID],
                   type: str, name: str, status: str):
        """
        Returns a single configuration object for Site
        """
        pass

    def override_configs(self, site_uuid: Union[str, uuid.UUID], configs):
        """
        Override all live configs in a single pass.

        This uses the v0 API which should be deprecated after the initial
        rollout.
        """
        pass
