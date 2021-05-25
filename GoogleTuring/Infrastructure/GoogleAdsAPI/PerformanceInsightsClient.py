import concurrent.futures
from dataclasses import asdict

from Core.Web.GoogleAdsAPI.AdsAPI.AdsBaseClient import AdsBaseClient
from Core.Web.GoogleAdsAPI.AdsAPIMappings.AdsAPIInsightsMapper import AdsAPIInsightsMapper
from Core.Web.GoogleAdsAPI.AdsAPIMappings.LevelMapping import GoogleLevelPlural, Level
from Core.Web.GoogleAdsAPI.GAQLBuilder.GAQLBuilder import GAQLBuilder
from Core.Web.GoogleAdsAPI.Models.GoogleAttributeFieldsMetadata import GoogleAttributeFieldsMetadata
from Core.Web.GoogleAdsAPI.Models.GoogleFieldType import GoogleResourceType
from Core.Web.GoogleAdsAPI.Models.GoogleMetricFieldsMetadata import GoogleMetricFieldsMetadata
from GoogleTuring.Infrastructure.Domain.Enums.AudienceTypeEnum import AudienceTypeEnum
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

    def get_performance_insights(
        self, client_customer_id, fields, filtering, sorting, level, page_size, next_page_token=None
    ):
        field_names = fields

        if level == Level.AUDIENCE.value:
            audience_attributes = [
                GoogleAttributeFieldsMetadata.user_interest,
                GoogleAttributeFieldsMetadata.custom_intent,
            ]

            field_names.extend([*audience_attributes])

        query = GAQLBuilder().select_(field_names).from_(level)

        if len(filtering) > 0:
            query = query.where_(filtering)

        if sorting:
            query = query.order_by_(sorting.field, sorting.ascending)

        query = query.build_()

        budgets = None
        if level == Level.CAMPAIGN.value:
            budgets = self.get_campaign_budgets(client_customer_id)

        query_response = self.perform_search(query, client_customer_id, page_size, next_page_token)

        next_page_token = query_response.next_page_token if query_response.next_page_token != "" else None

        if level == Level.AUDIENCE.value:
            return self.parse_audience_query_response(
                query_response, page_size, next_page_token, client_customer_id, fields, level
            )
        else:
            return self.parse_level_query_response(
                fields, query_response, page_size, next_page_token, client_customer_id, level, budgets
            )

    def parse_level_query_response(
        self, fields, query_response, page_size, next_page_token, client_customer_id, level, budgets=None
    ):
        response = []
        for row in query_response:
            if len(response) == page_size:
                return next_page_token, response, self.get_summary(client_customer_id, level)

            insights = AdsAPIInsightsMapper().map(fields, row)
            if insights.get("campaign_budget") and budgets:
                insights["campaign_budget"] = budgets[row.campaign.campaign_budget]

            response.append(insights)

        return next_page_token, response, self.get_summary(client_customer_id, level)

    def parse_audience_query_response(
        self, query_response, page_size, next_page_token, client_customer_id, fields, level
    ):
        response = []
        for row in query_response:
            if len(response) == page_size:
                response = self.process_audience_data(response, client_customer_id)
                return next_page_token, response, self.get_summary(client_customer_id, level)

            insights = AdsAPIInsightsMapper().map(fields, row)

            # TODO clean + implement postprocessing function
            insights.update(
                {
                    "audience": row.ad_group_criterion.user_interest.user_interest_category
                    if row.ad_group_criterion.user_interest.user_interest_category != ""
                    else row.ad_group_criterion.custom_intent.custom_intent,
                    "type": getattr(AudienceTypeEnum, row.ad_group_criterion.type_.name)
                    .name.replace("_", " ")
                    .capitalize(),
                }
            )
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
            # row["audience"] = results.get(row["audience"], row["audience"])
            row.update(results.get(row["audience"], row["audience"]))

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
                        "audience": row.user_interest.name,
                        "audience_category": row.user_interest.user_interest_parent,
                        "type": AudienceTypeEnum(row.user_interest.taxonomy_type).name.replace("_", " ").capitalize(),
                    }
                }
            )

        # getting details for category (parent name)
        for row in user_interest_response:
            user_interest_response[row]["audience_category"] = user_interest_response.get(
                user_interest_response[row]["audience_category"], user_interest_response[row]["audience_category"]
            )
            if type(user_interest_response[row]["audience_category"]) is dict:
                user_interest_response[row]["audience_category"] = user_interest_response[row]["audience_category"].get(
                    "audience"
                )

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
        # TODO optimize and clean this section
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
                        "audience": row.custom_interest.name,
                        "audience_category": "Custom audience",
                        "description": row.custom_interest.description,
                        "members": member_list,
                    }
                }
            )

        return custom_interest_response

    def get_campaign_budgets(self, client_customer_id):
        budget_query = (
            GAQLBuilder()
            .select_([GoogleAttributeFieldsMetadata.campaign_budget_amount_micros])
            .from_(GoogleResourceType.CAMPAIGN_BUDGET)
            .build_()
        )

        query_response = self.perform_search(budget_query, client_customer_id)

        budgets = {}
        for row in query_response:
            budgets.update({row.campaign_budget.resource_name: round(row.campaign_budget.amount_micros / 10 ** 6, 2)})

        return budgets
