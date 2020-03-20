from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()


class BusinessOwnerModel(Base):
    """Table used to hold user ids and their associated FB tokens"""

    __tablename__ = "BusinessOwners"
    id = Column(Integer, primary_key=True, autoincrement=True)
    facebook_id = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    token = Column(String, nullable=False)
    page_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

