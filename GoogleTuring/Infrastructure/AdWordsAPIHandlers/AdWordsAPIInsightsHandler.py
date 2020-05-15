from GoogleTuring.Api.Startup import startup
from GoogleTuring.Infrastructure.AdWordsAPIHandlers.AdWordsAPIBaseHandler import AdWordsAPIBaseHandler
from GoogleTuring.Infrastructure.Domain.Enums.FiledGoogleInsightsTableEnum import REPORT_TO_STATUS_FIELD
from GoogleTuring.Infrastructure.GoogleAdWordsAPI.AdWordsInsightsClient import AdWordsInsightsClient


class AdWordsAPIInsightsHandler(AdWordsAPIBaseHandler):
    @classmethod
    def _build_client(cls, client_customer_id, permanent_token):
        adwords_client = AdWordsInsightsClient(startup.google_config, refresh_token=permanent_token)
        adwords_client.set_client_customer_id(client_customer_id)
        return adwords_client

    @classmethod
    def get_insights(cls, permanent_token, client_customer_id, report, fields, time_range):
        adwords_client = cls._build_client(client_customer_id, permanent_token)
        report_name = report.value
        status_field = REPORT_TO_STATUS_FIELD[report]
        return adwords_client.get_insights(report_name=report_name, status_field=status_field,
                                           fields=fields, time_range=time_range)

    @classmethod
    def get_insights_with_totals(cls, permanent_token, client_customer_id, report, fields, time_range):
        adwords_client = cls._build_client(client_customer_id, permanent_token)
        report_name = report.value
        status_field = REPORT_TO_STATUS_FIELD[report]
        return adwords_client.get_insights_with_totals(report_name=report_name, status_field=status_field,
                                                       fields=fields, time_range=time_range)
