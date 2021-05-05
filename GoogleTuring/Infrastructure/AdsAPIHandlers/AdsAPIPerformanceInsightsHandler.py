import logging

from google.ads.googleads.errors import GoogleAdsException

from GoogleTuring.Infrastructure.GoogleAdsAPI.PerformanceInsightsClient import PerformanceInsightsClient

logger = logging.getLogger(__name__)


class AdsAPIPerformanceInsightsHandler:
    @classmethod
    def _build_client(cls, config, refresh_token, manager_id=None):
        client = PerformanceInsightsClient(config=config, refresh_token=refresh_token, manager_id=manager_id)
        # TODO look into setting login_customer_id method in ads API
        # ads_client.set_client_customer_id(int(manager_id))
        return client

    @classmethod
    def get_performance_insights(cls, config, refresh_token, query_builder_request_parser):
        client_customer_id = query_builder_request_parser.google_id
        client_manager_id = query_builder_request_parser.manager_id
        level = query_builder_request_parser.level
        filtering = query_builder_request_parser.filters
        sorting = query_builder_request_parser.sorting

        performance_insights_client = cls._build_client(config, refresh_token, client_manager_id)

        try:
            return performance_insights_client.get_performance_insights(
                client_customer_id=client_customer_id,
                filtering=filtering,
                sorting=sorting,
                level=level,
            )
        except GoogleAdsException as ex:
            logger.exception(f"Request with ID '{ex.request_id}' failed with status {ex.error.code().name}")
