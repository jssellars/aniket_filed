from dataclasses import dataclass


@dataclass
class GraphAPIPixelDAChecksDto:
    action_uri: str = None
    description: str = None
    key: str = None
    result: str = None
    title: str = None
    user_message: str = None
