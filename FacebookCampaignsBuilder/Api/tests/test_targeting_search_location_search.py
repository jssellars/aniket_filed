import pytest
import json
from enum import Enum


class TargetingSearchLocationSearchField(Enum):
    KEY = "key"
    NAME = "name"
    TYPE = "type"
    COUNTRY_CODE = "countryCode"
    COUNTRY_NAME = "countryName"
    REGION = "region"
    REGION_ID = "regionId"
    SUPPORT_REGION = "supportsRegion"
    SUPPORT_CITY = "supportsCity"
    GEO_HIERARCHY_LEVEL = "geoHierarchyLevel"
    GEO_HIERARCHY_NAME = "geoHierarchyName"


class TestTargetingSearchLocationSearch:
    @pytest.fixture(scope="session", params=["romania"])
    def response(self, client, config, request):
        url = f"/api/v1/targeting-search/locations/search/{request.param}"
        return client.get(url, headers=config["headers"])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        return json.loads(data)

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_list(self, response_json):
        assert isinstance(response_json, list)

    def test_data_in_list_is_non_empty_dict(self, response_json):
        for response in response_json:
            assert isinstance(response, dict)
            assert len(response) > 0

    def test_key_is_numeric_string(self, response_json):
        for response in response_json:
            assert TargetingSearchLocationSearchField.KEY.value in response
            key = response.get(TargetingSearchLocationSearchField.KEY.value)
            assert isinstance(key, str)
            assert len(key) > 0
            if key != response.get(
                TargetingSearchLocationSearchField.COUNTRY_CODE.value
            ):
                assert key.isnumeric()

    def test_name_is_non_empty_string(self, response_json):
        for response in response_json:
            assert TargetingSearchLocationSearchField.NAME.value in response
            name = response.get(TargetingSearchLocationSearchField.NAME.value)

            assert isinstance(name, str)
            assert len(name) > 0

    def test_type_is_non_empty_string(self, response_json):
        for response in response_json:
            assert TargetingSearchLocationSearchField.TYPE.value in response
            _type = response.get(TargetingSearchLocationSearchField.TYPE.value)
            assert isinstance(_type, str)
            assert len(_type) > 0

    def test_country_code_is_string_with_len_2(self, response_json):
        for response in response_json:
            assert TargetingSearchLocationSearchField.COUNTRY_CODE.value in response
            country_code = response.get(
                TargetingSearchLocationSearchField.COUNTRY_CODE.value
            )
            assert isinstance(country_code, str)
            assert len(country_code) == 2

    def test_country_name_is_non_empty_string(self, response_json):
        for response in response_json:
            assert TargetingSearchLocationSearchField.COUNTRY_NAME.value in response
            country_name = response.get(
                TargetingSearchLocationSearchField.COUNTRY_NAME.value
            )
            assert isinstance(country_name, str)
            assert len(country_name) > 0

    def test_supports_region_is_bool(self, response_json):
        for response in response_json:
            assert TargetingSearchLocationSearchField.SUPPORT_REGION.value in response
            supports_region = response.get(
                TargetingSearchLocationSearchField.SUPPORT_REGION.value
            )
            assert isinstance(supports_region, bool)

    def test_supports_city_is_bool(self, response_json):
        for response in response_json:
            assert TargetingSearchLocationSearchField.SUPPORT_CITY.value in response
            support_city = response.get(
                TargetingSearchLocationSearchField.SUPPORT_CITY.value
            )
            assert isinstance(support_city, bool)

    def test_region_is_non_empty_string(self, response_json):
        for response in response_json:
            region = response.get(TargetingSearchLocationSearchField.REGION.value)
            if region:
                assert isinstance(region, str)
                assert len(region) > 0

    def test_region_id_is_positive_int(self, response_json):
        for response in response_json:
            region_id = response.get(TargetingSearchLocationSearchField.REGION_ID.value)
            if region_id:
                assert isinstance(region_id, int)
                assert region_id > 0

    def test_geo_hierarchy_name_is_non_empty_string(self, response_json):
        for response in response_json:
            geo_hierarchy_name = response.get(
                TargetingSearchLocationSearchField.GEO_HIERARCHY_NAME.value
            )
            if geo_hierarchy_name:
                assert isinstance(geo_hierarchy_name, str)
                assert len(geo_hierarchy_name) > 0

    def test_geo_hierarchy_level_is_non_empty_string(self, response_json):
        for response in response_json:
            geo_hierarchy_level = response.get(
                TargetingSearchLocationSearchField.GEO_HIERARCHY_LEVEL.value
            )
            if geo_hierarchy_level:
                assert isinstance(geo_hierarchy_level, str)
                assert len(geo_hierarchy_level) > 0
