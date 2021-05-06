from dataclasses import asdict

from Core.Web.GoogleAdsAPI.AdsAPI.AdsBaseClient import AdsBaseClient
from Core.Web.GoogleAdsAPI.GAQLBuilder.GAQLBuilder import GAQLBuilder
from Core.Web.GoogleAdsAPI.Mappings.LevelMapping import Level
from Core.Web.GoogleAdsAPI.Models.GoogleAttributeFieldsMetadata import GoogleAttributeFieldsMetadata
from Core.Web.GoogleAdsAPI.Models.GoogleMetricFieldsMetadata import GoogleMetricFieldsMetadata
from GoogleTuring.Infrastructure.Domain.Structures.GooglePerformanceInsightsResponse import (
    GooglePerformanceInsightsResponse,
)


class PerformanceInsightsClient(AdsBaseClient):
    __PERFORMANCE_FIELDS = [
        GoogleMetricFieldsMetadata.impressions,
        GoogleMetricFieldsMetadata.ctr,
        GoogleMetricFieldsMetadata.average_cpc,
        GoogleMetricFieldsMetadata.clicks,  # TODO find unique_clicks and reach in google ads API if available
    ]

    def get_performance_insights(self, client_customer_id, filtering, sorting, level):
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

        ga_service = self.get_ad_service()
        query_response = ga_service.search_stream(customer_id=client_customer_id, query=query)

        response = []
        for batch in query_response:
            for row in batch.results:
                insights = GooglePerformanceInsightsResponse(
                    campaign_id=str(row.campaign.id),
                    campaign_name=row.campaign.name,
                    impressions=row.metrics.impressions,
                    unique_link_clicks=row.metrics.clicks,
                    ctr_all=row.metrics.ctr,
                    cpc_all=row.metrics.average_cpc,
                    reach=None,
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

                response.append(asdict(insights))

        return response
