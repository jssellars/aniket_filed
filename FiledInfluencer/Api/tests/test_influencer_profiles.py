import json
from dataclasses import dataclass
from typing import List, Optional, Union, Dict

import pytest
from flask.testing import FlaskClient

from FiledInfluencer.Api.schemas import InfluencersResponse


@dataclass
class ResponseParameterize:
    url: str
    # str allowed for testing purpose
    last_influencer_id: Optional[Union[int, str]] = None
    page_size: Optional[Union[int, str]] = None


# List of URLs and corresponding query params
# that need to be tested
end_points: List[ResponseParameterize] = [
    ResponseParameterize(
        url="/api/v1/influencer-profiles",
    ),
    # defaults in end point
    ResponseParameterize(
        url="/api/v1/influencer-profiles?last_influencer_id={}&page_size={}",
        last_influencer_id=0,
        page_size=100,
    ),
    # infinite scroll
    ResponseParameterize(
        url="/api/v1/influencer-profiles?last_influencer_id={}&page_size={}",
        last_influencer_id=150,
        page_size=2,
    ),
    # last_influencer_id is present in url, but no value
    ResponseParameterize(
        url="/api/v1/influencer-profiles?last_influencer_id={}&page_size={}",
        last_influencer_id='',
        page_size=2,
    ),
    # page_size is present in url, but no value
    ResponseParameterize(
        url="/api/v1/influencer-profiles?last_influencer_id={}&page_size={}",
        last_influencer_id=150,
        page_size='',
    ),
    # invalid request
    ResponseParameterize(
        url="/api/v1/influencer-profiles?last_influencer_id={}&page_size={}",
        last_influencer_id=None,
        page_size='invalid',
    ),
    ResponseParameterize(
        url="/api/v1/influencer-profiles?last_influencer_id={}&page_size={}",
        last_influencer_id='invalid',
        page_size=None,
    ),
]


class Default:
    last_influencer_id = 0
    page_size = 100
    response_dict_len = len(InfluencersResponse.__fields__)


@pytest.fixture(params=end_points, scope="session")
def parameterize(request) -> ResponseParameterize:
    """
    Return objects one by one from end_points
    """
    return request.param


@pytest.fixture(scope="session")
def response(parameterize, client: FlaskClient):
    """
    Get response from URL and use query params if available
    """
    last_influencer_id = parameterize.last_influencer_id
    page_size = parameterize.page_size
    url = parameterize.url.format(last_influencer_id, page_size)
    return client.get(url)


@pytest.fixture(scope="session")
def response_json(response) -> Dict:
    """
    Convert json string to dictionary
    """
    data = response.data.decode("UTF-8")
    return json.loads(data)


@pytest.mark.usefixtures("response")
class TestInfluencerProfileInfiniteScroll:
    """
    Test influencer-profiles

    Test all the methods on all objects in end_points
    """

    def test_status_code_200(self, parameterize, response):
        assert response.status_code == 200

    def test_return_type_is_list(self, response_json):
        assert isinstance(response_json, list)

    def test_return_data_not_empty(self, response_json):
        assert len(response_json) > 0

    def test_data_in_list_is_dict(self, response_json):
        for response in response_json:
            assert isinstance(response, dict)

    def test_dict_in_list_has_required_length(self, response_json):
        for response in response_json:
            assert len(response) == Default.response_dict_len

    def test_return_data_page_size(self, parameterize, response_json):
        page_size = parameterize.page_size
        if not isinstance(page_size, int):
            page_size = Default.page_size

        assert len(response_json) == page_size

    def test_return_data_paging_start(self, parameterize, response_json):
        last_influencer_id = parameterize.last_influencer_id
        if not isinstance(last_influencer_id, int):
            last_influencer_id = Default.last_influencer_id

        assert response_json[0]['id'] == last_influencer_id + 1

    def test_return_data_paging_end(self, parameterize, response_json):
        last_influencer_id = parameterize.last_influencer_id
        if not isinstance(last_influencer_id, int):
            last_influencer_id = Default.last_influencer_id

        page_size = parameterize.page_size
        if not isinstance(page_size, int):
            page_size = Default.page_size

        assert response_json[-1]['id'] == last_influencer_id + page_size
