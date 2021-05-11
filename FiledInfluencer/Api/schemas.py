from typing import Optional

from pydantic import BaseModel, AnyUrl


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
    CategoryName: Optional[str]

    class Config:
        orm_mode = True


class InfluencersCategoriesPydantic(BaseModel):
    Id: int
    Name: str

    class Config:
        orm_mode = True
