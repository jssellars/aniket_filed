from dataclasses import asdict

from Core.Web.GoogleAdsAPI.AdsAPI.AdsBaseClient import AdsBaseClient
from Core.Web.GoogleAdsAPI.GAQLBuilder.GAQLBuilder import GAQLBuilder
from Core.Web.GoogleAdsAPI.Mappings.LevelMapping import GoogleLevelPlural, Level
from Core.Web.GoogleAdsAPI.Models.GoogleAttributeFieldsMetadata import GoogleAttributeFieldsMetadata
from Core.Web.GoogleAdsAPI.Models.GoogleFieldType import GoogleResourceType
from Core.Web.GoogleAdsAPI.Models.GoogleMetricFieldsMetadata import GoogleMetricFieldsMetadata
from GoogleTuring.Infrastructure.Domain.Structures.GoogleInsightsSummaryResponse import GoogleInsightsSummaryResponse
from GoogleTuring.Infrastructure.Domain.Structures.GooglePerformanceInsightsResponse import (
    GooglePerformanceInsightsResponse,
)


class PerformanceInsightsClient(AdsBaseClient):
    __PERFORMANCE_FIELDS = [
        GoogleMetricFieldsMetadata.impressions,
        GoogleMetricFieldsMetadata.ctr,
        GoogleMetricFieldsMetadata.average_cpc,
        GoogleMetricFieldsMetadata.clicks,
    ]

    def get_performance_insights(self, client_customer_id, filtering, sorting, level, page_size, next_page_token=None):
        field_names = []
        field_names.extend(self.__PERFORMANCE_FIELDS)

        if level == Level.CAMPAIGN.value:
            campaign_attributes = [
                GoogleAttributeFieldsMetadata.campaign_id,
                GoogleAttributeFieldsMetadata.campaign_name,
            ]

            field_names.extend(campaign_attributes)

        elif level == Level.ADGROUP.value:
            campaign_attributes = [
                GoogleAttributeFieldsMetadata.campaign_id,
                GoogleAttributeFieldsMetadata.campaign_name,
            ]

            adgroup_attributes = [
                GoogleAttributeFieldsMetadata.adgroup_id,
                GoogleAttributeFieldsMetadata.adgroup_name,
            ]

            field_names.extend([*adgroup_attributes, *campaign_attributes])

        elif level == Level.KEYWORDS.value:
            campaign_attributes = [
                GoogleAttributeFieldsMetadata.campaign_id,
                GoogleAttributeFieldsMetadata.campaign_name,
            ]

            adgroup_attributes = [
                GoogleAttributeFieldsMetadata.adgroup_id,
                GoogleAttributeFieldsMetadata.adgroup_name,
            ]

            keyword_attributes = [
                GoogleAttributeFieldsMetadata.resource_name,
                GoogleAttributeFieldsMetadata.keyword_id,
                GoogleAttributeFieldsMetadata.keyword_text,
                GoogleAttributeFieldsMetadata.keyword_match_type,
            ]

            field_names.extend([*adgroup_attributes, *campaign_attributes, *keyword_attributes])

        query = GAQLBuilder().select_(field_names).from_(level)

        if len(filtering) > 0:
            query = query.where_(filtering)

        if sorting:
            query = query.order_by_(sorting.field, sorting.ascending)

        query = query.build_()

        query_response = self.perform_search(query, client_customer_id, page_size, next_page_token)

        next_page_token = query_response.next_page_token if query_response.next_page_token != "" else None

        response = []
        for row in query_response:
            if len(response) == page_size:
                return next_page_token, response, self.get_summary(client_customer_id, level)

            insights = GooglePerformanceInsightsResponse(
                campaign_id=str(row.campaign.id),
                campaign_name=row.campaign.name,
                impressions=row.metrics.impressions,
                clicks=row.metrics.clicks,
                ctr=row.metrics.ctr,
                average_cpc=row.metrics.average_cpc / 10 ** 4,
            )

            if level == Level.ADGROUP.value:
                insights.adgroup_id = str(row.ad_group.id)
                insights.adgroup_name = row.ad_group.name

            elif level == Level.KEYWORDS.value:
                insights.adgroup_id = str(row.ad_group.id)
                insights.adgroup_name = row.ad_group.name
                insights.keyword_id = str(row.ad_group_criterion.criterion_id)
                insights.keyword_text = row.ad_group_criterion.keyword.text
                insights.keyword_match_type = row.ad_group_criterion.keyword.match_type.name

            insights = {k: v for k, v in asdict(insights).items() if v is not None}

            response.append(insights)

        return next_page_token, response, self.get_summary(client_customer_id, level)

    def perform_search(self, query, client_customer_id, page_size, next_page_token):
        ga_service = self.get_ad_service()
        search_request = self.get_search_google_ads_request_type()
        search_request.customer_id = client_customer_id
        search_request.query = query
        search_request.page_size = page_size

        if next_page_token:
            search_request.page_token = next_page_token

        return ga_service.search(request=search_request)

    def get_summary(self, client_customer_id, level):
        query = GAQLBuilder().select_(self.__PERFORMANCE_FIELDS).from_(GoogleResourceType.CUSTOMER).build_()
        ga_service = self.get_ad_service()
        query_response = ga_service.search_stream(customer_id=client_customer_id, query=query)

        for batch in query_response:
            for row in batch.results:
                summary = GoogleInsightsSummaryResponse(
                    impressions=row.metrics.impressions,
                    clicks=row.metrics.clicks,
                    ctr=row.metrics.ctr,
                    average_cpc=row.metrics.average_cpc / 10 ** 4,
                )
                summary = asdict(summary)

                level_display_name = "".join(level.split("_")) if level != Level.KEYWORDS.value else level.split("_")[0]
                summary.update({f"{level_display_name}_name": GoogleLevelPlural[level.upper()].value.capitalize()})

                return [summary]
