import logging
from dataclasses import asdict

from Core.Tools.QueryBuilder.QueryBuilderGoogleFilter import QueryBuilderGoogleFilters
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridGoogleOperator
from Core.Web.GoogleAdsAPI.AdsAPI.AdsBaseClient import AdsBaseClient
from Core.Web.GoogleAdsAPI.GAQLBuilder.GAQLBuilder import GAQLBuilder
from Core.Web.GoogleAdsAPI.Models.GoogleAttributeFieldsMetadata import GoogleAttributeFieldsMetadata
from Core.Web.GoogleAdsAPI.Models.GoogleFieldType import GoogleFieldType, GoogleResourceType
from Core.Web.GoogleAdsAPI.Models.GoogleMetricFieldsMetadata import GoogleMetricFieldsMetadata
from Core.Web.GoogleAdsAPI.Models.GoogleSegmentFieldsMetadata import GoogleSegmentFieldsMetadata
from GoogleAccounts.Infrastructure.Domain.GoogleAdAccountInsightsResponse import AdAccountInsightsResponse

logger = logging.getLogger(__name__)


class AdAccountInsightsClient(AdsBaseClient):
    __ACCOUNT_FIELDS = [
        GoogleAttributeFieldsMetadata.customer_id,
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

    __CHILD_FIELDS = [
        GoogleAttributeFieldsMetadata.customer_client_id,
        GoogleAttributeFieldsMetadata.client_descriptive_name,
    ]

    def get_account_insights(self, command, manager_id):

        child_where_conditions = [
            QueryBuilderGoogleFilters(
                GoogleAttributeFieldsMetadata.level.resource_type.value
                + "."
                + GoogleAttributeFieldsMetadata.level.field_name,
                AgGridGoogleOperator.LESS_THAN_OR_EQUAL,
                1,
            ),
        ]

        child_query = (
            GAQLBuilder()
            .select_(self.__CHILD_FIELDS)
            .from_(GoogleResourceType.CUSTOMER_CLIENT)
            .where_(child_where_conditions)
            .build_()
        )

        report_where_conditions = [
            QueryBuilderGoogleFilters(
                GoogleSegmentFieldsMetadata.date.field_type.value + "." + GoogleSegmentFieldsMetadata.date.field_name,
                AgGridGoogleOperator.BETWEEN,
                [command.from_date, command.to_date],
            ),
        ]

        report_query = (
            GAQLBuilder()
            .select_(self.__ACCOUNT_FIELDS)
            .from_(GoogleResourceType.CUSTOMER)
            .where_(report_where_conditions)
            .limit_(100)
            .build_()
        )

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
