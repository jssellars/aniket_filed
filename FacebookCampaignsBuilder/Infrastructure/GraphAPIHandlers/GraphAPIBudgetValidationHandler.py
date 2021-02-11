import typing
from facebook_business.adobjects.adaccount import AdAccount
from forex_python.converter import CurrencyCodes
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from FacebookCampaignsBuilder.Api.startup import config


class GraphAPIBudgetValidationHandler:

    @classmethod
    def map_minimum_budgets_response(
            cls,
            minimum_budgets_facebook: typing.List[typing.Dict],
            currency: typing.AnyStr = None
    ) -> typing.Union[typing.Dict, typing.NoReturn]:

        minimum_budgets = list(filter(lambda x: x if x['currency'] == currency else None, minimum_budgets_facebook))[0]

        if not minimum_budgets:
            return None

        mappend_minimum_budgets = {
            'IMPRESSIONS': round(minimum_budgets['min_daily_budget_imp'] / 100),
            'VIDEO_VIEWS': round(minimum_budgets['min_daily_budget_video_views'] / 100),
            'APP_INSTALLS': round(minimum_budgets['min_daily_budget_low_freq'] / 100),
            'LINK_CLICK': round(minimum_budgets['min_daily_budget_high_freq'] / 100),
            'PAGE_LIKES': round(minimum_budgets['min_daily_budget_high_freq'] / 100),
            'DEFAULT': round(minimum_budgets['min_daily_budget_high_freq'] / 100),
        }

        return mappend_minimum_budgets

    @classmethod
    def map_budget_validation_response(
            cls,
            facebook_response: typing.Dict,
            max_bid: typing.Dict,
            minimum_budgets: typing.List[typing.Dict]
    ) -> typing.Dict:

        _currency_converter = CurrencyCodes()
        mapped_budget_validation_response = {
            'currency': facebook_response['currency'],
            'currencySymbol': _currency_converter.get_symbol(facebook_response['currency']),
            'maximumAdAccountBid': round(max_bid['max_bid'] / 100),
            'minimumAdAccountDailyBudget': round(facebook_response['min_daily_budget'] / 100),
            'minimumAdAccountBudgets': cls.map_minimum_budgets_response(minimum_budgets, facebook_response['currency'])
        }

        return mapped_budget_validation_response

    @classmethod
    def handle(cls, account_id: typing.AnyStr = None, access_token: typing.AnyStr = None) -> typing.Dict:

        _ = GraphAPISdkBase(config.facebook, access_token)

        required_fields = ["currency", "min_daily_budget"]
        account = AdAccount(account_id)
        facebook_response = account.api_get(fields=required_fields)
        max_bid = account.get_max_bid()[0]
        minimum_budgets = account.get_minimum_budgets()

        response = cls.map_budget_validation_response(
            facebook_response=facebook_response,
            max_bid=max_bid,
            minimum_budgets=minimum_budgets
        )

        return response
