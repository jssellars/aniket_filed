from datetime import datetime

import pytest
import json
from enum import Enum

from Core.test_config import ACCOUNT_ID
from Core.constants import DEFAULT_DATETIME_UTC


class AgGridInsightField(Enum):
    ADSET_ID = "adset_id"
    ADSET_NAME = "adset_name"
    AMOUNT_SPENT = "amount_spent"
    BUDGET = "budget"
    CONVERSION_RATE_RANKING = "conversion_rate_ranking"
    COST_PER_RESULT = "cost_per_result"
    COST_PER_UNIQUE_CLICK_ALL = "cost_per_unique_click_all"
    CPM = "cpm"
    EFFECTIVE_STATUS = "effective_status"
    FREQUENCY = "frequency"
    IMPRESSIONS = "impressions"
    LANDING_PAGE_VIEWS_TOTAL = "landing_page_views_total"
    LANDING_PAGE_VIEWS_UNIQUE = "landing_page_views_unique"
    PURCHASE_ROAS = "purchase_roas"
    PURCHASES_VALUE = "purchases_value"
    RESULTS = "results"
    STATUS = "status"
    STOP_TIME = "stop_time"
    UNIQUE_CLICKS_ALL = "unique_clicks_all"
    UNIQUE_CTR_ALL = "unique_ctr_all"
    ACCOUNT_ID = "account_id"
    ACCOUNT_NAME = "account_name"
    CAMPAIGN_ID = "campaign_id"
    CAMPAIGN_NAME = "campaign_name"
    DAILY_BUDGET = "daily_budget"
    ID = "id"
    LIFETIME_BUDGET = "lifetime_budget"
    NAME = "name"
    RESULT_TYPE = "result_type"


class TestAgGridInsights:

    level = None

    post_data = {
        "startRow": 0,
        "endRow": 20,
        "rowGroupCols": [],
        "valueCols": [],
        "pivotCols": [],
        "pivotMode": False,
        "groupKeys": [],
        "filterModel": {},
        "sortModel": [],
        "timeRange": {"since": "2021-01-02", "until": "2021-02-20"},
        "facebookAccountId": ACCOUNT_ID,
        "pageSize": 20,
        "nextPageCursor": None,
    }

    ag_columns = ["selected",
                  "status",
                  "adset_id",
                  "adset_name",
                  "effective_status",
                  "budget",
                  "amount_spent",
                  "impressions",
                  "cpm",
                  "frequency",
                  "unique_clicks_all",
                  "cost_per_unique_click_all",
                  "unique_ctr_all",
                  "results",
                  "cost_per_result",
                  "conversion_rate_ranking",
                  "landing_page_views_total",
                  "landing_page_views_unique",
                  "purchases_value",
                  "purchase_roas",
                  "stop_time"]

    @pytest.fixture(scope="session", params=[True, False])
    def has_delivery(self, request):
        return request.param

    @pytest.fixture(scope="session", params=["campaign", "adset", "ad"])
    def response(self, client, config, request, has_delivery):
        self.post_data["hasDelivery"] = has_delivery
        if request.param == "ad":
            self.post_data["agColumns"] = ",".join(self.ag_columns[:-1])
        else:
            self.post_data["agColumns"] = ",".join(self.ag_columns)
        TestAgGridInsights.level = request.param
        url = f"/api/v1/ag-grid-insights/{request.param}"
        return client.post(url, json=self.post_data, headers=config["headers"])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        return json.loads(data)


class TestAgGridInsightsBaseParam(TestAgGridInsights):

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_dict(self, response):
        data = response.data.decode("UTF-8")
        assert isinstance(json.loads(data), dict)

    def test_has_next_page_cursor_param(self, response_json):
        assert "nextPageCursor" in response_json

    def test_data_param_is_list(self, response_json):
        assert "data" in response_json
        data = response_json.get("data")
        assert isinstance(data, list)
        if len(data) > 0:
            TestAgGridInsights.data_present = True

    def test_summary_param_is_non_empty_list(self, response_json):
        assert "summary" in response_json
        summary = response_json.get("summary")
        assert isinstance(summary, list)
        assert len(summary) == 1

    def test_data_in_summary_is_non_empty_dict(self, response_json):
        summary = response_json.get("summary")[0]
        assert isinstance(summary, dict)
        if TestAgGridInsights.level == "ad":
            assert len(summary) == 16
        else:
            assert len(summary) == 17


class TestAgGridInsightsSummaryParam(TestAgGridInsights):

    @pytest.fixture(scope="class")
    def data(self, response_json):
        return response_json.get("summary")

    def test_cost_per_unique_click_all_is_positive_float(self, data):
        for summary in data:
            assert AgGridInsightField.COST_PER_UNIQUE_CLICK_ALL.value in summary
            cost_per_unique_click_all = summary.get(
                AgGridInsightField.COST_PER_UNIQUE_CLICK_ALL.value
            )
            if (
                    cost_per_unique_click_all is not None
                    and cost_per_unique_click_all is not 0
            ):
                assert isinstance(cost_per_unique_click_all, float)
                assert cost_per_unique_click_all >= 0

    def test_purchases_value_is_positive_float(self, data):
        print()
        for summary in data:
            assert AgGridInsightField.PURCHASES_VALUE.value in summary
            purchases_value = summary.get(AgGridInsightField.PURCHASES_VALUE.value)
            if purchases_value is not None and purchases_value is not 0:
                assert isinstance(purchases_value, float)
                assert purchases_value >= 0

    def test_amount_spent_is_positive_float(self, data):
        for summary in data:
            assert AgGridInsightField.AMOUNT_SPENT.value in summary
            amount_spent = summary.get(AgGridInsightField.AMOUNT_SPENT.value)
            if amount_spent is not None and amount_spent is not 0:
                assert isinstance(amount_spent, float)
                assert amount_spent >= 0

    def test_purchase_roas_is_positive_float(self, data):
        for summary in data:
            assert AgGridInsightField.PURCHASE_ROAS.value in summary
            purchase_roas = summary.get(AgGridInsightField.PURCHASE_ROAS.value)
            if purchase_roas is not None and purchase_roas is not 0:
                assert isinstance(purchase_roas, float)
                assert purchase_roas >= 0

    def test_impressions_is_positive_int(self, data):
        for summary in data:
            assert AgGridInsightField.IMPRESSIONS.value in summary
            impressions = summary.get(AgGridInsightField.IMPRESSIONS.value)
            if impressions is not None:
                assert isinstance(impressions, int)
                assert impressions >= 0

    def test_frequency_is_positive_float(self, data):
        for summary in data:
            assert AgGridInsightField.FREQUENCY.value in summary
            frequency = summary.get(AgGridInsightField.FREQUENCY.value)
            if frequency is not None and frequency is not 0:
                assert isinstance(frequency, float)
                assert frequency >= 0

    def test_stop_time_is_non_empty_datetime(self, data):
        if TestAgGridInsights.level == "ad":
            pytest.skip(msg=f"Field not relevant to level {TestAgGridInsights.level}")
        for summary in data:
            assert AgGridInsightField.STOP_TIME.value in summary
            stop_time = summary.get(AgGridInsightField.STOP_TIME.value)
            if stop_time is not None:
                assert isinstance(stop_time, str)
                assert len(stop_time) == 24
                stop_time = datetime.strptime(stop_time, DEFAULT_DATETIME_UTC)
                assert isinstance(stop_time, datetime)

    def test_landing_page_views_unique_is_positive_int(self, data):
        for summary in data:
            assert AgGridInsightField.LANDING_PAGE_VIEWS_UNIQUE.value in summary
            landing_page_views_unique = summary.get(
                AgGridInsightField.LANDING_PAGE_VIEWS_UNIQUE.value
            )
            if landing_page_views_unique is not None:
                assert isinstance(landing_page_views_unique, int)
                assert landing_page_views_unique >= 0

    def test_landing_page_views_total_is_positive_int(self, data):
        for summary in data:
            assert AgGridInsightField.LANDING_PAGE_VIEWS_TOTAL.value in summary
            landing_page_views_total = summary.get(
                AgGridInsightField.LANDING_PAGE_VIEWS_TOTAL.value
            )
            if landing_page_views_total is not None:
                assert isinstance(landing_page_views_total, int)
                assert landing_page_views_total >= 0

    def test_status_is_non_empty_string(self, data):
        for summary in data:
            assert AgGridInsightField.STATUS.value in summary
            status = summary.get(AgGridInsightField.STATUS.value)
            if status is not None:
                assert isinstance(status, str)
                assert len(status) > 0

    def test_unique_ctr_all_is_positive_float(self, data):
        for summary in data:
            assert AgGridInsightField.UNIQUE_CTR_ALL.value in summary
            unique_ctr_all = summary.get(AgGridInsightField.UNIQUE_CTR_ALL.value)
            if unique_ctr_all is not None and unique_ctr_all is not 0:
                assert isinstance(unique_ctr_all, float)
                assert unique_ctr_all >= 0

    def test_cpm_is_positive_float(self, data):
        for summary in data:
            assert AgGridInsightField.CPM.value in summary
            cpm = summary.get(AgGridInsightField.CPM.value)
            if cpm is not None and cpm is not 0:
                assert isinstance(cpm, float)
                assert cpm >= 0

    def test_unique_clicks_all_is_positive_int(self, data):
        for summary in data:
            assert AgGridInsightField.UNIQUE_CLICKS_ALL.value in summary
            unique_clicks_all = summary.get(AgGridInsightField.UNIQUE_CLICKS_ALL.value)
            if unique_clicks_all is not None:
                assert isinstance(unique_clicks_all, int)
                assert unique_clicks_all >= 0

    def test_effective_status_is_non_empty_string(self, data):
        for summary in data:
            assert AgGridInsightField.EFFECTIVE_STATUS.value in summary
            effective_status = summary.get(AgGridInsightField.EFFECTIVE_STATUS.value)
            if effective_status is not None:
                assert isinstance(effective_status, str)
                assert len(effective_status) > 0

    def test_adset_name_is_non_empty_string(self, data):
        for summary in data:
            assert AgGridInsightField.ADSET_NAME.value in summary
            adset_name = summary.get(AgGridInsightField.ADSET_NAME.value)
            if adset_name is not None:
                assert isinstance(adset_name, str)
                assert len(adset_name) > 0

    def test_conversion_rate_ranking_is_non_empty_string(self, data):
        for summary in data:
            assert AgGridInsightField.CONVERSION_RATE_RANKING.value in summary
            conversion_rate_ranking = summary.get(
                AgGridInsightField.CONVERSION_RATE_RANKING.value
            )
            if conversion_rate_ranking is not None:
                assert isinstance(conversion_rate_ranking, str)
                assert len(conversion_rate_ranking) > 0

    def test_adset_id_is_non_empty_numeric_string(self, data):
        for summary in data:
            assert AgGridInsightField.ADSET_ID.value in summary
            adset_id = summary.get(AgGridInsightField.ADSET_ID.value)
            if adset_id is not None:
                assert isinstance(adset_id, str)
                assert len(adset_id) > 0
                assert adset_id.isnumeric()


class TestAgGridInsightsDataParams(TestAgGridInsightsSummaryParam):

    @pytest.fixture(scope="class")
    def data(self, response_json):
        return response_json.get("data")

    def test_budget_is_non_empty_string(self, data):
        for response in data:
            budget = response.get(AgGridInsightField.BUDGET.value)
            if budget is not None:
                assert isinstance(budget, str)
                assert len(budget) > 0

    def test_cost_per_result_is_positive_float(self, data):
        for response in data:
            cost_per_result = response.get(AgGridInsightField.COST_PER_RESULT.value)
            if cost_per_result is not None and cost_per_result is not 0:
                assert isinstance(cost_per_result, float)
                assert cost_per_result >= 0

    def test_results_is_positive_float(self, data):
        for response in data:
            results = response.get(AgGridInsightField.RESULTS.value)
            if results is not None and results is not 0:
                assert isinstance(results, float)
                assert results >= 0

    def test_account_id_is_non_empty_numeric_string(self, data):
        for response in data:
            account_id = response.get(AgGridInsightField.ADSET_ID.value)
            if account_id is not None:
                assert isinstance(account_id, str)
                assert len(account_id) > 0
                assert account_id.isnumeric()

    def test_account_name_is_non_empty_string(self, data):
        for response in data:
            account_name = response.get(AgGridInsightField.ACCOUNT_NAME.value)
            if account_name is not None:
                assert isinstance(account_name, str)
                assert len(account_name) > 0

    def test_campaign_id_is_non_empty_numeric_string(self, data):
        for response in data:
            campaign_id = response.get(AgGridInsightField.CAMPAIGN_ID.value)
            if campaign_id is not None:
                assert isinstance(campaign_id, str)
                assert len(campaign_id) > 0
                assert campaign_id.isnumeric()

    def test_campaign_name_is_non_empty_string(self, data):
        for response in data:
            campaign_name = response.get(AgGridInsightField.CAMPAIGN_NAME.value)
            if campaign_name is not None:
                assert isinstance(campaign_name, str)
                assert len(campaign_name) > 0

    def test_daily_budget_is_positive_float(self, data):
        for response in data:
            daily_budget = response.get(AgGridInsightField.DAILY_BUDGET.value)
            if daily_budget is not None and daily_budget is not 0:
                assert isinstance(daily_budget, float)
                assert daily_budget >= 0

    def test_lifetime_budget_is_numeric_string(self, data):
        for response in data:
            lifetime_budget = response.get(AgGridInsightField.LIFETIME_BUDGET.value)
            if lifetime_budget is not None and lifetime_budget is not 0:
                assert isinstance(lifetime_budget, str)
                assert len(lifetime_budget) > 0
                assert lifetime_budget.isnumeric()

    def test_result_type_is_non_empty_string(self, data):
        for response in data:
            result_type = response.get(AgGridInsightField.RESULT_TYPE.value)
            if result_type is not None:
                assert isinstance(result_type, str)
                assert len(result_type) > 0
