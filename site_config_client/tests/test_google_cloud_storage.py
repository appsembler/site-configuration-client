"""
Tests for GoogleCloudStorage
"""
import json
import mock
from mock import Mock
from google.api_core.exceptions import NotFound


@mock.patch('site_config_client.google_cloud_storage.storage.Client')
def test_google_cloud_storage(client):
    mock_gcs_client = client.return_value
    mock_bucket = Mock()
    mock_gcs_client.bucket = mock_bucket()

    json_configs = {
        "site": {
            "uuid": "77d4ee4e-6888-4965-b246-b8629ac65bce",
            "domain_name": "croissant.edu",
            "tier": "trial",
            "always_active": False,
            "subscription_ends": "2021-10-31T16:44:45+0000",
            "is_active": True}
    }

    blob_downloaded_as_bytes = str.encode(json.dumps(json_configs))

    mock_bucket.blob.return_value.download_as_bytes.return_value = (
        blob_downloaded_as_bytes.decode('utf8'))

    expected_string_results = json.dumps(json_configs)
    assert (mock_bucket.blob.return_value.download_as_bytes.return_value ==
            expected_string_results)


@mock.patch('site_config_client.google_cloud_storage.storage.Client')
def test_not_found_exceptions(client):
    mock_gcs_client = client.return_value
    mock_bucket = Mock()
    mock_gcs_client.bucket = mock_bucket
    mock_bucket.blob.return_value.download_as_bytes.return_value = NotFound
    assert (str(mock_bucket.blob.return_value.download_as_bytes.return_value)
            == "<class 'google.api_core.exceptions.NotFound'>")
