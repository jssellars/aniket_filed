import pytest
import json

from Core.Web.FacebookGraphAPI.GraphAPIHandlers.GraphAPIBudgetValidationFields import (
    GraphAPIBudgetValidationField,
)


class TestBudgetValidation:

    @pytest.fixture(scope="session")
    def response(self, client, config):
        url = f"/api/v1/budget-validation/{config['account_id']}"
        return client.get(url, headers=config['headers'])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        return json.loads(data)

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_dict(self, response):
        data = response.data.decode("UTF-8")
        assert isinstance(json.loads(data), dict)

    def test_currency_param_is_string_with_length_three(self, response_json):
        assert GraphAPIBudgetValidationField.CURRENCY.value in response_json
        currency = response_json.get(GraphAPIBudgetValidationField.CURRENCY.value)
        assert isinstance(currency, str)
        assert len(currency) == 3

    def test_currency_symbol_param_is_string_with_length_gt_zero(self, response_json):
        assert GraphAPIBudgetValidationField.CURRENCY_SYMBOL.value in response_json
        currency_symbol = response_json.get(
            GraphAPIBudgetValidationField.CURRENCY_SYMBOL.value
        )
        assert isinstance(currency_symbol, str)
        assert len(currency_symbol) > 0

    def test_max_account_bid_param_is_positive_float(self, response_json):
        assert GraphAPIBudgetValidationField.MAX_AD_ACCOUNT_BID.value in response_json
        max_bid = response_json.get(
            GraphAPIBudgetValidationField.MAX_AD_ACCOUNT_BID.value
        )
        assert isinstance(max_bid, float)
        assert max_bid >= 0

    def test_min_account_daily_budget_param_is_positive_float(self, response_json):
        assert (
            GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_DAILY_BUDGET.value
            in response_json
        )
        min_daily_budget = response_json.get(
            GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_DAILY_BUDGET.value
        )
        assert isinstance(min_daily_budget, float)
        assert min_daily_budget >= 0

    def test_min_account_budget_param_is_dict(self, response_json):
        assert (
            GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_BUDGETS.value in response_json
        )
        min_account_budget = response_json.get(
            GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_BUDGETS.value
        )
        assert isinstance(min_account_budget, dict)

    def test_impressions_param_is_positive_float(self, response_json):
        assert (
            GraphAPIBudgetValidationField.IMPRESSIONS.value
            in response_json[GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_BUDGETS.value]
        )
        impression = response_json.get(
            GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_BUDGETS.value
        ).get(GraphAPIBudgetValidationField.IMPRESSIONS.value)
        assert isinstance(impression, float)
        assert impression >= 0

    def test_video_views_param_is_positive_float(self, response_json):
        assert (
            GraphAPIBudgetValidationField.VIDEO_VIEWS.value
            in response_json[GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_BUDGETS.value]
        )
        video_views = response_json.get(
            GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_BUDGETS.value
        ).get(GraphAPIBudgetValidationField.VIDEO_VIEWS.value)
        assert isinstance(video_views, float)
        assert video_views >= 0

    def test_app_installs_param_is_positive_float(self, response_json):
        assert (
            GraphAPIBudgetValidationField.APP_INSTALLS.value
            in response_json[GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_BUDGETS.value]
        )
        app_installs = response_json.get(
            GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_BUDGETS.value
        ).get(GraphAPIBudgetValidationField.APP_INSTALLS.value)
        assert isinstance(app_installs, float)
        assert app_installs >= 0

    def test_link_clicks_param_is_positive_float(self, response_json):
        assert (
            GraphAPIBudgetValidationField.LINK_CLICKS.value
            in response_json[GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_BUDGETS.value]
        )
        link_clicks = response_json.get(
            GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_BUDGETS.value
        ).get(GraphAPIBudgetValidationField.LINK_CLICKS.value)
        assert isinstance(link_clicks, float)
        assert link_clicks >= 0

    def test_page_likes_param_is_positive_float(self, response_json):
        assert (
            GraphAPIBudgetValidationField.PAGE_LIKES.value
            in response_json[GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_BUDGETS.value]
        )
        page_likes = response_json.get(
            GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_BUDGETS.value
        ).get(GraphAPIBudgetValidationField.PAGE_LIKES.value)
        assert isinstance(page_likes, float)
        assert page_likes >= 0

    def test_default_param_is_positive_float(self, response_json):
        assert (
            GraphAPIBudgetValidationField.DEFAULT.value
            in response_json[GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_BUDGETS.value]
        )
        default = response_json.get(
            GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_BUDGETS.value
        ).get(GraphAPIBudgetValidationField.DEFAULT.value)
        assert isinstance(default, float)
        assert default >= 0
