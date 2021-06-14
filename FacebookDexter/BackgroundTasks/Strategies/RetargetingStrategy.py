import logging
from dataclasses import dataclass
from typing import ClassVar, Dict, List
from enum import Enum
from datetime import datetime

from Core.Dexter.Infrastructure.Domain import ChannelEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationStatusEnum
from Core.mongo_adapter import MongoRepositoryBase

from FacebookDexter.BackgroundTasks.Strategies.DexterLabsStrategyBase import DexterLabsStrategyBase
from FacebookDexter.Infrastructure.DexterRules.DexterLabsTemplate import DexterLabsTemplate
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import RecommendationEntryModel
from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from facebook_business.adobjects.campaign import Campaign

logger = logging.getLogger(__name__)


@dataclass
class RetargetingStrategy(DexterLabsStrategyBase):
    ALGORITHM: ClassVar[str] = "labs_retargeting_strategy"

    def generate_recommendation(
            self,
            level: LevelEnum,
            business_owner: str,
            account_id: str,
            campaign: Dict,
            recommendations_repository: MongoRepositoryBase,
    ) -> None:
        """
        Generate Recommendation for Retargeting Strategy
        param
        """
        pixel_id = self.get_pixel_id(account_id)
        if pixel_id is not None:
            insights = self.get_campaign_insights(campaign["campaign_id"], [GraphAPIInsightsFields.actions], {})
            if insights:
                audience_size = self.evaluate_metrics(insights[0][GraphAPIInsightsFields.actions])
                if audience_size > 100:
                    structure_data, reports_data = DexterLabsStrategyBase.get_structure_and_reports_data(
                        business_owner, account_id, campaign, LevelEnum.CAMPAIGN, pixel_id
                    )
                    dexter_recommendation = DexterLabsTemplate.NO_PURCHASE_30_DAYS_AUDIENCE.value
                    dexter_output: Enum = DexterLabsTemplate.NO_PURCHASE_30_DAYS_AUDIENCE
                    best_adset_id, best_adset_name = DexterLabsStrategyBase.get_best_adset(campaign["campaign_id"],
                                                                                           f"act_{account_id}")
                    entry = RecommendationEntryModel(
                        template=dexter_output.name,
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
                            "strategy": "C30",
                            "best_adset_id": best_adset_id,
                            "best_adset_name": best_adset_name,
                        },
                        is_labs=True,
                    )

                    dexter_recommendation.process_output(
                        recommendations_repository, recommendation_entry_model=entry.get_extended_db_entry()
                    )
                    logger.info(
                        f"Completed Dexter Labs {self.ALGORITHM} for campaign: {campaign['campaign_id']} ad account: {account_id}, business owner: {business_owner}"
                    )

    @staticmethod
    def evaluate_metrics(actions: List):
        """
        Retrieve the audience size for the people who initiated checkout but didn't purchase.
        params: List of all the action types under insights for a campaign
        returns: intege
        """
        fb_pixel_initiate_checkout = 0
        fb_pixel_purchase = 0
        for action in actions:
            if action[GraphAPIInsightsFields.action_type] == GraphAPIInsightsFields.website_checkouts_initiated:
                fb_pixel_initiate_checkout = action[GraphAPIInsightsFields.value]
            if action[GraphAPIInsightsFields.action_type] == GraphAPIInsightsFields.website_purchases:
                fb_pixel_purchase = action[GraphAPIInsightsFields.value]

        audience_size = int(fb_pixel_initiate_checkout) - int(fb_pixel_purchase)
        return audience_size

    @staticmethod
    def get_campaign_insights(campaign_id: str, fields: List, params: Dict):
        insights = Campaign(campaign_id).get_insights(fields=fields, params=params)
        insights = [insight.export_all_data() for insight in insights]
        return insights
