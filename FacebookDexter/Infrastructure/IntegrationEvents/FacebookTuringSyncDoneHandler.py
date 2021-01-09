import logging
import json
from dataclasses import dataclass

from Core.Dexter.Infrastructure.Domain.DexterJournalEnums import DexterEngineRunJournalEnum
from Core.Dexter.PersistanceLayer.DexterRecommendationsMongoRepository import DexterRecommendationsMongoRepository
from Core.mongo_adapter import MongoOperator
from FacebookDexter.BackgroundTasks.Strategies.EmailNotificationsSystem import send_email

from FacebookDexter.BackgroundTasks.Strategies.StrategyMaster import DexterStrategyMaster, DexterStrategiesEnum
from FacebookDexter.BackgroundTasks.startup import config
from FacebookDexter.Infrastructure.IntegrationEvents.FacebookTuringDataSyncCompletedEvent import (
    FacebookTuringDataSyncCompletedEvent,
)
from FacebookDexter.Infrastructure.IntegrationEvents.FacebookTuringDataSyncCompletedEventMapping import (
    FacebookTuringDataSyncCompletedEventMapping,
)
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyDataMongoRepository import StrategyDataMongoRepository
from FacebookDexter.Infrastructure.PersistanceLayer.StrategyJournalMongoRepository import StrategyJournalMongoRepository


logger = logging.getLogger(__name__)


@dataclass
class FacebookTuringSyncDoneHandler:
    recommendations_repository: DexterRecommendationsMongoRepository = None
    journal_repository: StrategyJournalMongoRepository = None

    def handle(self, body: str):
        body = json.loads(body)

        mapper = FacebookTuringDataSyncCompletedEventMapping(target=FacebookTuringDataSyncCompletedEvent)
        business_owners = mapper.load(body.get("business_owners", []), many=True)

        for business_owner in business_owners:

            account_ids = [f"act_{account_id}" for account_id in business_owner.ad_account_ids]
            query = {
                MongoOperator.AND.value: [
                    {"account_id": {MongoOperator.IN.value: account_ids}},
                    {DexterEngineRunJournalEnum.BUSINESS_OWNER_ID.value: {MongoOperator.EQUALS.value: business_owner.business_owner_facebook_id}},
                ]
            }

            self.recommendations_repository.delete_many(query)

            for strategy in DexterStrategiesEnum:
                dexter_strategy_master = DexterStrategyMaster(
                    strategy.value,
                    StrategyDataMongoRepository(
                        config=config.mongo,
                        database_name=config.mongo.insights_database,
                    ),
                    self.recommendations_repository,
                    self.journal_repository,
                )

                dexter_strategy_master.analyze_data_for_business_owner(
                    business_owner.business_owner_facebook_id,
                    business_owner.ad_account_ids,
                )

            response = send_email(self.recommendations_repository, account_ids)
            if response.status_code != 200:
                logger.error(
                    "Failed to send Dexter recommendations emails.",
                    extra=dict(business_owner=business_owner),
                )
