from GoogleTuring.Infrastructure.AdWordsAPIHandlers.AdWordsAPIBaseHandler import AdWordsAPIBaseHandler
from GoogleTuring.Infrastructure.Domain.Enums.FiledGoogleInsightsTableEnum import REPORT_TO_STATUS_FIELD
from GoogleTuring.Infrastructure.GoogleAdWordsAPI.AdWordsInsightsClient import AdWordsInsightsClient


class AdWordsAPIInsightsHandler(AdWordsAPIBaseHandler):
    @classmethod
    def _build_client(cls, config, client_customer_id, permanent_token):
        adwords_client = AdWordsInsightsClient(config=config, refresh_token=permanent_token)
        adwords_client.set_client_customer_id(client_customer_id)
        return adwords_client

    @classmethod
    def get_insights(cls, config, permanent_token, client_customer_id, report, fields, start_date, end_date):
        adwords_client = cls._build_client(config, client_customer_id, permanent_token)
        report_name = report.value
        status_field = REPORT_TO_STATUS_FIELD[report]
        return adwords_client.get_insights(report_name=report_name, status_field=status_field,
                                           fields=fields, start_date=start_date, end_date=end_date)

    @classmethod
    def get_insights_with_totals(cls, config, permanent_token, client_customer_id, report, fields, start_date,
                                 end_date):
        adwords_client = cls._build_client(config, client_customer_id, permanent_token)
        report_name = report.value
        status_field = REPORT_TO_STATUS_FIELD[report]
        return adwords_client.get_insights_with_totals(report_name=report_name, status_field=status_field,
                                                       fields=fields, start_date=start_date, end_date=end_date)
