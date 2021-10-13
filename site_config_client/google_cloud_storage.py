"""
Google cloud read-only storage.
"""

from google.cloud import storage
from google.cloud.exceptions import NotFound


class GoogleCloudStorage:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(self.bucket_name)

    def read(self, file_path):
        blob = self.bucket.get_blob('get_blob')
        try:
            return blob.download_as_bytes(file_path).decode('utf-8')
        except NotFound:
            # TODO: Handle it better may via SiteConfiguraitonError
            raise
