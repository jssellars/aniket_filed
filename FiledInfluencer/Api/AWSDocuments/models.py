from sqlalchemy import Column
from sqlalchemy.dialects.mssql import (
    BIGINT,
    NVARCHAR,
    INTEGER,
)

from FiledInfluencer.Api.Common.models import AuditFields


class Documents(AuditFields):
    __tablename__ = 'Documents'

    Id = Column(BIGINT, primary_key=True)
    Name = Column(NVARCHAR(length=128))
    Extension = Column(NVARCHAR(length=128))
    Location = Column(NVARCHAR(length=128))
    IsContract = Column(INTEGER)
    CampaignId = Column(BIGINT)

    def __repr__(self):
        return f"<Documents(name={self.Name}')>"
