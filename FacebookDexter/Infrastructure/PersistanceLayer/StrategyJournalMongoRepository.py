from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, Dict, List

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DexterJournalEnums import (
    DexterEngineRunJournalEnum,
    RunStatusDexterEngineJournal,
)
from pymongo.errors import AutoReconnect
from retry import retry

from Core.mongo_adapter import MongoOperator, MongoRepositoryBase


class StrategyJournalMongoRepository(MongoRepositoryBase):
    __RETRY_LIMIT = 3

    @retry(AutoReconnect, tries=__RETRY_LIMIT, delay=1)
    def update_journal_entry(
            self,
            business_owner: str,
            account_id: str,
            run_status: RunStatusDexterEngineJournal,
            channel: ChannelEnum,
            algorithm: str,
            start_time: datetime = None,
            end_time: datetime = None,
    ):
        query_filter = {
            MongoOperator.AND.value: [
                {DexterEngineRunJournalEnum.AD_ACCOUNT_ID.value: {MongoOperator.EQUALS.value: account_id}},
                {DexterEngineRunJournalEnum.BUSINESS_OWNER_ID.value: {MongoOperator.EQUALS.value: business_owner}},
            ]
        }

        query = {
            MongoOperator.SET.value: {
                DexterEngineRunJournalEnum.BUSINESS_OWNER_ID.value: business_owner,
                DexterEngineRunJournalEnum.AD_ACCOUNT_ID.value: account_id,
                DexterEngineRunJournalEnum.RUN_STATUS.value: run_status.value,
                DexterEngineRunJournalEnum.CHANNEL.value: channel.value,
                DexterEngineRunJournalEnum.ALGORITHM_TYPE.value: algorithm,
                DexterEngineRunJournalEnum.END_TIMESTAMP.value: None,
            }
        }

        if start_time:
            query[MongoOperator.SET.value][DexterEngineRunJournalEnum.START_TIMESTAMP.value] = start_time
        if end_time:
            query[MongoOperator.SET.value][DexterEngineRunJournalEnum.END_TIMESTAMP.value] = end_time

        self.update_one(query_filter, query, True)


@dataclass
class StructureRecommendationModel:
    business_owner_id: str
    account_id: str
    structure_id: str
    structure_name: str
    campaign_id: str
    campaign_name: str
    level: str


@dataclass
class ReportRecommendationDataModel:
    metrics: List[Dict]
    breakdown: Dict


@dataclass
class RecommendationEntryModel:
    template: str
    status: str
    trigger_variance: float
    created_at: datetime
    time_interval: int
    channel: str
    priority: int
    structure_data: StructureRecommendationModel
    reports_data: ReportRecommendationDataModel
    algorithm_type: Optional[str] = None
    underperforming_breakdowns: Optional[List[str]] = None
    hidden_interests: Optional[str] = None
    debug_msg: Optional[str] = None
    apply_parameters: Optional[Dict] = None

    def get_extended_db_entry(self):
        recommendation = asdict(self)
        recommendation.update(recommendation.pop("structure_data"))
        recommendation.update(recommendation.pop("reports_data"))
        return recommendation
