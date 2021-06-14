from datetime import datetime

from pydantic import BaseModel
from typing import Optional


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
