from sqlalchemy import Column

from sqlalchemy.dialects.mssql import (
    BIGINT,
    DATETIME2,
    NVARCHAR,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AuditFields(Base):
    __abstract__ = True
    UpdatedAt = Column(DATETIME2(precision=7))
    UpdatedById = Column(BIGINT)
    UpdatedByFirstName = Column(NVARCHAR(length=128))
    UpdatedByLastName = Column(NVARCHAR(length=128))
    CreatedAt = Column(DATETIME2(precision=7))
    CreatedById = Column(BIGINT)
    CreatedByFirstName = Column(NVARCHAR(length=128))
    CreatedByLastName = Column(NVARCHAR(length=128))
