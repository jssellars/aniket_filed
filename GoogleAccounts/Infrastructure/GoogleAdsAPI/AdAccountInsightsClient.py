import logging
from dataclasses import asdict

from Core.Web.GoogleAdsAPI.AdsAPI.AdsBaseClient import AdsBaseClient
from Core.Web.GoogleAdsAPI.Models.GoogleAttributeFieldsMetadata import GoogleAttributeFieldsMetadata
from Core.Web.GoogleAdsAPI.Models.GoogleFieldType import GoogleFieldType, GoogleResourceType
from Core.Web.GoogleAdsAPI.Models.GoogleMetricFieldsMetadata import GoogleMetricFieldsMetadata
from Core.Web.GoogleAdsAPI.Models.GoogleSegmentFieldsMetadata import GoogleSegmentFieldsMetadata
from GoogleAccounts.Infrastructure.Domain.GoogleAdAccountInsightsResponse import AdAccountInsightsResponse

logger = logging.getLogger(__name__)


class AdAccountInsightsClient(AdsBaseClient):
    __ACCOUNT_FIELDS = [
        GoogleAttributeFieldsMetadata.id,
        GoogleAttributeFieldsMetadata.descriptive_name,
        GoogleAttributeFieldsMetadata.currency_code,
        # direct manager
        # account type
        GoogleMetricFieldsMetadata.clicks,
        GoogleMetricFieldsMetadata.impressions,
        GoogleMetricFieldsMetadata.ctr,
        GoogleMetricFieldsMetadata.average_cpc,
        GoogleMetricFieldsMetadata.average_cpm,
        GoogleMetricFieldsMetadata.average_cost,
        GoogleMetricFieldsMetadata.conversions,
        # GoogleMetricFieldsMetadata.conversion_rate,
        # account labels
        GoogleMetricFieldsMetadata.cost_per_conversion,
    ]

    def get_account_insights(self, command, manager_id):
        field_names = [
            field.resource_type.value + "." + field.field_name
            if field.field_type.value == GoogleFieldType.ATTRIBUTE.value
            else field.field_type.value + "." + field.field_name
            for field in self.__ACCOUNT_FIELDS
        ]
        child_query = f"""
                       SELECT {GoogleResourceType.CUSTOMER_CLIENT.value + "." +
                               GoogleAttributeFieldsMetadata.id.field_name},
                               {GoogleResourceType.CUSTOMER_CLIENT.value + "." +
                               GoogleAttributeFieldsMetadata.descriptive_name.field_name}
                       FROM {GoogleResourceType.CUSTOMER_CLIENT.value}
                       WHERE {GoogleAttributeFieldsMetadata.level.resource_type.value + "." +
                              GoogleAttributeFieldsMetadata.level.field_name} <= 1
                   """

        report_query = f"""
                        SELECT {','.join(field for field in field_names)}
                        FROM {GoogleResourceType.CUSTOMER.value}
                        WHERE {GoogleSegmentFieldsMetadata.date.field_type.value + "." +
                               GoogleSegmentFieldsMetadata.date.field_name}
                        BETWEEN '{command.from_date}' AND '{command.to_date}'
                        LIMIT 100
                    """

        customer_clients = self.search(child_query, manager_id)

        response = []
        manager_name = None
        for googleads_row in customer_clients:
            customer_client = googleads_row.customer_client
            customer_client_id = str(customer_client.id)
            if customer_client_id == manager_id:
                manager_name = customer_client.descriptive_name

        for googleads_row in customer_clients:
            customer_client = googleads_row.customer_client
            customer_client_id = str(customer_client.id)

            try:
                results = self.search(report_query, customer_client_id)
                customer_info = next(iter(results))

                insights = AdAccountInsightsResponse(
                    account_id=str(customer_info.customer.id),
                    name=customer_info.customer.descriptive_name,
                    account_status=None,
                    business_id=manager_id,
                    business_manager=manager_name,
                    currency=customer_info.customer.currency_code,
                    amount_spent=round(
                        (customer_info.metrics.cost_per_conversion * customer_info.metrics.conversions) / 10 ** 6, 2
                    ),
                    cpc_all=round(customer_info.metrics.average_cpc / 10 ** 4, 2),
                    cpm=round(customer_info.metrics.average_cpm / 10 ** 4, 2),
                    purchase_cost=None,
                    ctr_all=customer_info.metrics.ctr,
                    unique_ctr_all=None,
                    impressions=customer_info.metrics.impressions,
                    unique_clicks_all=customer_info.metrics.clicks,
                    # not unique clicks
                    conversions=customer_info.metrics.conversions,
                    average_cost=customer_info.metrics.average_cost,
                )

                response.append(asdict(insights))

            except Exception as e:
                logger.exception(f"failed {customer_client_id}, {repr(e)}")

        return response

    def search(self, query, manager_id):
        googleads_service = self.get_ad_service()

        search_request = self.get_search_google_ads_request_type()
        search_request.customer_id = manager_id
        search_request.query = query
        search_request.page_size = 1000

        results = googleads_service.search(request=search_request)
        return results
