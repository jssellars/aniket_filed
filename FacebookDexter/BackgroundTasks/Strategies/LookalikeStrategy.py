import copy
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import AnyStr, ClassVar, Dict, List, MutableMapping

from facebook_business.adobjects.adaccount import AdAccount
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
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import (
    RecommendationEntryModel,
    ReportRecommendationDataModel,
)

logger = logging.getLogger(__name__)


@dataclass
class LookalikeStrategy(DexterLabsStrategyBase):
    ALGORITHM: ClassVar[str] = "Labs_Lookalike_Algorithm"
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

        adset_audiences = [adset["details"].get("targeting", {}).get("custom_audiences") for adset in adsets]

        audience_ids = [
            audience["id"] for audiences in adset_audiences if audiences is not None for audience in audiences
        ]

        custom_audience_mapper = GraphAPIDexterCustomAudienceMapping(target=GraphAPIDexterCustomAudienceDto)
        custom_audiences = [
            CustomAudience(audience_id).api_get(fields=["name", "rule"]) for audience_id in audience_ids
        ]
        custom_audiences = custom_audience_mapper.load(custom_audiences, many=True)

        if LookalikeStrategy.is_rule_exists(custom_audiences):
            pixel_id = LookalikeStrategy.get_pixel_id(account_id)

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
                apply_parameters={"pixel_id": pixel_id},
                is_labs=True,
            )

            dexter_recommendation.process_output(
                recommendations_repository, recommendation_entry_model=entry.get_extended_db_entry()
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
                logger.exception("No rule present in custom_audience")

        return True

    @staticmethod
    def get_pixel_id(ad_account_id):
        ad_account_id = "act_" + ad_account_id
        ad_account = AdAccount(ad_account_id)
        pixels = ad_account.get_ads_pixels()
        return pixels[0].get_id()
