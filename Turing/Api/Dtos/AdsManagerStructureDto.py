from dataclasses import dataclass


@dataclass
class AdsManagerStructureDto:
    facebook_id: str = None
    name: str = None
    facebook_details: dict = None
    action_details: dict = None