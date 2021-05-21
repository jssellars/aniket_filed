import concurrent.futures
from dataclasses import asdict

from Core.Web.GoogleAdsAPI.AdsAPI.AdsBaseClient import AdsBaseClient
from Core.Web.GoogleAdsAPI.GAQLBuilder.GAQLBuilder import GAQLBuilder
from Core.Web.GoogleAdsAPI.Mappings.LevelMapping import GoogleLevelPlural, Level
from Core.Web.GoogleAdsAPI.Models.GoogleAttributeFieldsMetadata import GoogleAttributeFieldsMetadata
from Core.Web.GoogleAdsAPI.Models.GoogleFieldType import GoogleResourceType
from Core.Web.GoogleAdsAPI.Models.GoogleMetricFieldsMetadata import GoogleMetricFieldsMetadata
from GoogleTuring.Infrastructure.Domain.Structures.GoogleInsightsSummaryResponse import GoogleInsightsSummaryResponse
from GoogleTuring.Infrastructure.Domain.Structures.GoogleResponses import (
    GoogleAudienceResponse,
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

        elif level == Level.AUDIENCE.value:
            campaign_attributes = [
                GoogleAttributeFieldsMetadata.campaign_id,
                GoogleAttributeFieldsMetadata.campaign_name,
            ]

            adgroup_attributes = [
                GoogleAttributeFieldsMetadata.adgroup_id,
                GoogleAttributeFieldsMetadata.adgroup_name,
            ]

            audience_attributes = [
                GoogleAttributeFieldsMetadata.ad_group_criterion_resource_name,
                GoogleAttributeFieldsMetadata.ad_group_criterion_id,
                GoogleAttributeFieldsMetadata.ad_group_criterion_type,
                GoogleAttributeFieldsMetadata.user_interest,
                GoogleAttributeFieldsMetadata.custom_intent,
                GoogleAttributeFieldsMetadata.ad_group_criterion_status,
            ]

            field_names.extend([*adgroup_attributes, *campaign_attributes, *audience_attributes])

        query = GAQLBuilder().select_(field_names).from_(level)

        if len(filtering) > 0:
            query = query.where_(filtering)

        if sorting:
            query = query.order_by_(sorting.field, sorting.ascending)

        query = query.build_()

        query_response = self.perform_search(query, client_customer_id, page_size, next_page_token)

        next_page_token = query_response.next_page_token if query_response.next_page_token != "" else None

        if level == Level.AUDIENCE.value:
            return self.parse_audience_query_response(
                query_response, page_size, next_page_token, client_customer_id, level
            )
        else:
            return self.parse_level_query_response(
                query_response, page_size, next_page_token, client_customer_id, level
            )

    def parse_level_query_response(self, query_response, page_size, next_page_token, client_customer_id, level):
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

    def parse_audience_query_response(self, query_response, page_size, next_page_token, client_customer_id, level):
        response = []
        for row in query_response:
            if len(response) == page_size:
                response = self.process_audience_data(response, client_customer_id)
                return next_page_token, response, self.get_summary(client_customer_id, level)

            insights = GoogleAudienceResponse(
                campaign_id=str(row.campaign.id),
                campaign_name=row.campaign.name,
                adgroup_id=str(row.ad_group.id),
                adgroup_name=row.ad_group.name,
                criterion_id=row.ad_group_criterion.criterion_id,
                impressions=row.metrics.impressions,
                clicks=row.metrics.clicks,
                ctr=row.metrics.ctr,
                average_cpc=row.metrics.average_cpc / 10 ** 4,
                audience=row.ad_group_criterion.user_interest.user_interest_category
                if row.ad_group_criterion.user_interest.user_interest_category != ""
                else row.ad_group_criterion.custom_intent.custom_intent,
                audience_type=row.ad_group_criterion.type_.name,
            )

            insights = {k: v for k, v in asdict(insights).items() if v is not None}

            response.append(insights)

        response = self.process_audience_data(response, client_customer_id)

        return next_page_token, response, self.get_summary(client_customer_id, level)

    def perform_search(self, query, client_customer_id, page_size=None, next_page_token=None):
        ga_service = self.get_ad_service()
        search_request = self.get_search_google_ads_request_type()
        search_request.customer_id = client_customer_id
        search_request.query = query

        if page_size:
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

    def process_audience_data(self, response, client_customer_id):
        # fetching details of two different types of audiences: user_interest and custom_interest
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.get_user_interest, client_customer_id),
                executor.submit(self.get_custom_interest, client_customer_id),
            ]

            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        # merging user_interest and custom_interest response dict in single dict
        results = {k: v for list_item in results for (k, v) in list_item.items()}

        # replacing audience resource name with audience details
        for row in response:
            row["audience"] = results.get(row["audience"], row["audience"])

        return response

    def get_user_interest(self, client_customer_id):
        fields = [
            GoogleAttributeFieldsMetadata.user_interest_taxonomy_type,
            GoogleAttributeFieldsMetadata.user_interest_name,
            GoogleAttributeFieldsMetadata.user_interest_resource_name,
            GoogleAttributeFieldsMetadata.user_interest_id,
            GoogleAttributeFieldsMetadata.user_interest_parent,
        ]

        query = GAQLBuilder().select_(fields).from_(GoogleResourceType.USER_INTEREST).build_()

        query_response = self.perform_search(query, client_customer_id)

        # generating resource_name, audience detail dict from query response
        user_interest_response = {}
        for row in query_response:
            user_interest_response.update(
                {
                    row.user_interest.resource_name: {
                        "name": row.user_interest.name,
                        "category": row.user_interest.user_interest_parent,
                        "taxonomy_type": row.user_interest.taxonomy_type.name,
                    }
                }
            )

        # getting details for category (parent name)
        for row in user_interest_response:
            user_interest_response[row]["category"] = user_interest_response.get(
                user_interest_response[row]["category"], user_interest_response[row]["category"]
            )
            if type(user_interest_response[row]["category"]) is dict:
                user_interest_response[row]["category"] = user_interest_response[row]["category"].get("name")

        return user_interest_response

    def get_custom_interest(self, client_customer_id):
        fields = [
            GoogleAttributeFieldsMetadata.custom_interest_id,
            GoogleAttributeFieldsMetadata.custom_interest_name,
            GoogleAttributeFieldsMetadata.custom_interest_resource_name,
            GoogleAttributeFieldsMetadata.custom_interest_status,
            GoogleAttributeFieldsMetadata.custom_interest_type,
            GoogleAttributeFieldsMetadata.custom_interest_members,
            GoogleAttributeFieldsMetadata.custom_interest_description,
        ]

        query = GAQLBuilder().select_(fields).from_(GoogleResourceType.CUSTOM_INTEREST).build_()

        query_response = self.perform_search(query, client_customer_id)

        # generating resource_name, audience detail dict from query response
        # TODO optimize
        custom_interest_response = {}
        for row in query_response:
            members = [
                {"members": member.parameter, "member_type": member.member_type.name}
                for member in row.custom_interest.members
            ]

            member_list = []
            for member in members:
                parsed = False
                for re in member_list:
                    if member["member_type"] == re.get("member_type"):
                        re["members"].append(member["members"])
                        parsed = True
                        break
                if not parsed:
                    member_list.append({"member_type": member["member_type"], "members": [member["members"]]})

            custom_interest_response.update(
                {
                    row.custom_interest.resource_name: {
                        "name": row.custom_interest.name,
                        "description": row.custom_interest.description,
                        "members": member_list,
                    }
                }
            )

        return custom_interest_response
