from pydantic import BaseModel, AnyUrl
from typing import Optional


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
    Email: Optional[str]

    class Config:
        orm_mode = True
