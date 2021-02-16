from typing import Any, Dict, List, Optional

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.minimumbudget import MinimumBudget
from forex_python.converter import CurrencyCodes

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase


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
            "IMPRESSIONS": round(minimum_budgets[MinimumBudget.Field.min_daily_budget_imp] / 100, cls.PRECISION),
            "VIDEO_VIEWS": round(
                minimum_budgets[MinimumBudget.Field.min_daily_budget_video_views] / 100, cls.PRECISION
            ),
            "APP_INSTALLS": round(minimum_budgets[MinimumBudget.Field.min_daily_budget_low_freq] / 100, cls.PRECISION),
            "LINK_CLICK": min_daily_budget_high_freq,
            "PAGE_LIKES": min_daily_budget_high_freq,
            "DEFAULT": min_daily_budget_high_freq,
        }

        return mapped_minimum_budgets

    @classmethod
    def map_budget_validation_response(
        cls, facebook_response: Dict, max_bid: Dict, minimum_budgets: List[Dict]
    ) -> Dict:

        _currency_converter = CurrencyCodes()
        mapped_budget_validation_response = {
            "currency": facebook_response["currency"],
            "currencySymbol": _currency_converter.get_symbol(facebook_response["currency"]),
            "maximumAdAccountBid": round(max_bid["max_bid"] / 100, cls.PRECISION),
            "minimumAdAccountDailyBudget": round(facebook_response["min_daily_budget"] / 100, cls.PRECISION),
            "minimumAdAccountBudgets": cls.map_minimum_budgets_response(minimum_budgets, facebook_response["currency"]),
        }

        return mapped_budget_validation_response

    @classmethod
    def handle(cls, account_id: str, access_token: str, config: Any) -> Dict:

        _ = GraphAPISdkBase(config.facebook, access_token)

        required_fields = ["currency", "min_daily_budget"]
        account = AdAccount(account_id)
        facebook_response = account.api_get(fields=required_fields)
        max_bid = account.get_max_bid()[0]
        minimum_budgets = account.get_minimum_budgets()

        response = cls.map_budget_validation_response(
            facebook_response=facebook_response, max_bid=max_bid, minimum_budgets=minimum_budgets
        )

        return response
