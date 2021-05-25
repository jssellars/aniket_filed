from google.api_core import protobuf_helpers

from Core.Tools.QueryBuilder.QueryBuilderGoogleMappers import QueryBuilderGoogleFilters
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridGoogleOperator
from Core.Web.GoogleAdsAPI.AdsAPI.AdsBaseClient import AdsBaseClient
from Core.Web.GoogleAdsAPI.AdsAPIMappings.EditFieldMapping import EditFieldMapping
from Core.Web.GoogleAdsAPI.AdsAPIMappings.LevelMapping import Level
from Core.Web.GoogleAdsAPI.GAQLBuilder.GAQLBuilder import GAQLBuilder
from Core.Web.GoogleAdsAPI.Models.GoogleAttributeFieldsMetadata import GoogleAttributeFieldsMetadata
from GoogleTuring.Infrastructure.Domain.StructureStatusEnum import StructureStatusEnum


class StructuresClient(AdsBaseClient):
    def __get_services(self, customer_id, level=None, campaign_id=None, ad_group_id=None, keyword_id=None):
        if not level:
            service = self.get_campaign_budget_service()
            return (
                service,
                self.get_campaign_budget_operation_type(),
                self.get_campaign_budget_path(customer_id, campaign_id),
                service.mutate_campaign_budgets,
            )

        if level == Level.CAMPAIGN.value:
            service = self.get_campaign_service()
            return (
                service,
                self.get_campaign_operation_type(),
                service.campaign_path(customer_id, campaign_id),
                service.mutate_campaigns,
            )
        elif level == Level.ADGROUP.value:
            service = self.get_ad_group_service()
            return (
                service,
                self.get_ad_group_operation_type(),
                service.ad_group_path(customer_id, ad_group_id),
                service.mutate_ad_groups,
            )
        elif level == Level.KEYWORDS.value:
            service = self.get_ad_group_criterion_service()
            return (
                service,
                self.get_ad_group_criterion_operation_type(),
                service.ad_group_criterion_path(customer_id, ad_group_id, keyword_id),
                service.mutate_ad_group_criteria,
            )
        else:
            raise ValueError("Invalid level provided")

    def update_structure(self, customer_id, edit_details, level, campaign_id=None, ad_group_id=None, keyword_id=None):
        service, operation, service_path, mutate_service = self.__get_services(
            customer_id, level, campaign_id, ad_group_id, keyword_id
        )

        structure = operation.update

        structure.resource_name = service_path

        self._update_fields(edit_details, structure, level, customer_id, campaign_id)

        self._client.copy_from(
            operation.update_mask,
            protobuf_helpers.field_mask(None, structure._pb),
        )

        response = mutate_service(customer_id=customer_id, operations=[operation])

        return {"message": f"successfully updated {str(response.results[0].resource_name)}"}

    def set_status_by_level(self, level, status_value):

        if level == Level.CAMPAIGN.value:
            if status_value == StructureStatusEnum.PAUSED.name:
                return self.get_campaign_status_enum_type().CampaignStatus.PAUSED
            else:
                return self.get_campaign_status_enum_type().CampaignStatus.ACTIVE

        elif level == Level.ADGROUP.value:
            if status_value == StructureStatusEnum.PAUSED.name:
                return self.get_ad_group_status_enum_type().AdGroupStatus.PAUSED
            else:
                return self.get_ad_group_status_enum_type().AdGroupStatus.ACTIVE

        elif level == Level.KEYWORD.value:
            if status_value == StructureStatusEnum.PAUSED.name:
                return self.get_ad_group_criterion_status_enum_type().AdGroupCriterionStatus.PAUSED
            else:
                return self.get_ad_group_criterion_status_enum_type().AdGroupCriterionStatus.PAUSED

    def _update_fields(self, edit_details, structure, level, customer_id=None, campaign_id=None):
        for detail in edit_details:
            if detail["field"] == EditFieldMapping.NAME.value and level != Level.KEYWORDS.value:
                structure.name = detail["value"]
            elif detail["field"] == EditFieldMapping.CPC.value and level != Level.CAMPAIGN.value:
                structure.cpc_bid_micros = detail["value"] * 10 ** 6
            elif detail["field"] == EditFieldMapping.STATUS.value:
                structure.status = self.set_status_by_level(level, detail["value"])
            elif detail["field"] == EditFieldMapping.BUDGET.value and level == Level.CAMPAIGN.value:
                self.update_campaign_budget(detail["value"], structure, customer_id, campaign_id)

    def get_campaign_budget_path(self, customer_id, campaign_id):
        where_field = (
            GoogleAttributeFieldsMetadata.campaign_id.resource_type.value
            + "."
            + GoogleAttributeFieldsMetadata.campaign_id.field_name
        )
        where_condition = [QueryBuilderGoogleFilters(where_field, AgGridGoogleOperator.EQUAL, campaign_id)]
        query = (
            GAQLBuilder()
            .select_([GoogleAttributeFieldsMetadata.campaign_budget])
            .from_(Level.CAMPAIGN)
            .where_(where_condition)
            .build_()
        )

        ga_service = self.get_ad_service()
        query_response = ga_service.search_stream(customer_id=customer_id, query=query)

        for batch in query_response:
            for row in batch.results:
                return row.campaign.campaign_budget

    def update_campaign_budget(self, budget_amount, structure, customer_id, campaign_id):
        campaign_budget_service, campaign_budget_operation, resource_path, mutate_service = self.__get_services(
            customer_id=customer_id, campaign_id=campaign_id
        )

        campaign_budget = campaign_budget_operation.update
        campaign_budget.resource_name = resource_path

        campaign_budget.amount_micros = budget_amount * 10 ** 6

        self._client.copy_from(
            campaign_budget_operation.update_mask,
            protobuf_helpers.field_mask(None, campaign_budget._pb),
        )

        campaign_budget_response = campaign_budget_service.mutate_campaign_budgets(
            customer_id=customer_id, operations=[campaign_budget_operation]
        )

        structure.campaign_budget = campaign_budget_response.results[0].resource_name
