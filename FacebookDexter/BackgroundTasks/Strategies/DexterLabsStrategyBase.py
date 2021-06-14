import typing
from dataclasses import dataclass
from typing import ClassVar, Dict, List, Tuple

from facebook_business.adobjects.adaccount import AdAccount

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum, LevelIdKeyEnum
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import add_results_to_response, create_facebook_filter
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.GraphAPIInsightsMapper import GraphAPIInsightsMapper
from Core.Web.FacebookGraphAPI.Models.Field import Field
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import (
    ReportRecommendationDataModel,
    StructureRecommendationModel,
)


@dataclass
class DexterLabsStrategyBase:
    ALGORITHM: ClassVar[str] = "Base_Algorithm"
    levels: List[LevelEnum]

    def generate_recommendation(self, *args):
        raise NotImplementedError

    def get_pixel_audiences(self, account_id):
        pass

    def get_audience_by_rule(self, pixel_audiences):
        pass

    CPR_FIELDS = [
        GraphAPIInsightsFields.cost_per_unique_action_type,
        GraphAPIInsightsFields.spend,
        GraphAPIInsightsFields.cpp,
        GraphAPIInsightsFields.actions,
        GraphAPIInsightsFields.cost_per_thruplay,
        GraphAPIInsightsFields.adset_name,
        GraphAPIInsightsFields.adset_id,
        GraphAPIInsightsFields.cpm,
        GraphAPIInsightsFields.date_start,
        GraphAPIInsightsFields.objective,
        GraphAPIInsightsFields.cost_per_action_type,
    ]

    @staticmethod
    def get_structure_and_reports_data(
        business_owner: str, account_id: str, structure: Dict, level: LevelEnum, pixel_id: str = None
    ) -> Tuple[StructureRecommendationModel, ReportRecommendationDataModel]:
        structure_key = LevelIdKeyEnum[level.value.upper()].value

        structure_data = StructureRecommendationModel(
            business_owner,
            f"act_{account_id}",
            structure[structure_key],
            structure[f"{level.value}_name"],
            structure[FieldsMetadata.campaign_id.name],
            structure[FieldsMetadata.campaign_name.name],
            level.value,
            pixel_id,
        )

        reports_data = ReportRecommendationDataModel(
            [{"display_name": None, "name": None}],
            {},
        )

        return structure_data, reports_data

    @staticmethod
    def get_most_frequent_country(adsets):
        country_list = []
        for adset in adsets:
            adset_countries = adset.get("details", {}).get("targeting", {}).get("geo_locations", {}).get("countries")
            country_list.extend(adset_countries) if adset_countries is not None else country_list.extend([])

        if len(country_list) == 0:
            return None
        else:
            return max(set(country_list), key=country_list.count)

    @staticmethod
    def map_(name: typing.AnyStr) -> Field:
        return getattr(FieldsMetadata, name, None)

    @staticmethod
    def create_field_and_param(campaign_id):
        filtering = create_facebook_filter(
            FieldsMetadata.campaign_id.name.replace("_", "."),
            AgGridFacebookOperator.EQUAL,
            campaign_id,
        )

        params = {
            "level": LevelEnum.ADSET.value,
            "breakdowns": [],
            "time_increment": "all_days",
            "date_preset": "last_90d",
            "filtering": [filtering],
        }

        requested_fields = []
        fields_ = ["cost_per_result", "adset_id", "adset_name"]

        for field in fields_:
            requested_fields.append(DexterLabsStrategyBase.map_(field))

        return params, requested_fields

    @staticmethod
    def get_insights(account_id, parameters, requested_fields, level):
        ad_account = AdAccount(account_id)
        insights = ad_account.get_insights(fields=DexterLabsStrategyBase.CPR_FIELDS, params=parameters)

        if not insights:
            return []

        # Sanity Check on Requested Fields.
        results_requested = any(
            [
                FieldsMetadata.results.name == x.name or FieldsMetadata.cost_per_result.name == x.name
                for x in requested_fields
            ]
        )

        insights_data = []
        for insight in insights:
            insights_data.append(insight.export_all_data())
            insights.params = parameters

        if results_requested:
            add_results_to_response(level, insights_data, account_id)

        if insights_data:
            insights_response = GraphAPIInsightsMapper().map(requested_fields=requested_fields, response=insights_data)
        else:
            return []

        insights_response = sorted(
            insights_response, key=lambda k: (k["cost_per_result"] is None, k["cost_per_result"])
        )
        return insights_response

    @staticmethod
    def get_best_adset(campaign_id, account_id):
        parameters, requested_fields = DexterLabsStrategyBase.create_field_and_param(campaign_id)
        insights_response = DexterLabsStrategyBase.get_insights(account_id, parameters, requested_fields, "adset")
        return insights_response[0]["adset_id"], insights_response[0]["adset_name"]

    @staticmethod
    def get_pixel_id(ad_account_id):
        ad_account_id = "act_" + ad_account_id
        ad_account = AdAccount(ad_account_id)
        pixels = ad_account.get_ads_pixels()
        return pixels[0].get_id()
