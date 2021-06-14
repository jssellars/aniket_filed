import json

import pytest
import requests
from flask.testing import FlaskClient
from typing import Dict

from FiledInfluencer.Api.AWSDocuments.schemas import DocumentsResponse
from FiledInfluencer.Api.tests.TestDocuments.utils import test_file


@pytest.fixture(scope="session")
def response(client: FlaskClient):
    """
    Get response from URL and use query params if available
    """
    url = 'api/v1/documents'

    result = client.post(
        url,
        buffered=True,
        data={
            'documents': test_file,
            "campaign_name": "test-campaign",
            "campaign_id": 1,
            "is_contract": True,
        },
        content_type="multipart/form-data",
    )

    return result


@pytest.fixture(scope="session")
def response_json(response) -> Dict:
    """
    Convert json string to dictionary
    """
    data = response.data.decode("UTF-8")
    return json.loads(data)


@pytest.fixture(scope="session")
def response_download(client: FlaskClient, response_json):
    """
    Get response from URL and use query params if available
    """
    key = response_json['location']
    url = f'api/v1/documents?key={key}'
    result = client.get(url)

    return result


@pytest.fixture(scope="session")
def response_download_json(response_download) -> Dict:
    """
    Convert json string to dictionary
    """
    data = response_download.data.decode("UTF-8")
    return json.loads(data)


@pytest.fixture(scope="session")
def response_delete(client: FlaskClient, response_json):
    """
    Get response from URL and use query params if available
    """
    key = response_json['location']
    url = f'api/v1/documents?key={key}'
    result = client.delete(url)

    return result


@pytest.fixture(scope="session")
def response_delete_json(response_delete) -> str:
    """
    Convert json string to dictionary
    """
    data = response_delete.data.decode("UTF-8").strip()
    return data


class Default:
    response_dict_len = len(DocumentsResponse.__fields__)


@pytest.mark.usefixtures(scope="session")
class TestDocumentUpload:
    """
    Test document upload

    Test all the methods on all objects in end_points
    """

    def test_status_code_200(self, response):
        print(response.status_code)
        assert response.status_code == 200

    def test_return_type_is_dict(self, response_json):
        assert isinstance(response_json, dict)

    def test_return_data_not_empty(self, response_json):
        assert len(response_json) > 0

    def test_dict_in_list_has_required_length(self, response_json):
        assert len(response_json) == Default.response_dict_len


@pytest.mark.usefixtures(scope="session")
class TestDocumentDownload:
    """
    Test document download
    """

    def test_status_code_200(self, response_download):
        assert response_download.status_code == 200

    def test_return_type_is_dict(self, response_download_json):
        assert isinstance(response_download_json, dict)

    def test_return_data_not_empty(self, response_download_json):
        assert len(response_download_json) > 0

    def test_dict_has_required_length(self, response_download_json):
        assert len(response_download_json) == 1

    def test_download_url(self, response_download_json):
        url = response_download_json['url']
        result = requests.get(url)
        assert result.status_code == 200


@pytest.mark.usefixtures(scope="session")
class TestDocumentDelete:
    """
    Test document delete
    """

    def test_status_code_200(self, response_delete):
        assert response_delete.status_code == 200

    def test_return_type_is_dict(self, response_delete_json):
        assert isinstance(response_delete_json, str)

    def test_return_data_not_empty(self, response_delete_json):
        assert len(response_delete_json) > 0

    def test_dict_has_required_length(self, response_delete_json):
        assert response_delete_json == "true"
