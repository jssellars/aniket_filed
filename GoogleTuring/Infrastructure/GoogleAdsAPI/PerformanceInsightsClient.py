import logging
from dataclasses import asdict

from Core.Web.GoogleAdsAPI.AdsAPI.AdsBaseClient import AdsBaseClient
from GoogleAccounts.Infrastructure.Domain.GoogleAttributeFieldsMetadata import GoogleAttributeFieldsMetadata
from GoogleAccounts.Infrastructure.Domain.GoogleFieldType import GoogleFieldType
from GoogleAccounts.Infrastructure.Domain.GoogleMetricFieldsMetadata import GoogleMetricFieldsMetadata
from GoogleAccounts.Infrastructure.Domain.GoogleSegmentFieldsMetadata import GoogleSegmentFieldsMetadata
from GoogleTuring.Infrastructure.Domain.Structures.GooglePerformanceInsightsResponse import (
    GooglePerformanceInsightsResponse,
)
from GoogleTuring.Infrastructure.Mappings.LevelMapping import Level


class PerformanceInsightsClient(AdsBaseClient):
    __PERFORMANCE_FIELDS = [
        GoogleMetricFieldsMetadata.impressions,
        GoogleMetricFieldsMetadata.ctr,
        GoogleMetricFieldsMetadata.average_cpc,
        GoogleMetricFieldsMetadata.clicks,  # TODO find unique_clicks and reach in google ads API if available
    ]

    __ATTRIBUTE_FIELDS = [
        GoogleAttributeFieldsMetadata.id,
        GoogleAttributeFieldsMetadata.name,
    ]

    __KEYWORD_FIELDS = [
        GoogleAttributeFieldsMetadata.resource_name,
        GoogleAttributeFieldsMetadata.criterion_id,
        GoogleAttributeFieldsMetadata.keyword_text,
        GoogleAttributeFieldsMetadata.keyword_match_type,
    ]

    def get_performance_insights(self, client_customer_id, filtering, level):
        field_names = [
            level + "." + field.field_name
            if field.field_type.value == GoogleFieldType.ATTRIBUTE.value
            else field.field_type.value + "." + field.field_name
            for field in self.__PERFORMANCE_FIELDS
        ]

        if level == Level.CAMPAIGN.value:
            Campaign_attributes = [Level.CAMPAIGN.value + "." + field.field_name for field in self.__ATTRIBUTE_FIELDS]
            field_names.extend(Campaign_attributes)

        elif level == Level.ADGROUP.value:
            Campaign_attributes = [Level.CAMPAIGN.value + "." + field.field_name for field in self.__ATTRIBUTE_FIELDS]
            Adgroup_attributes = [Level.ADGROUP.value + "." + field.field_name for field in self.__ATTRIBUTE_FIELDS]
            field_names.extend([*Adgroup_attributes, *Campaign_attributes])

        elif level == Level.KEYWORDS.value:
            Campaign_attributes = [Level.CAMPAIGN.value + "." + field.field_name for field in self.__ATTRIBUTE_FIELDS]
            Adgroup_attributes = [Level.ADGROUP.value + "." + field.field_name for field in self.__ATTRIBUTE_FIELDS]
            keyword_attributes = [field.resource_type.value + "." + field.field_name for field in self.__KEYWORD_FIELDS]

            field_names.extend([*Adgroup_attributes, *Campaign_attributes, *keyword_attributes])

        query = f"""
                    SELECT {','.join(field for field in field_names)}
                    FROM {level}
                """

        if len(filtering) > 0:
            filters = " AND ".join(filters for filters in filtering)
            query += "WHERE " + filters

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
                    cpc_all=None,
                    reach=None,
                )

                if level == Level.ADGROUP.value:
                    insights.adgroup_id = str(row.ad_group.id)
                    insights.adgroup_name = row.ad_group.name

                elif level == Level.KEYWORDS.value:
                    insights.adgroup_id = str(row.ad_group.id)
                    insights.adgroup_name = row.ad_group.name
                    insights.criterion_id = str(row.ad_group_criterion.criterion_id)
                    insights.keyword_text = row.ad_group_criterion.keyword.text
                    insights.keyword_match_type = row.ad_group_criterion.keyword.match_type.name

                response.append(asdict(insights))

        return response
