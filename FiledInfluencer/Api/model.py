from dataclasses import dataclass
from typing import Optional, Dict, List, Union


# TODO: convert all to pydantic BaseModel
@dataclass
class InfluencerCategory:
    _id: int
    name: str


@dataclass
class CategoryHashtag:
    category_id: int
    hashtag: List[str]


@dataclass
class FiledInfluencer:
    _id: int
    filed_platform_id: Optional[int]
    filed_category_id: Optional[int]
    name: str
    biography: str
    details: Dict[str, Union[str, Dict[str, int]]]
    engagement: Optional[str] = None


@dataclass
class Platform:
    _id: int
    name: str
    handle: str


@dataclass
class InfluencerPost:
    filed_platform_id: Optional[int]
    influencer_id: Optional[int]
    post_content: str
    posted_at: str
    engagement: Optional[int] = None
