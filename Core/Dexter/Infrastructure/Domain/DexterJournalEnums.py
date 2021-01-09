from enum import Enum


class RunStatusDexterEngineJournal(Enum):
    IN_PROGRESS = 1
    COMPLETED = 2
    PENDING = 3
    FAILED = 4


class DexterEngineRunJournalEnum(Enum):
    BUSINESS_OWNER_ID = "business_owner_id"
    AD_ACCOUNT_ID = "ad_account_id"
    ALGORITHM_TYPE = "algorithm_type"
    RUN_STATUS = "run_status"
    LEVEL = "level"
    START_TIMESTAMP = "start_timestamp"
    END_TIMESTAMP = "end_timestamp"
    CHANNEL = "channel"
