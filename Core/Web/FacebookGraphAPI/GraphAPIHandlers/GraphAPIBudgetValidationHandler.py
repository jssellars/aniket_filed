from typing import Dict, List, Optional

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.minimumbudget import MinimumBudget
from forex_python.converter import CurrencyCodes

from Core.Web.FacebookGraphAPI.GraphAPIHandlers.GraphAPIBudgetValidationFields import GraphAPIBudgetValidationField


class GraphAPIBudgetValidationHandler:

    PRECISION = 2

    @classmethod
    def map_minimum_budgets_response(cls, minimum_budgets_facebook: List[Dict], currency: str = None) -> Optional[Dict]:

        minimum_budgets = list(filter(lambda x: x if x["currency"] == currency else None, minimum_budgets_facebook))[0]

        if not minimum_budgets:
            return None

        min_daily_budget_high_freq = round(
            minimum_budgets[MinimumBudget.Field.min_daily_budget_high_freq] / 100, cls.PRECISION
        )

        mapped_minimum_budgets = {
            GraphAPIBudgetValidationField.IMPRESSIONS.value: round(
                minimum_budgets[MinimumBudget.Field.min_daily_budget_imp] / 100, cls.PRECISION
            ),
            GraphAPIBudgetValidationField.VIDEO_VIEWS.value: round(
                minimum_budgets[MinimumBudget.Field.min_daily_budget_video_views] / 100, cls.PRECISION
            ),
            GraphAPIBudgetValidationField.APP_INSTALLS.value: round(
                minimum_budgets[MinimumBudget.Field.min_daily_budget_low_freq] / 100, cls.PRECISION
            ),
            GraphAPIBudgetValidationField.LINK_CLICKS.value: min_daily_budget_high_freq,
            GraphAPIBudgetValidationField.PAGE_LIKES.value: min_daily_budget_high_freq,
            GraphAPIBudgetValidationField.DEFAULT.value: min_daily_budget_high_freq,
        }

        return mapped_minimum_budgets

    @classmethod
    def map_budget_validation_response(
        cls, facebook_response: Dict, max_bid: Dict, minimum_budgets: List[Dict]
    ) -> Dict:

        _currency_converter = CurrencyCodes()
        mapped_budget_validation_response = {
            GraphAPIBudgetValidationField.CURRENCY.value: facebook_response["currency"],
            GraphAPIBudgetValidationField.CURRENCY_SYMBOL.value: _currency_converter.get_symbol(
                facebook_response["currency"]
            ),
            GraphAPIBudgetValidationField.MAX_AD_ACCOUNT_BID.value: round(max_bid["max_bid"] / 100, cls.PRECISION),
            GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_DAILY_BUDGET.value: round(
                facebook_response["min_daily_budget"] / 100, cls.PRECISION
            ),
            GraphAPIBudgetValidationField.MIN_AD_ACCOUNT_BUDGETS.value: cls.map_minimum_budgets_response(
                minimum_budgets, facebook_response["currency"]
            ),
        }

        return mapped_budget_validation_response

    @classmethod
    def handle(cls, account_id: str) -> Dict:

        required_fields = ["currency", "min_daily_budget"]
        account = AdAccount(account_id)
        facebook_response = account.api_get(fields=required_fields)
        max_bid = account.get_max_bid()[0]
        minimum_budgets = account.get_minimum_budgets()

        response = cls.map_budget_validation_response(
            facebook_response=facebook_response, max_bid=max_bid, minimum_budgets=minimum_budgets
        )

        return response
