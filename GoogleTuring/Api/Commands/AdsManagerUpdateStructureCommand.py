from dataclasses import dataclass


@dataclass
class AdsManagerUpdateStructureCommand:
    details: dict = None
    dataSourceName: str = None
