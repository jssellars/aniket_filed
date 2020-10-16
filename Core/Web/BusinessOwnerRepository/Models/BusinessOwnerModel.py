from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BusinessOwnerModel(Base):
    """Table used to hold user ids and their associated FB tokens"""

    __tablename__ = "BusinessOwnerTokens"
    FacebookId = Column(String, primary_key=True)
    Name = Column(String, nullable=True)
    Email = Column(String, nullable=True)
    Token = Column(String, nullable=False)
    PageId = Column(String, primary_key=True, nullable=False)
    CreatedAt = Column(DateTime, nullable=False)
    UpdatedAt = Column(DateTime)
