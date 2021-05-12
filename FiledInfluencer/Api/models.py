from dataclasses import dataclass
from typing import Optional, Dict, List, Union

from sqlalchemy import Column
from sqlalchemy.dialects.mssql import BIGINT, \
    DATETIME2, NVARCHAR
from sqlalchemy.ext.declarative import declarative_base


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
    name: str
    biography: str
    details: Dict[str, Union[str, Dict[str, int]]]
    engagement: Optional[str] = None
    filed_platform_id: Optional[int] = None
    filed_category_id: Optional[int] = None


@dataclass
class Platform:
    _id: int
    name: str
    handle: str


@dataclass
class InfluencerPost:
    post_content: str
    posted_at: str
    filed_platform_id: Optional[int] = None
    influencer_id: Optional[int] = None
    engagement: Optional[int] = None


Base = declarative_base()


class Influencers(Base):
    __tablename__ = 'Influencers'

    Id = Column(BIGINT, primary_key=True)
    UpdatedAt = Column(DATETIME2(precision=7))
    UpdatedById = Column(BIGINT)
    UpdatedByFirstName = Column(NVARCHAR(length=128))
    UpdatedByLastName = Column(NVARCHAR(length=128))
    CreatedAt = Column(DATETIME2(precision=7))
    CreatedById = Column(BIGINT)
    CreatedByFirstName = Column(NVARCHAR(length=128))
    CreatedByLastName = Column(NVARCHAR(length=128))
    Name = Column(NVARCHAR(length=256))

    # Following fields are set to MAX in db
    # docs don't provide info about setting length to MAX
    # https://docs.sqlalchemy.org/en/13/dialects/mssql.html?highlight=mssql#sqlalchemy.dialects.mssql.NVARCHAR

    Biography = Column(NVARCHAR())
    Engagement = Column(NVARCHAR())
    Details = Column(NVARCHAR())

    PlatformId = Column(BIGINT)
    InfluencersCategoriesId = Column(BIGINT)

    def __repr__(self):
        return f"<User(name={self.Name}')>"


class InfluencersCategories(Base):
    __tablename__ = 'InfluencersCategories'

    Id = Column(BIGINT, primary_key=True)
    Name = Column(NVARCHAR(length=256))

    def __repr__(self):
        return f"<User(name={self.Name})>"
