from datetime import datetime

from pydantic import BaseModel, AnyUrl
from typing import Optional


# https://pydantic-docs.helpmanual.io/usage/schema/#json-schema-types
class InfluencersResponse(BaseModel):
    """
    Convert SQLAlchemy model to Pydantic Model

    FastAPI uses pydantic model
    And pydantic models are required for serialization of data
    """
    Id: int
    Name: str
    Biography: str
    Engagement: str
    ProfilePicture: AnyUrl
    CategoryName: Optional[str] = None
    AccountType: str
    IsVerified: str
    Followers: int

    class Config:
        orm_mode = True


class InfluencersCategoriesPydantic(BaseModel):
    Id: int
    Name: str

    class Config:
        orm_mode = True


class EmailTemplateResponse(BaseModel):
    """
    Convert SQLAlchemy model to Pydantic Model

    FastAPI uses pydantic model
    And pydantic models are required for serialization of data
    """
    Id: Optional[int]
    Name: str
    Subject: str
    Body: str
    CampaignId: int
    CreatedById: int
    CreatedAt: datetime

    class Config:
        orm_mode = True
