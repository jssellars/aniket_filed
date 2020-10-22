import typing
from string import Template

import requests
from forex_python.converter import CurrencyCodes


class GraphAPIBudgetValidationHandler:
    __facebook_budget_validation_url = Template('https://graph.facebook.com/v7.0/$account_id?'
                                                'fields=currency,max_bid,min_daily_budget,minimum_budgets&'
                                                'access_token=$access_token')

    __objective_optimization_catalogs = {
        'min_daily_budget_imp': 'IMPRESSIONS',
        'min_daily_budget_video_views': 'VIDEO_VIEWS',
        'min_daily_budget_low_freq': 'APP_INSTALLS',
        'min_daily_budget_high_freq': ['LINK_CLICK', 'PAGE_LIKES']
    }

    @classmethod
    def map_minimum_budgets_response(cls,
                                     minimum_budgets_facebook: typing.List[typing.Dict],
                                     currency: typing.AnyStr = None) -> typing.Union[typing.Dict, typing.NoReturn]:
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
    def map_budget_validation_response(cls, facebook_response: typing.Dict) -> typing.Dict:
        _currency_converter = CurrencyCodes()
        mapped_budget_validation_response = {
            'currency': facebook_response['currency'],
            'currencySymbol': _currency_converter.get_symbol(facebook_response['currency']),
            'maximumAdAccountBid': round(facebook_response['max_bid']['data'][0]['max_bid'] / 100),
            'minimumAdAccountDailyBudget': round(facebook_response['min_daily_budget'] / 100),
            'minimumAdAccountBudgets': cls.map_minimum_budgets_response(facebook_response['minimum_budgets']['data'],
                                                                        facebook_response['currency'])
        }

        return mapped_budget_validation_response

    @classmethod
    def handle(cls, account_id: typing.AnyStr = None, access_token: typing.AnyStr = None) -> typing.Dict:
        facebook_budget_validation_url = cls.__facebook_budget_validation_url.substitute(account_id=account_id,
                                                                                         access_token=access_token)
        response_facebook = requests.get(facebook_budget_validation_url)
        response_facebook = response_facebook.json()

        if 'error' in response_facebook.keys():
            raise Exception(response_facebook['error'])

        response = cls.map_budget_validation_response(response_facebook)
        return response
