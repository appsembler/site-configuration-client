"""
Google cloud read-only storage.
"""

from google.cloud import storage
from google.api_core.exceptions import NotFound


class GoogleCloudStorage:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(self.bucket_name)

    def read(self, file_path):
        blob = self.bucket.get_blob(file_path)
        try:
            return blob.download_as_bytes().decode('utf-8')
        except NotFound:
            raise
