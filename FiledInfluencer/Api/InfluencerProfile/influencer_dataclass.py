from dataclasses import dataclass

from typing import Optional


@dataclass
class Followers:
    followers_min_count: int
    followers_max_count: int


@dataclass
class EngagementPerPost:
    engagements_per_post_min_count: int
    engagements_per_post_max_count: int


@dataclass
class EngagementRate:
    engagement_rate_min_count: int
    engagement_rate_max_count: int


@dataclass
class InfluencerProfile:
    page_size: int
    last_influencer_id: int
    name: str
    get_total_count: bool
    account_type: int
    is_verified: str
    followers: Optional[Followers]
    engagement_per_post: Optional[EngagementPerPost]
    engagement_rate: Optional[EngagementRate]
