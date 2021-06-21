"""
Implementation of Hidden Interests Strategy.

"""
# Standard Imports.
from dataclasses import dataclass
from typing import ClassVar, Dict
from enum import Enum
from datetime import datetime
import logging

# Core Imports.
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.mongo_adapter import MongoRepositoryBase
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import create_facebook_filter, get_and_map_structures
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationStatusEnum
from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum

# for filtering
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator

# Local Imports.
from FacebookDexter.BackgroundTasks.Strategies.DexterLabsStrategyBase import DexterLabsStrategyBase
from FacebookDexter.Infrastructure.DexterRules.DexterLabsTemplate import DexterLabsTemplate

from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import (
    RecommendationEntryModel
)

# Init Logger.
logger = logging.getLogger(__name__)


@dataclass
class HiddenInterestsStrategy(DexterLabsStrategyBase):
    ALGORITHM: ClassVar[str] = "labs_hidden_interests_strategy"
    dexter_output: Enum = DexterLabsTemplate.HIDDEN_INTERESTS

    def generate_recommendation(
            self,
            level: LevelEnum,
            business_owner: str,
            account_id: str,
            campaign: Dict,
            recommendations_repository: MongoRepositoryBase) -> None:
        """
        Generates Hidden Interests Recommendations.

        Parameters
        ----------
        level: LevelEnum
            Ad Campaign Structure Level
        business_owner: str
            Facebook Business Owner ID
        account_id: str
            Ad Account ID
        campaign: dict
            Campaign
        recommendations_repository: MongoRepositoryBase
            env_dexter_recommendations Mongo Table

        """
        # Filter out Adsets for the particular Campaign.
        filtering = create_facebook_filter(
            field=FieldsMetadata.campaign_id.name.replace("_", "."),
            operator=AgGridFacebookOperator.EQUAL,
            value=campaign["campaign_id"]
        )

        adset_structures = get_and_map_structures(ad_account_id=f"act_{account_id}",
                                                  level=level,
                                                  filtering=filtering)

        # Check Adsets have Specific Interests Targeting.
        valid_adset_structures = self.check_interests_targeting(adset_structures=adset_structures)

        # If there are valid adsets trigger the recommendations.
        for valid_adset_structure in valid_adset_structures:
            structure_data, reports_data = DexterLabsStrategyBase.get_structure_and_reports_data(
                business_owner=business_owner,
                account_id=account_id,
                structure=valid_adset_structure,
                level=LevelEnum.ADSET
            )

            dexter_recommendation = self.dexter_output.value
            apply_parameters = {
                "adset_name": valid_adset_structure["adset_name"],
                "adset_id": valid_adset_structure["adset_id"]
            }

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
                apply_parameters=apply_parameters,
                is_labs=True,
            )

            dexter_recommendation.process_output(
                recommendations_repository, recommendation_entry_model=entry.get_extended_db_entry()
            )

            logger.info(
                f"Completed Dexter Labs {self.ALGORITHM} for Adset: {valid_adset_structure['adset_id'], valid_adset_structure['adset_name']} Ad account: {account_id}, business owner: {business_owner}"
            )

    @staticmethod
    def check_interests_targeting(adset_structures: dict):
        """
        Returns valid_adsets & valid_adset_structures for Adsets with Interests Targeting.

        Parameters
        ----------
        adset_structures: dict
            Adset Structure

        Returns
        -------
        valid_adset_structures: list[dict]
            Adset Structure with Interests Targeting

        """
        valid_adset_structures = []

        for adset_structure in adset_structures:
            targeting = adset_structure.get("details", {}).get("targeting", {})
            if "flexible_spec" in targeting:
                for specs in targeting.get("flexible_spec"):
                    if "interests" in specs:
                        valid_adset_structures.append(adset_structure)

        return valid_adset_structures
