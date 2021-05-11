from typing import Optional

from pydantic import BaseModel, Json
from pydantic.schema import datetime


# https://pydantic-docs.helpmanual.io/usage/schema/#json-schema-types
class InfluencersPydantic(BaseModel):
    """
    Convert SQLAlchemy model to Pydantic Model

    FastAPI uses pydantic model
    And pydantic models are required for serialization of data
    """
    Id: int
    UpdatedAt: Optional[datetime]
    UpdatedById: Optional[int]
    UpdatedByFirstName: Optional[str]
    UpdatedByLastName: Optional[str]
    CreatedAt: Optional[datetime]
    CreatedById: int
    CreatedByFirstName: Optional[str]
    CreatedByLastName: Optional[str]
    Name: str
    Biography: str
    Engagement: str
    Details: Json
    PlatformId: int
    InfluencersCategoriesId: Optional[int]

    class Config:
        orm_mode = True


class InfluencersCategoriesPydantic(BaseModel):
    Id: int
    Name: str

    class Config:
        orm_mode = True
