import json
from enum import Enum

import pytest


class AdsManagerReportsDimensionsField(Enum):
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


class TestAdsManagerReportsDimensions:
    @pytest.fixture(scope="session")
    def response(self, client, config):
        url = f"/api/v1/get-metrics"
        return client.get(url, headers=config["headers"])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        return json.loads(data)

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_list(self, response_json):
        assert isinstance(response_json, list)

    def test_id_is_non_empty_string(self, response_json):
        for response in response_json:
            _id = response.get(AdsManagerReportsDimensionsField.ID.value)
            assert isinstance(_id, str)
            assert len(_id) >= 0

    def test_display_name_is_non_empty_string(self, response_json):
        for response in response_json:
            display_name = response.get(AdsManagerReportsDimensionsField.DISPLAY_NAME.value)
            assert isinstance(display_name, str)
            assert len(display_name) >= 0

    def test_type_id_is_positive_int(self, response_json):
        for response in response_json:
            type_id = response.get(AdsManagerReportsDimensionsField.TYPE_ID.value)
            assert isinstance(type_id, int)
            assert type_id >= 0

    def test_actions_is_null(self, response_json):
        for response in response_json:
            actions = response.get(AdsManagerReportsDimensionsField.ACTIONS.value)
            assert actions is None

    def test_category_id_is_positive_int(self, response_json):
        for response in response_json:
            category_id = response.get(AdsManagerReportsDimensionsField.CATEGORY_ID.value)
            assert isinstance(category_id, int)
            assert category_id >= 0

    def test_width_is_positive_int(self, response_json):
        for response in response_json:
            width = response.get(AdsManagerReportsDimensionsField.WIDTH.value)
            assert isinstance(width, int)
            assert width >= 0

    def test_is_fixed_bool(self, response_json):
        for response in response_json:
            is_fixed = response.get(AdsManagerReportsDimensionsField.IS_FIXED.value)
            assert isinstance(is_fixed, bool)

    def test_group_display_name_is_null(self, response_json):
        for response in response_json:
            group_display_name = response.get(AdsManagerReportsDimensionsField.GROUP_DISPLAY_NAME.value)
            assert group_display_name is None

    def test_hidden_is_bool(self, response_json):
        for response in response_json:
            hidden = response.get(AdsManagerReportsDimensionsField.HIDDEN.value)
            assert isinstance(hidden, bool)

    def test_is_filterable_bool(self, response_json):
        for response in response_json:
            is_filterable = response.get(AdsManagerReportsDimensionsField.IS_FILTERABLE.value)
            assert isinstance(is_filterable, bool)

    def test_is_editable_bool(self, response_json):
        for response in response_json:
            is_editable = response.get(AdsManagerReportsDimensionsField.IS_EDITABLE.value)
            assert isinstance(is_editable, bool)

    def test_is_sortable_bool(self, response_json):
        for response in response_json:
            is_sortable = response.get(AdsManagerReportsDimensionsField.IS_SORTABLE.value)
            assert isinstance(is_sortable, bool)

    def test_no_of_decimals_is_positive_int(self, response_json):
        for response in response_json:
            no_of_decimals = response.get(AdsManagerReportsDimensionsField.NO_OF_DECIMALS.value)
            assert isinstance(no_of_decimals, int)
            assert no_of_decimals >= 0

    def test_description_is_non_empty_string_if_present(self, response_json):
        for response in response_json:
            description = response.get(AdsManagerReportsDimensionsField.DESCRIPTION.value)
            if description:
                assert isinstance(description, str)
                assert len(description) >= 0

    def test_is_toggle_bool(self, response_json):
        for response in response_json:
            is_toggle = response.get(AdsManagerReportsDimensionsField.IS_TOGGLE.value)
            assert isinstance(is_toggle, bool)

    def test_primary_value_is_dict_of_len_three(self, response_json):
        for response in response_json:
            primary_value = response.get(AdsManagerReportsDimensionsField.PRIMARY_VALUE.value)
            assert isinstance(primary_value, dict)
            assert len(primary_value) == 3

    def test_secondary_value_is_null(self, response_json):
        for response in response_json:
            secondary_value = response.get(AdsManagerReportsDimensionsField.SECONDARY_VALUE.value)
            assert secondary_value is None

    def test_pinned_is_null(self, response_json):
        for response in response_json:
            pinned = response.get(AdsManagerReportsDimensionsField.PINNED.value)
            assert pinned is None

    def test_primary_value_name_is_non_empty_string(self, response_json):
        for response in response_json:
            primary_value = response.get(AdsManagerReportsDimensionsField.PRIMARY_VALUE.value)
            name = primary_value.get(AdsManagerReportsDimensionsField.NAME.value)
            assert isinstance(name, str)

    def test_primary_value_type_id_is_positive_int(self, response_json):
        for response in response_json:
            primary_value = response.get(AdsManagerReportsDimensionsField.PRIMARY_VALUE.value)
            type_id = primary_value.get(AdsManagerReportsDimensionsField.TYPE_ID.value)
            assert isinstance(type_id, int)
            assert type_id >= 0

    def test_primary_value_aggregate_id_is_positive_int(self, response_json):
        for response in response_json:
            primary_value = response.get(AdsManagerReportsDimensionsField.PRIMARY_VALUE.value)
            aggregate_id = primary_value.get(AdsManagerReportsDimensionsField.AGGREGATE_ID.value)
            assert isinstance(aggregate_id, int)
            assert aggregate_id >= 0
