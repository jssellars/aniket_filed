import copy
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import AnyStr, List, MutableMapping

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.customaudience import CustomAudience

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DexterJournalEnums import RunStatusDexterEngineJournal
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.mongo_adapter import MongoRepositoryBase
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import create_facebook_filter, get_and_map_structures
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FacebookToTuringStatusMapping import EffectiveStatusEnum
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from Core.Web.FacebookGraphAPI.Tools import Tools
from FacebookDexter.BackgroundTasks.Strategies.DexterLabsStrategyBase import DexterLabsStrategyBase
from FacebookDexter.BackgroundTasks.Strategies.LookalikeStrategy import LookalikeStrategy
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyDataMongoRepository import StrategyDataMongoRepository
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import StrategyJournalMongoRepository
from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIFields import (
    GraphAPIPixelCustomAudienceFields,
    GraphAPIPixelFields,
)
from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIPixelCustomAudienceDto import GraphAPIPixelCustomAudienceDto
from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIPixelDto import GraphAPIPixelDto
from FacebookPixels.Infrastructure.GraphAPIMappings.GraphAPIMappingBase import GraphAPIPixelCustomAudienceMapping
from FacebookPixels.Infrastructure.GraphAPIMappings.GraphAPIPixelMapping import GraphAPIPixelMapping


class DexterLabsStrategiesEnum(Enum):
    LOOKALIKE_STRATEGY = LookalikeStrategy(
        levels=[LevelEnum.ADSET],
    )


@dataclass
class DexterLabsStrategyMaster:
    dexter_strategy: DexterLabsStrategyBase
    data_repository: StrategyDataMongoRepository
    recommendations_repository: MongoRepositoryBase
    journal_repository: StrategyJournalMongoRepository

    def analyze_data_for_business_owner(self, business_owner: str, account_ids: List):
        for account_id in account_ids:
            self.analyze_account(business_owner, account_id)

    def analyze_account(self, business_owner: str, account_id: str) -> None:
        self.journal_repository.update_journal_entry(
            business_owner,
            account_id,
            RunStatusDexterEngineJournal.IN_PROGRESS,
            ChannelEnum.FACEBOOK,
            self.dexter_strategy.ALGORITHM,
            start_time=datetime.now(),
        )

        has_errors = False

        for level in self.dexter_strategy.levels:
            filtering = create_facebook_filter(
                FieldsMetadata.effective_status.name,
                AgGridFacebookOperator.IN,
                [EffectiveStatusEnum.ACTIVE.value],
            )

            # TODO filter active status > 7 days
            # filtering = create_facebook_filter("date_preset", AgGridFacebookOperator.IN, ["last_7d"])

            structures = get_and_map_structures(f"act_{account_id}", level, filtering)
            valid_campaigns = [
                {"campaign_id": adset.get("campaign_id"), "campaign_name": adset.get("campaign_name")}
                for adset in structures
            ]
            valid_campaigns = list({v["campaign_id"]: v for v in valid_campaigns}.values())

            for campaign in valid_campaigns:
                self.dexter_strategy.generate_recommendation(
                    level,
                    business_owner,
                    account_id,
                    campaign,
                    self.recommendations_repository,
                )
