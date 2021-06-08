from dataclasses import dataclass


@dataclass
class GraphAPIDexterCustomAudienceDto:
    id: str = None
    name: str = None
    pixel_id: str = None
    rule: dict = None
