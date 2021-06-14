import json
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import ClassVar, Dict

from facebook_business.adobjects.customaudience import CustomAudience

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationStatusEnum
from Core.mongo_adapter import MongoRepositoryBase
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import create_facebook_filter, get_and_map_structures
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.BackgroundTasks.Strategies.DexterLabsStrategyBase import DexterLabsStrategyBase
from FacebookDexter.Infrastructure.DexterRules.DexterLabsTemplate import DexterLabsTemplate
from FacebookDexter.Infrastructure.GraphAPIDtos.GraphAPIDexterCustomAudienceDtos import GraphAPIDexterCustomAudienceDto
from FacebookDexter.Infrastructure.GraphAPIMappings.GraphAPIDexterCustomAudienceMapping import (
    GraphAPIDexterCustomAudienceMapping,
)
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import RecommendationEntryModel

logger = logging.getLogger(__name__)


@dataclass
class LookalikeStrategy(DexterLabsStrategyBase):
    ALGORITHM: ClassVar[str] = "labs_lookalike_strategy"
    dexter_output: Enum = DexterLabsTemplate.LOOKALIKE_AUDIENCE

    def generate_recommendation(
        self,
        level: LevelEnum,
        business_owner: str,
        account_id: str,
        campaign: Dict,
        recommendations_repository: MongoRepositoryBase,
    ) -> None:

        filtering = create_facebook_filter(
            FieldsMetadata.campaign_id.name.replace("_", "."),
            AgGridFacebookOperator.EQUAL,
            campaign["campaign_id"],
        )

        adsets = get_and_map_structures(f"act_{account_id}", level, filtering)

        # calculate most frequent country targeted from all adsets' geo targeting.
        # If no specific country found, ignore campaign.
        most_frequent_country = DexterLabsStrategyBase.get_most_frequent_country(adsets)
        if not most_frequent_country:
            logger.info("No specific country to target in this campaign, ignoring recommendation")
            return

        # get audiences from all adsets
        adset_audiences = [adset["details"].get("targeting", {}).get("custom_audiences") for adset in adsets]

        audience_ids = [
            audience["id"] for audiences in adset_audiences if audiences is not None for audience in audiences
        ]

        # custom audience mapper
        custom_audience_mapper = GraphAPIDexterCustomAudienceMapping(target=GraphAPIDexterCustomAudienceDto)

        # get all custom audiences for all adsets in campaigns
        custom_audiences = [
            CustomAudience(audience_id).api_get(fields=["name", "rule", "lookalike_spec"])
            for audience_id in audience_ids
        ]
        custom_audiences = custom_audience_mapper.load(custom_audiences, many=True)

        # get origin custom audience from lookalike audiences
        for custom_audience in list(custom_audiences):
            if custom_audience.lookalike_spec:
                origin_id = custom_audience.lookalike_spec.get("origin", {})[0].get("id")
                original_custom_audience = CustomAudience(origin_id).api_get(fields=["name", "rule"])
                custom_audiences.remove(custom_audience)
                custom_audiences.append(custom_audience_mapper.load(original_custom_audience, many=False))

        # check if Purchase rule exists in any custom audience
        if LookalikeStrategy.is_rule_exists(custom_audiences):
            pixel_id = self.get_pixel_id(account_id)
            best_adset_id, best_adset_name = DexterLabsStrategyBase.get_best_adset(
                campaign["campaign_id"], f"act_{account_id}"
            )

            structure_data, reports_data = DexterLabsStrategyBase.get_structure_and_reports_data(
                business_owner, account_id, campaign, LevelEnum.CAMPAIGN, pixel_id
            )

            dexter_recommendation = self.dexter_output.value

            entry = RecommendationEntryModel(
                template=self.dexter_output.name,
                status=RecommendationStatusEnum.ACTIVE.value,
                trigger_variance=0.0,
                created_at=datetime.now().isoformat(),
                time_interval=0,
                channel=ChannelEnum.FACEBOOK.value,
                priority=dexter_recommendation.priority.value,
                structure_data=structure_data,
                reports_data=reports_data,
                algorithm_type=self.ALGORITHM,
                apply_parameters={
                    "pixel_id": pixel_id,
                    "best_adset_id": best_adset_id,
                    "best_adset_name": best_adset_name,
                    "most_frequent_country": most_frequent_country,
                },
                is_labs=True,
            )

            dexter_recommendation.process_output(
                recommendations_repository, recommendation_entry_model=entry.get_extended_db_entry()
            )

        logger.info(
            f"Completed Dexter Labs {self.ALGORITHM} for Campaign: {campaign['campaign_id']} ad account: {account_id}, business owner: {business_owner}"
        )

    @staticmethod
    def is_rule_exists(custom_audiences, rule_value="Purchase"):
        for audience in custom_audiences:
            try:
                for rule in json.loads(audience.rule)["inclusions"]["rules"]:
                    for filter in rule["filter"]["filters"]:
                        if filter.get("value") is not None:
                            if filter.get("value") == rule_value:
                                return False
                        else:
                            for f in filter.get("filters"):
                                if f.get("value") is not None:
                                    if filter.get("value") == rule_value:
                                        return False
            except Exception as e:
                logger.info("Failed to parse audience")

        return True
