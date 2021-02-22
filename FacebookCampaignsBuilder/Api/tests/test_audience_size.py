import pytest
import json


class TestAudienceSize:

    post_data = {
        "optimizationGoal": "OFFSITE_CONVERSIONS",
        "targetingSpec": {
            "custom_audiences": [],
            "excluded_custom_audiences": [],
            "excluded_connections": [],
            "friends_of_connections": [],
            "connections": [],
            "genders": [0],
            "age_min": 18,
            "age_max": 57,
            "geo_locations": {
                "countries": ["US"],
                "location_types": ["home", "recent"],
            },
            "locales": [6],
            "flexible_spec": [],
            "exclusions": {},
            "targeting_optimization": "none",
            "publisher_platforms": [
                "audience_network",
                "facebook",
                "instagram",
                "messenger",
            ],
            "facebook_positions": [
                "feed",
                "instant_article",
                "video_feeds",
                "right_hand_column",
                "marketplace",
                "story",
                "instream_video",
                "search",
            ],
            "instagram_positions": ["stream", "story", "explore"],
            "messenger_positions": ["messenger_home", "story"],
            "audience_network_positions": [
                "classic",
                "rewarded_video",
                "instream_video",
            ],
            "device_platforms": ["mobile", "desktop"],
            "brand_safety_content_filter_levels": ["FACEBOOK_STANDARD"],
        },
    }

    @pytest.fixture(scope="session")
    def response(self, client, config):
        url = f"/api/v1/audience-size/{config['account_id']}"
        return client.post(url, json=self.post_data, headers=config["headers"])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        return json.loads(data)

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_dict(self, response):
        data = response.data.decode("UTF-8")
        assert isinstance(json.loads(data), dict)

    def test_return_data_is_length_one(self, response_json):
        assert len(response_json) == 1

    def test_audience_size_param_is_positive_integer(self, response_json):
        assert "audienceSize" in response_json
        audience_size = response_json.get("audienceSize")
        assert isinstance(audience_size, int)
        assert audience_size >= 0
