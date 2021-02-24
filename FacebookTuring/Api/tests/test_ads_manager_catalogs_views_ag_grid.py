import pytest
import json
from enum import Enum


class AdsManagerCatalogsViewsAgGridField(Enum):
    COLUMNS = "columns"
    ID = "id"
    IS_DEFAULT = "isDefault"
    IS_SELECTED = "isSelected"
    NAME = "name"
    COL_ID = "colId"
    FIELD = "field"
    COLUMN_TYPE = "columnType"
    HEADER_NAME = "headerName"
    SORTABLE = "sortable"
    FILTER = "filter"
    PINNED = "pinned"
    EDITABLE = "editable"
    IS_NAME_CLICKABLE = "isNameClickable"
    SUPPRESS_COLUMNS_TOOL_PANEL = "suppressColumnsToolPanel"
    NUMBER_OF_DECIMALS = "numberOfDecimals"


class TestAdsManagerCatalogsViewsAgGrid:

    @pytest.fixture(scope="session", params=["campaign", "adset", "ad"])
    def response(self, client, config, request):
        url = f"/api/v1/ag-grid-views/{request.param}"
        return client.get(url, headers=config["headers"])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        return json.loads(data)

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_list(self, response_json):
        assert isinstance(response_json, list)

    def test_data_in_list_is_dict_with_len_5(self, response_json):
        for response in response_json:
            assert isinstance(response, dict)
            assert len(response) == 5

    def test_columns_is_non_empty_list(self, response_json):
        for response in response_json:
            assert AdsManagerCatalogsViewsAgGridField.COLUMNS.value in response
            columns = response.get(AdsManagerCatalogsViewsAgGridField.COLUMNS.value)
            assert isinstance(columns, list)
            assert len(columns) > 0

    def test_id_is_positive_int(self, response_json):
        for response in response_json:
            assert AdsManagerCatalogsViewsAgGridField.ID.value in response
            _id = response.get(AdsManagerCatalogsViewsAgGridField.ID.value)
            assert isinstance(_id, int)
            assert _id > 0

    def test_is_default_is_bool(self, response_json):
        for response in response_json:
            assert AdsManagerCatalogsViewsAgGridField.IS_DEFAULT.value in response
            is_default = response.get(AdsManagerCatalogsViewsAgGridField.IS_DEFAULT.value)
            assert isinstance(is_default, bool)

    def test_is_selected_is_bool(self, response_json):
        for response in response_json:
            assert AdsManagerCatalogsViewsAgGridField.IS_SELECTED.value in response
            is_selected = response.get(AdsManagerCatalogsViewsAgGridField.IS_SELECTED.value)
            assert isinstance(is_selected, bool)

    def test_name_is_non_empty_string(self, response_json):
        for response in response_json:
            assert AdsManagerCatalogsViewsAgGridField.NAME.value in response
            name = response.get(AdsManagerCatalogsViewsAgGridField.NAME.value)
            assert isinstance(name, str)
            assert len(name) > 0

    @pytest.fixture(scope="session")
    def column_data(self, response_json):
        data = []
        for response in response_json:
            data += response.get(AdsManagerCatalogsViewsAgGridField.COLUMNS.value)

        return data

    def test_col_id_is_non_empty_string(self, column_data):
        for data in column_data:
            assert AdsManagerCatalogsViewsAgGridField.COL_ID.value in data
            col_id = data.get(AdsManagerCatalogsViewsAgGridField.COL_ID.value)
            assert isinstance(col_id, str)
            assert len(col_id) > 0

    def test_field_is_non_empty_string(self, column_data):
        for data in column_data:
            assert AdsManagerCatalogsViewsAgGridField.FIELD.value in data
            field = data.get(AdsManagerCatalogsViewsAgGridField.FIELD.value)
            assert isinstance(field, str)
            assert len(field) > 0

    def test_column_type_is_non_empty_string(self, column_data):
        for data in column_data:
            assert AdsManagerCatalogsViewsAgGridField.COLUMN_TYPE.value in data
            column_type = data.get(AdsManagerCatalogsViewsAgGridField.COLUMN_TYPE.value)
            assert isinstance(column_type, str)
            assert len(column_type) > 0

    def test_header_name_is_string(self, column_data):
        for data in column_data:
            assert AdsManagerCatalogsViewsAgGridField.HEADER_NAME.value in data
            header_name = data.get(AdsManagerCatalogsViewsAgGridField.HEADER_NAME.value)
            assert isinstance(header_name, str)

    def test_sortable_is_bool(self, column_data):
        for data in column_data:
            sortable = data.get(AdsManagerCatalogsViewsAgGridField.SORTABLE.value)
            if sortable:
                assert isinstance(sortable, bool)

    def test_filter_is_non_empty_string(self, column_data):
        for data in column_data:
            _filter = data.get(AdsManagerCatalogsViewsAgGridField.FILTER.value)
            if _filter:
                assert isinstance(_filter, str)
                assert len(_filter) > 0

    def test_pinned_is_non_empty_string(self, column_data):
        for data in column_data:
            pinned = data.get(AdsManagerCatalogsViewsAgGridField.PINNED.value)
            if pinned:
                assert isinstance(pinned, str)
                assert len(pinned) > 0

    def test_editable_is_bool(self, column_data):
        for data in column_data:
            editable = data.get(AdsManagerCatalogsViewsAgGridField.EDITABLE.value)
            if editable is not None:
                assert isinstance(editable, bool)

    def test_is_name_clickable(self, column_data):
        for data in column_data:
            is_name_clickable = data.get(AdsManagerCatalogsViewsAgGridField.IS_NAME_CLICKABLE.value)
            if is_name_clickable is not None:
                assert isinstance(is_name_clickable, bool)

    def test_number_of_decimals_is_positive_int(self, column_data):
        for data in column_data:
            number_of_decimals = data.get(AdsManagerCatalogsViewsAgGridField.NUMBER_OF_DECIMALS.value)
            if number_of_decimals:
                assert isinstance(number_of_decimals, int)
                assert number_of_decimals > 0

    def test_suppress_columns_tools_panel(self, column_data):
        for data in column_data:
            suppress_columns_tools_panel = data.get(AdsManagerCatalogsViewsAgGridField.SUPPRESS_COLUMNS_TOOL_PANEL.value)
            if suppress_columns_tools_panel is not None:
                assert isinstance(suppress_columns_tools_panel, bool)
