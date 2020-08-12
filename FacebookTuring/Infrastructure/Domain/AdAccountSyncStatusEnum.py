from enum import Enum


class AdAccountSyncStatusEnum(Enum):
    COMPLETED = 1
    PENDING = 2
    IN_PROGRESS = 3
    COMPLETED_WITH_ERRORS = 4
