from dataclasses import asdict

from Core.Web.GoogleAdsAPI.AdsAPI.AdsBaseClient import AdsBaseClient
from Core.Web.GoogleAdsAPI.GAQLBuilder.GAQLBuilder import GAQLBuilder
from Core.Web.GoogleAdsAPI.Mappings.LevelMapping import Level
from Core.Web.GoogleAdsAPI.Models.GoogleAttributeFieldsMetadata import GoogleAttributeFieldsMetadata
from Core.Web.GoogleAdsAPI.Models.GoogleMetricFieldsMetadata import GoogleMetricFieldsMetadata
from Core.Web.GoogleAdsAPI.Models.GoogleSegmentFieldsMetadata import GoogleSegmentFieldsMetadata
from GoogleTuring.Infrastructure.Domain.Structures.GooglePerformanceInsightsResponse import (
    GooglePerformanceInsightsResponse,
)


class InsightsReportClient(AdsBaseClient):
    __campaign_attributes = [
        GoogleAttributeFieldsMetadata.campaign_id,
        GoogleAttributeFieldsMetadata.campaign_name,
    ]

    __adgroup_attributes = [
        GoogleAttributeFieldsMetadata.adgroup_id,
        GoogleAttributeFieldsMetadata.adgroup_name,
    ]

    __keyword_attributes = [
        GoogleAttributeFieldsMetadata.resource_name,
        GoogleAttributeFieldsMetadata.keyword_id,
        GoogleAttributeFieldsMetadata.keyword_text,
        GoogleAttributeFieldsMetadata.keyword_match_type,
    ]

    def get_insights_report(self, client_customer_id, filtering, sorting, level, fields, breakdown_column):
        field_names = fields

        if level == Level.CAMPAIGN.value:
            field_names.extend(self.__campaign_attributes)

        elif level == Level.ADGROUP.value:
            field_names.extend([*self.__adgroup_attributes, *self.__campaign_attributes])

        elif level == Level.KEYWORDS.value:
            field_names.extend([*self.__adgroup_attributes, *self.__campaign_attributes, *self.__keyword_attributes])

        # building GAQL query
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
                breakdown_metric = InsightsReportClient.__get_breakdown_metric(row, breakdown_column)
                insights = GooglePerformanceInsightsResponse(
                    date=row.segments.date,
                    device=str(row.segments.device).split(".")[1],
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

                insights = {k: v for k, v in asdict(insights).items() if v is not None and k != breakdown_column}

                insight_parsed = False
                for resp in response:
                    if resp.get(breakdown_column) == breakdown_metric:
                        resp["report"].append(insights)
                        insight_parsed = True
                        break
                if not insight_parsed:
                    response.append({breakdown_column: breakdown_metric, "report": [insights]})

        return response

    @staticmethod
    def __get_breakdown_metric(row, breakdown_column):
        columns = {
            "campaign_id": str(row.campaign.id),
            "adgroup_id": str(row.ad_group.id),
            "keyword_id": str(row.ad_group_criterion.criterion_id),
            "date": str(row.segments.date),
            "device": str(row.segments.device).split(".")[1],
        }

        breakdown_metric = columns.get(breakdown_column)
        if breakdown_metric:
            return breakdown_metric
        else:
            raise ValueError("Invalid breakdown provided")
