from datetime import datetime, timezone

import bson
from pydantic import BaseModel
from pydantic.class_validators import validator
from pydantic.fields import Field
from typing import Optional


class ObjectId(bson.ObjectId):
    """
    extract _id from pymongo

    https://github.com/tiangolo/fastapi/issues/68#issuecomment-844911949
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        try:
            return cls(value)
        except bson.errors.InvalidId:
            raise ValueError("Not a valid ObjectId")


class MessageModel(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    sender: str
    recipient: str
    message: str
    timestamp: Optional[datetime]

    class Config:
        json_encoders = {ObjectId: str}

    @validator("timestamp", pre=True, always=True)
    def set_timestamp(cls, _):
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()[:-6] + "Z"
