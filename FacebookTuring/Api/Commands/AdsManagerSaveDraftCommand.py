from dataclasses import dataclass


@dataclass
class AdsManagerSaveDraftCommand:
    details: dict = None
