import concurrent.futures
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DexterJournalEnums import RunStatusDexterEngineJournal
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.mongo_adapter import MongoRepositoryBase
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import create_facebook_filter, get_and_map_structures
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FacebookToTuringStatusMapping import EffectiveStatusEnum
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.BackgroundTasks.Strategies.DexterLabsStrategyBase import DexterLabsStrategyBase

# Hidden Interests Local Imports.
from FacebookDexter.BackgroundTasks.Strategies.HiddenInterestsStrategy import HiddenInterestsStrategy
from FacebookDexter.BackgroundTasks.Strategies.LookalikeStrategy import LookalikeStrategy
from FacebookDexter.BackgroundTasks.Strategies.RetargetingStrategy import RetargetingStrategy
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyDataMongoRepository import StrategyDataMongoRepository
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import StrategyJournalMongoRepository

logger = logging.getLogger(__name__)


class DexterLabsStrategiesEnum(Enum):
    LOOKALIKE_STRATEGY = LookalikeStrategy(
        levels=[LevelEnum.ADSET],
    )

    HIDDEN_INTERESTS_STRATEGY = HiddenInterestsStrategy(
        levels=[LevelEnum.ADSET],
    )

    RETARGETING_STRATEGY = RetargetingStrategy(
        levels=[LevelEnum.CAMPAIGN],
    )


@dataclass
class DexterLabsStrategyMaster:
    dexter_strategy: DexterLabsStrategyBase
    data_repository: StrategyDataMongoRepository
    recommendations_repository: MongoRepositoryBase
    journal_repository: StrategyJournalMongoRepository
    account_id: str = None

    def analyze_data_for_business_owner(self, business_owner: str, account_ids: List):
        for account_id in account_ids:
            self.analyze_account(business_owner, account_id)

    def analyze_account(self, business_owner: str, account_id: str) -> None:
        # Start Journal Entry.
        self.journal_repository.update_journal_entry(
            business_owner,
            account_id,
            RunStatusDexterEngineJournal.IN_PROGRESS,
            ChannelEnum.FACEBOOK,
            self.dexter_strategy.ALGORITHM,
            start_time=datetime.now(),
        )

        has_errors = False

        # init account_id attribute.
        self.account_id = account_id

        for level in self.dexter_strategy.levels:

            # Grab Campaign ID & Names that are Valid indicating Active + Minimum 1 Adset Running for 7 days.
            valid_campaigns = self.get_valid_campaigns(level=level)

            # Analyze Each Valid Campaign.
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for campaign in valid_campaigns:
                    executor.submit(
                        self.dexter_strategy.generate_recommendation,
                        level,
                        business_owner,
                        account_id,
                        campaign,
                        self.recommendations_repository,
                    )

        # End Journal Entry.
        status = RunStatusDexterEngineJournal.FAILED if has_errors else RunStatusDexterEngineJournal.COMPLETED
        self.journal_repository.update_journal_entry(
            business_owner,
            account_id,
            status,
            ChannelEnum.FACEBOOK,
            self.dexter_strategy.ALGORITHM,
            end_time=datetime.now(),
        )

        logger.info(f"Completed Dexter Labs {self.dexter_strategy.ALGORITHM} for Ad Account: {account_id}, Business Owner: {business_owner}")

    def get_valid_campaigns(self, level: LevelEnum):
        """
        Returns Campaign ID & Names that are Valid = Active + Minimum 1 Adset Running for 7 days.

        Parameters
        ----------
        level: LevelEnum
            Structure Level

        Returns
        -------
        valid_campaigns: list[dict]
            Names & Ids of Valid Campaigns

        """
        # Grab all the Live Campaigns (With Effective Status as Active)
        live_campaigns = self.get_live_campaigns(level=level)

        valid_campaigns = []

        for live_campaign in live_campaigns:
            campaign_with_adset_active = self.is_active_seven_days(live_campaign=live_campaign,
                                                                   level=level)
            if campaign_with_adset_active:
                valid_campaigns.append(
                    {
                        "campaign_id": live_campaign["campaign_id"],
                        "campaign_name": live_campaign["campaign_name"]
                    }
                )

        # Cleaning the repeating entries.
        valid_campaigns = list(
            {valid_campaign["campaign_id"]: valid_campaign for valid_campaign in valid_campaigns}.values()
        )

        return valid_campaigns

    def get_live_campaigns(self, level: LevelEnum):
        """
        Returns Campaign ID & Names that are Live.

        Parameters
        ----------
        level: LevelEnum
            Structure Level

        Returns
        -------
        live_campaigns: list[dict]
            Names & Ids of Live Campaigns
        """
        # Check 1 - Obtain Live Campaigns Structures.
        live_campaigns_filter = create_facebook_filter(
            FieldsMetadata.effective_status.name,
            AgGridFacebookOperator.IN,
            [EffectiveStatusEnum.ACTIVE.value],
        )

        campaign_structures = get_and_map_structures(ad_account_id=f"act_{self.account_id}",
                                                     level=level,
                                                     filtering=live_campaigns_filter)
        live_campaigns = [
            {"campaign_id": structure.get("campaign_id"), "campaign_name": structure.get("campaign_name")}
            for structure in campaign_structures
        ]

        # Cleaning the repeating entries.
        live_campaigns = list(
            {active_campaign["campaign_id"]: active_campaign for active_campaign in live_campaigns}.values()
        )

        return live_campaigns

    def is_active_seven_days(self, live_campaign, level: LevelEnum):
        """
        Returns True if the Campaign has minimum of 1 live Adset running for 7 days, else False.

        Parameters
        ----------
        live_campaign: dict
            Live Campaign
        level: LevelEnum
            Structure Level.

        Returns
        -------
        Returns True if the Campaign has minimum of 1 live Adset running for 7 days, else False.

        """
        # Filter out Adsets for the particular Campaign.
        filtering = create_facebook_filter(
            field=FieldsMetadata.campaign_id.name.replace("_", "."),
            operator=AgGridFacebookOperator.EQUAL,
            value=live_campaign["campaign_id"]
        )

        adset_structures = get_and_map_structures(ad_account_id=f"act_{self.account_id}",
                                                  level=level,
                                                  filtering=filtering)

        # Minimum 1 Live Adset running for 7 days and have interest targeting check.
        for adset_structure in adset_structures:
            adset_details = adset_structure.get("details")

            if adset_details["status"] == "ACTIVE":
                # Grab only the Creation Date from the timestamp.
                adset_created_at = adset_details["created_time"][:10]
                adset_created_at = datetime.strptime(adset_created_at, "%Y-%m-%d")

                # Check if it's running for 7 days at least from now.
                days_adset_was_active = datetime.now() - adset_created_at
                days_adset_was_active = days_adset_was_active.days

                # At least 1 Adset is active for 7 days.
                if days_adset_was_active >= 7:
                    return True

        return False
