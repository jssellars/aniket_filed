import pytest
import json
from enum import Enum

from Core.test_config import ACCOUNT_ID


class ReportsInsightsField(Enum):
    CPM = "cpm"
    DATE_START = "date_start"
    AMOUNT_SPENT = "amount_spent"
    UNIQUE_CTR_ALL = "unique_ctr_all"
    CPC_ALL = "cpc_all"
    DAY = "day"
    ACHIEVEMENT_UNLOCKED_COST = "achievements_unlocked_cost"


class TestReportsReportsInsights:

    post_data = {
        "TableName": "vCampaignInsights",
        "Columns": [
            {"Name": "achievements_unlocked_cost", "Aggregator": 1},
            {"Name": "cpm"},
            {"Name": "unique_ctr_all"},
            {"Name": "cpc_all"},
            {"Name": "amount_spent"},
        ],
        "Dimensions": [{"GroupColumnName": "date_start"}, {"GroupColumnName": "day"}],
        "Where": {
            "LogicalOperator": 1,
            "Conditions": None,
            "ChildConditions": [
                {
                    "LogicalOperator": 0,
                    "Conditions": [
                        {
                            "ColumnName": "date_start",
                            "Operator": 2,
                            "Value": "2021-01-02",
                        },
                        {
                            "ColumnName": "date_stop",
                            "Operator": 4,
                            "Value": "2021-02-19",
                        },
                        {
                            "ColumnName": "account_id",
                            "Operator": 0,
                            "Value": ACCOUNT_ID,
                        },
                        {"ColumnName": "time_increment", "Operator": 6, "Value": 1},
                    ],
                }
            ],
        },
    }

    @pytest.fixture(scope="session")
    def response(self, client, config):
        url = f"/api/v1/reports/reports"
        return client.post(url, json=self.post_data, headers=config["headers"])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        print(data)
        return json.loads(data)

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_list(self, response_json):
        assert isinstance(response_json, list)

    def test_data_in_list_is_dict_with_len_7(self, response_json):
        for data in response_json:
            assert isinstance(data, dict)
            assert len(data) == 7

    def test_cpm_is_positive_float(self, response_json):
        for data in response_json:
            assert ReportsInsightsField.CPM.value in data
            cpm = data.get(ReportsInsightsField.CPM.value)
            if cpm is not 0 and cpm is not None:
                assert isinstance(cpm, float)
                assert cpm >= 0

    def test_date_start_is_string_with_len_10(self, response_json):
        for data in response_json:
            assert ReportsInsightsField.DATE_START.value in data
            start_date = data.get(ReportsInsightsField.DATE_START.value)
            if start_date is not None:
                assert isinstance(start_date, str)
                assert len(start_date) == 10

    def test_amount_spent_is_positive_float(self, response_json):
        for data in response_json:
            assert ReportsInsightsField.AMOUNT_SPENT.value in data
            amount_spent = data.get(ReportsInsightsField.AMOUNT_SPENT.value)
            if amount_spent is not 0 and amount_spent is not None:
                assert isinstance(amount_spent, float)
                assert amount_spent >= 0

    def test_unique_ctr_all_is_positive_float(self, response_json):
        for data in response_json:
            assert ReportsInsightsField.UNIQUE_CTR_ALL.value in data
            unique_ctr_all = data.get(ReportsInsightsField.UNIQUE_CTR_ALL.value)
            if unique_ctr_all is not 0 and unique_ctr_all is not None:
                assert isinstance(unique_ctr_all, float)
                assert unique_ctr_all >= 0

    def test_cpc_all_is_positive_float(self, response_json):
        for data in response_json:
            assert ReportsInsightsField.CPC_ALL.value in data
            cpc_all = data.get(ReportsInsightsField.CPC_ALL.value)
            if cpc_all is not 0 and cpc_all is not None:
                assert isinstance(cpc_all, float)
                assert cpc_all >= 0

    def test_day_is_non_empty_string(self, response_json):
        for data in response_json:
            assert ReportsInsightsField.DAY.value in data
            day = data.get(ReportsInsightsField.DAY.value)
            if day is not None:
                assert isinstance(day, str)
                assert len(day) > 0

    def test_achievements_unlocked_cost_is_positive_float(self, response_json):
        for data in response_json:
            assert ReportsInsightsField.ACHIEVEMENT_UNLOCKED_COST.value in data
            achievements_unlocked_cost = data.get(
                ReportsInsightsField.ACHIEVEMENT_UNLOCKED_COST.value
            )
            if (
                achievements_unlocked_cost is not 0
                and achievements_unlocked_cost is not None
            ):
                assert isinstance(achievements_unlocked_cost, float)
                assert achievements_unlocked_cost >= 0
