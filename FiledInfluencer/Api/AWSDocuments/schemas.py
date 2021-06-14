from datetime import datetime

from pydantic import BaseModel


class DocumentsResponse(BaseModel):
    Id: int
    Location: str
    IsContract: int

    class Config:
        orm_mode = True
