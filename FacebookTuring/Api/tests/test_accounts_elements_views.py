import pytest
import json
from enum import Enum


class AccountsElementsViewsField(Enum):
    COLUMNS = "columns"
    ID = "id"
    IS_DEFAULT = "isDefault"
    IS_SELECTED = "isSelected"
    NAME = "name"
    FIELD = "field"
    HEADER_NAME = "headerName"
    DESCRIPTION = "description"
    COLUMN_TYPE = "columnType"
    NUMBER_OF_DECIMALS = "numberOfDecimals"


class TestAccountsElementsViews:

    @pytest.fixture(scope="session")
    def response(self, client, config):
        url = f"/api/v1/accounts/elements-cards-views"
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
            assert AccountsElementsViewsField.COLUMNS.value in response
            columns = response.get(AccountsElementsViewsField.COLUMNS.value)
            assert isinstance(columns, list)
            assert len(columns) > 0

    def test_id_is_positive_int(self, response_json):
        for response in response_json:
            assert AccountsElementsViewsField.ID.value in response
            _id = response.get(AccountsElementsViewsField.ID.value)
            assert isinstance(_id, int)
            assert _id > 0

    def test_is_default_is_bool(self, response_json):
        for response in response_json:
            assert AccountsElementsViewsField.IS_DEFAULT.value in response
            is_default = response.get(AccountsElementsViewsField.IS_DEFAULT.value)
            assert isinstance(is_default, bool)

    def test_is_selected_is_bool(self, response_json):
        for response in response_json:
            assert AccountsElementsViewsField.IS_SELECTED.value in response
            is_selected = response.get(AccountsElementsViewsField.IS_SELECTED.value)
            assert isinstance(is_selected, bool)

    def test_name_is_non_empty_string(self, response_json):
        for response in response_json:
            assert AccountsElementsViewsField.NAME.value in response
            name = response.get(AccountsElementsViewsField.NAME.value)
            assert isinstance(name, str)
            assert len(name) > 0

    @pytest.fixture(scope="session")
    def column_data(self, response_json):
        data = []
        for response in response_json:
            data += response.get(AccountsElementsViewsField.COLUMNS.value)
        return data

    def test_field_is_non_empty_string(self, column_data):
        for data in column_data:
            assert AccountsElementsViewsField.FIELD.value in data
            field = data.get(AccountsElementsViewsField.FIELD.value)
            assert isinstance(field, str)
            assert len(field) > 0

    def test_header_name_is_string(self, column_data):
        for data in column_data:
            assert AccountsElementsViewsField.HEADER_NAME.value in data
            header_name = data.get(AccountsElementsViewsField.HEADER_NAME.value)
            assert isinstance(header_name, str)

    def test_number_of_decimals_is_positive_int(self, column_data):
        for data in column_data:
            number_of_decimals = data.get(AccountsElementsViewsField.NUMBER_OF_DECIMALS.value)
            if number_of_decimals:
                assert isinstance(number_of_decimals, int)
                assert number_of_decimals > 0

    def test_column_type_is_non_empty_string(self, column_data):
        for data in column_data:
            assert AccountsElementsViewsField.COLUMN_TYPE.value in data
            column_type = data.get(AccountsElementsViewsField.COLUMN_TYPE.value)
            assert isinstance(column_type, str)
            assert len(column_type) > 0

    def test_description_is_non_empty_string(self, column_data):
        for data in column_data:
            assert AccountsElementsViewsField.DESCRIPTION.value in data
            description = data.get(AccountsElementsViewsField.DESCRIPTION.value)
            if description:
                assert isinstance(description, str)
                assert len(description) > 0
