from GoogleTuring.Infrastructure.AdWordsAPIHandlers.AdWordsAPIBaseHandler import AdWordsAPIBaseHandler
from GoogleTuring.Infrastructure.Domain.Enums.FiledGoogleInsightsTableEnum import LEVEL_TO_STATUS_FIELD
from GoogleTuring.Infrastructure.GoogleAdWordsAPI.AdWordsInsightsClient import AdWordsInsightsClient


class AdWordsAPIInsightsHandler(AdWordsAPIBaseHandler):
    @classmethod
    def _build_client(cls, config, client_customer_id, permanent_token):
        adwords_client = AdWordsInsightsClient(config=config, refresh_token=permanent_token)
        adwords_client.set_client_customer_id(client_customer_id)
        return adwords_client

    @classmethod
    def get_insights(cls, config, permanent_token, query_builder_request_parser):
        client_customer_id = query_builder_request_parser.google_id
        report = query_builder_request_parser.report
        report_name = report.value
        level = query_builder_request_parser.level
        status_field = LEVEL_TO_STATUS_FIELD[level]
        fields = query_builder_request_parser.google_fields
        start_date = query_builder_request_parser.start_date
        end_date = query_builder_request_parser.end_date
        time_increment = query_builder_request_parser.time_increment
        filtering = query_builder_request_parser.filtering

        adwords_client = cls._build_client(config, client_customer_id, permanent_token)
        return adwords_client.get_insights(
            report_name=report_name,
            status_field=status_field,
            fields=fields,
            start_date=start_date,
            end_date=end_date,
            time_increment=time_increment,
            filtering=filtering,
            level=level,
        )

    @classmethod
    def get_insights_with_totals(cls, config, permanent_token, query_builder_request_parser):
        client_customer_id = query_builder_request_parser.google_id
        report = query_builder_request_parser.report
        report_name = report.value
        level = query_builder_request_parser.level
        status_field = LEVEL_TO_STATUS_FIELD[level]
        fields = query_builder_request_parser.google_fields
        start_date = query_builder_request_parser.start_date
        end_date = query_builder_request_parser.end_date
        time_increment = query_builder_request_parser.time_increment
        filtering = query_builder_request_parser.filtering

        adwords_client = cls._build_client(config, client_customer_id, permanent_token)
        return adwords_client.get_insights_with_totals(
            report_name=report_name,
            status_field=status_field,
            fields=fields,
            start_date=start_date,
            end_date=end_date,
            time_increment=time_increment,
            filtering=filtering,
            level=level,
        )
