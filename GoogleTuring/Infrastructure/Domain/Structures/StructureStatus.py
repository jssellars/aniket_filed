from enum import Enum


class StructureStatus(Enum):
    PAUSED = 0
    ENABLED = 1
    REMOVED = 2
    DEPRECATED = 3


GOOGLE_STATUS_MAPPING = {
    'PAUSED': StructureStatus.PAUSED.value,
    'ENABLED': StructureStatus.ENABLED.value,
    'REMOVED': StructureStatus.REMOVED.value
}
