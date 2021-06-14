import json

import pytest
from flask.testing import FlaskClient
from typing import List, Dict

from FiledInfluencer.Api.InfluencerProfile.schemas import InfluencersResponse
from FiledInfluencer.Api.tests.TestProfiles.utils import InfluencersEndpoint

# List of URLs and corresponding query params
# that need to be tested
end_points: List[InfluencersEndpoint] = [
    InfluencersEndpoint(),
    InfluencersEndpoint(
        page_size=100,
    ),
    InfluencersEndpoint(
        last_influencer_id=50,
        page_size=100,
    ),
    InfluencersEndpoint(name="theo"),
    InfluencersEndpoint(account_type="0"),
    InfluencersEndpoint(account_type="1"),
    InfluencersEndpoint(account_type="3"),
    InfluencersEndpoint(is_verified="true"),
    InfluencersEndpoint(is_verified="false"),
    InfluencersEndpoint(is_verified="both"),
    InfluencersEndpoint(
        engagement_rate_min_count="5",
        engagement_rate_max_count="99",
    ),
    InfluencersEndpoint(
        engagements_per_post_min_count="10",
        engagements_per_post_max_count="1000",
    ),
    InfluencersEndpoint(
        followers_min_count="5_000",
        followers_max_count="10_000_000",
    ),
]


class Default:
    page_size = 100
    last_influencer_id = 0
    response_dict_len = len(InfluencersResponse.__fields__)


@pytest.fixture(params=end_points, scope="session")
def parameterize(request) -> InfluencersEndpoint:
    """
    yields from params
    """
    return request.param


@pytest.fixture(scope="session")
def response(parameterize: InfluencersEndpoint, client: FlaskClient):
    """
    Get response from URL and use query params if available
    """
    return client.get(parameterize.url)


@pytest.fixture(scope="session")
def response_json(response) -> Dict:
    """
    Convert json string to dictionary
    """
    data = response.data.decode("UTF-8")
    return json.loads(data)


@pytest.mark.usefixtures("response")
class TestInfluencerProfile:
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
