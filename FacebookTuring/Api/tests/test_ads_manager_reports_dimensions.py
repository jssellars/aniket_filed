import json
from enum import Enum

import pytest


class AdsManagerReportsDimensionsField(Enum):
    V_AD_INSIGHTS = "vAdInsights"
    V_AD_SET_INSIGHTS = "vAdSetInsights"
    V_CAMPAIGN_INSIGHTS = "vCampaignInsights"
    ID = "id"
    DISPLAY_NAME = "displayName"
    PRIMARY_VALUE = "primaryValue"
    SECONDARY_VALUE = "secondaryValue"
    TYPE_ID = "typeId"
    ACTIONS = "actions"
    CATEGORY_ID = "categoryId"
    WIDTH = "width"
    IS_FIXED = "isFixed"
    GROUP_DISPLAY_NAME = "groupDisplayName"
    HIDDEN = "hidden"
    IS_FILTERABLE = "isFilterable"
    IS_EDITABLE = "isEditable"
    IS_SORTABLE = "isSortable"
    NO_OF_DECIMALS = "noOfDecimals"
    PINNED = "pinned"
    DESCRIPTION = "description"
    IS_TOGGLE = "isToggle"
    NAME = "name"
    AGGREGATE_ID = "aggregationId"
    VALUE = "value"


class TestAdsManagerReportsDimensions:
    @pytest.fixture(scope="session")
    def response(self, client, config):
        url = f"/api/v1/get-dimensions"
        return client.get(url, headers=config["headers"])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        return json.loads(data)

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_dict_of_len_three(self, response_json):
        assert isinstance(response_json, dict)
        assert len(response_json) == 3

    def test_ad_insights_is_non_empty_list(self, response_json):
        ad_insights_data = response_json.get(AdsManagerReportsDimensionsField.V_AD_INSIGHTS.value)
        assert isinstance(ad_insights_data, list)
        assert len(ad_insights_data) >= 0

    def test_ad_set_insights_is_non_empty_list(self, response_json):
        ad_set_insights_data = response_json.get(AdsManagerReportsDimensionsField.V_AD_SET_INSIGHTS.value)
        assert isinstance(ad_set_insights_data, list)
        assert len(ad_set_insights_data) >= 0

    def test_campaign_insights_is_non_empty_list(self, response_json):
        campaigns_insights_data = response_json.get(AdsManagerReportsDimensionsField.V_CAMPAIGN_INSIGHTS.value)
        assert isinstance(campaigns_insights_data, list)
        assert len(campaigns_insights_data) >= 0

    @pytest.fixture(scope="session")
    def all_data(self, response_json):
        data = (
            response_json.get(AdsManagerReportsDimensionsField.V_AD_INSIGHTS.value)
            + response_json.get(AdsManagerReportsDimensionsField.V_AD_SET_INSIGHTS.value)
            + response_json.get(AdsManagerReportsDimensionsField.V_CAMPAIGN_INSIGHTS.value)
        )
        return data

    def test_id_is_non_empty_string(self, all_data):
        for response in all_data:
            _id = response.get(AdsManagerReportsDimensionsField.ID.value)
            assert isinstance(_id, str)
            assert len(_id) >= 0

    def test_display_name_is_non_empty_string(self, all_data):
        for response in all_data:
            display_name = response.get(AdsManagerReportsDimensionsField.DISPLAY_NAME.value)
            assert isinstance(display_name, str)
            assert len(display_name) >= 0

    def test_type_id_is_positive_int(self, all_data):
        for response in all_data:
            type_id = response.get(AdsManagerReportsDimensionsField.TYPE_ID.value)
            assert isinstance(type_id, int)

    def test_actions_is_null(self, all_data):
        for response in all_data:
            actions = response.get(AdsManagerReportsDimensionsField.ACTIONS.value)
            assert actions is None

    def test_category_id_is_positive_int(self, all_data):
        for response in all_data:
            category_id = response.get(AdsManagerReportsDimensionsField.CATEGORY_ID.value)
            assert isinstance(category_id, int)
            assert category_id >= 0

    def test_width_is_positive_int(self, all_data):
        for response in all_data:
            width = response.get(AdsManagerReportsDimensionsField.WIDTH.value)
            assert isinstance(width, int)
            assert width >= 0

    def test_is_fixed_bool(self, all_data):
        for response in all_data:
            is_fixed = response.get(AdsManagerReportsDimensionsField.IS_FIXED.value)
            assert isinstance(is_fixed, bool)

    def test_group_display_name_is_null(self, all_data):
        for response in all_data:
            group_display_name = response.get(AdsManagerReportsDimensionsField.GROUP_DISPLAY_NAME.value)
            assert group_display_name is None

    def test_hidden_is_bool(self, all_data):
        for response in all_data:
            hidden = response.get(AdsManagerReportsDimensionsField.HIDDEN.value)
            assert isinstance(hidden, bool)

    def test_is_filterable_bool(self, all_data):
        for response in all_data:
            is_filterable = response.get(AdsManagerReportsDimensionsField.IS_FILTERABLE.value)
            assert isinstance(is_filterable, bool)

    def test_is_editable_bool(self, all_data):
        for response in all_data:
            is_editable = response.get(AdsManagerReportsDimensionsField.IS_EDITABLE.value)
            assert isinstance(is_editable, bool)

    def test_is_sortable_bool(self, all_data):
        for response in all_data:
            is_sortable = response.get(AdsManagerReportsDimensionsField.IS_SORTABLE.value)
            assert isinstance(is_sortable, bool)

    def test_no_of_decimals_is_positive_int(self, all_data):
        for response in all_data:
            no_of_decimals = response.get(AdsManagerReportsDimensionsField.NO_OF_DECIMALS.value)
            assert isinstance(no_of_decimals, int)
            assert no_of_decimals >= 0

    def test_description_is_null(self, all_data):
        for response in all_data:
            description = response.get(AdsManagerReportsDimensionsField.DESCRIPTION.value)
            assert description is None

    def test_is_toggle_bool(self, all_data):
        for response in all_data:
            is_toggle = response.get(AdsManagerReportsDimensionsField.IS_TOGGLE.value)
            assert isinstance(is_toggle, bool)

    def test_primary_value_is_dict_of_len_three(self, all_data):
        for response in all_data:
            primary_value = response.get(AdsManagerReportsDimensionsField.PRIMARY_VALUE.value)
            assert isinstance(primary_value, dict)
            assert len(primary_value) == 3

    def test_secondary_value_is_dict_of_len_three_if_present(self, all_data):
        for response in all_data:
            secondary_value = response.get(AdsManagerReportsDimensionsField.SECONDARY_VALUE.value)
            if secondary_value:
                assert isinstance(secondary_value, dict)
                assert len(secondary_value) == 3

    def test_pinned_is_dict_of_len_two_if_present(self, all_data):
        for response in all_data:
            pinned = response.get(AdsManagerReportsDimensionsField.PINNED.value)
            if pinned:
                assert isinstance(pinned, dict)
                assert len(pinned) == 2

    def test_primary_value_name_is_non_empty_string(self, all_data):
        for response in all_data:
            primary_value = response.get(AdsManagerReportsDimensionsField.PRIMARY_VALUE.value)
            name = primary_value.get(AdsManagerReportsDimensionsField.NAME.value)
            assert isinstance(name, str)

    def test_primary_value_type_id_is_positive_int(self, all_data):
        for response in all_data:
            primary_value = response.get(AdsManagerReportsDimensionsField.PRIMARY_VALUE.value)
            type_id = primary_value.get(AdsManagerReportsDimensionsField.TYPE_ID.value)
            assert isinstance(type_id, int)
            assert type_id >= 0

    def test_primary_value_aggregate_id_is_positive_int(self, all_data):
        for response in all_data:
            primary_value = response.get(AdsManagerReportsDimensionsField.PRIMARY_VALUE.value)
            aggregate_id = primary_value.get(AdsManagerReportsDimensionsField.AGGREGATE_ID.value)
            assert isinstance(aggregate_id, int)
            assert aggregate_id >= 0

    def test_secondary_value_name_is_non_empty_string(self, all_data):
        for response in all_data:
            secondary_value = response.get(AdsManagerReportsDimensionsField.SECONDARY_VALUE.value)
            if secondary_value:
                name = secondary_value.get(AdsManagerReportsDimensionsField.NAME.value)
                assert isinstance(name, str)

    def test_secondary_value_type_id_is_positive_int(self, all_data):
        for response in all_data:
            secondary_value = response.get(AdsManagerReportsDimensionsField.SECONDARY_VALUE.value)
            if secondary_value:
                type_id = secondary_value.get(AdsManagerReportsDimensionsField.TYPE_ID.value)
                assert isinstance(type_id, int)
                assert type_id >= 0

    def test_secondary_value_aggregate_id_is_positive_int(self, all_data):
        for response in all_data:
            secondary_value = response.get(AdsManagerReportsDimensionsField.SECONDARY_VALUE.value)
            if secondary_value:
                aggregate_id = secondary_value.get(AdsManagerReportsDimensionsField.AGGREGATE_ID.value)
                assert isinstance(aggregate_id, int)
                assert aggregate_id >= 0

    def test_pinned_name_is_non_empty_string(self, all_data):
        for response in all_data:
            pinned = response.get(AdsManagerReportsDimensionsField.PINNED.value)
            if pinned is not None:
                name = pinned.get(AdsManagerReportsDimensionsField.NAME.value)
                assert isinstance(name, str)

    def test_pinned_value_is_non_empty_string(self, all_data):
        for response in all_data:
            pinned = response.get(AdsManagerReportsDimensionsField.PINNED.value)
            if pinned is not None:
                value = pinned.get(AdsManagerReportsDimensionsField.VALUE.value)
                assert isinstance(value, str)
