''' SQl Alchmemy model for filed product '''

from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mssql import BIGINT, DATETIME2, DECIMAL, NVARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Currencies(Base):
    __tablename__ = "Currencies"
    Id = Column(BIGINT, primary_key=True)
    Name = Column(NVARCHAR(length=128))
    Value = Column(NVARCHAR(length=256))


class States(Base):
    __tablename__ = "States"
    Id = Column(BIGINT, primary_key=True)
    Name = Column(NVARCHAR(length=128))
    Value = Column(NVARCHAR(length=256))


class CustomProperties(Base):
    __tablename__ = "CustomProperties"
    Id = Column(BIGINT, primary_key=True)
    FiledVariantId = Column(BIGINT, ForeignKey("FiledVariants.Id"))
    Properties = Column(NVARCHAR(length=512))


class FiledSetVariants(Base):
    __tablename__ = "FiledSetVariants"
    FiledVariantId = Column(BIGINT, ForeignKey("FiledVariants.Id"), primary_key=True)
    FiledSetId = Column(BIGINT, primary_key=True)


class FiledVariantConnections(Base):
    __tablename__ = "FiledVariantConnections"
    FiledVariantId = Column(BIGINT, ForeignKey("FiledVariants.Id"), primary_key=True)
    ExternalPlatformId = Column(BIGINT, ForeignKey("ExternalPlatforms.Id"), primary_key=True)
    IdInPlatform = Column(NVARCHAR(length=512))

class FiledProductConnections(Base):
    __tablename__ = "FiledProductConnections"
    
    FiledVariantId = Column(BIGINT, ForeignKey("FiledVariants.Id"), primary_key=True)
    ExternalPlatformId = Column(BIGINT, ForeignKey("ExternalPlatforms.Id"), primary_key=True)
    IdInPlatform = Column(NVARCHAR(length=512))

class FiledSetConnections(Base):
    __tablename__ = "FiledSetConnections"
    FiledSetId = Column(BIGINT, ForeignKey("FiledSets.Id"), primary_key=True)
    ExternalPlatformId = Column(BIGINT, ForeignKey("ExternalPlatforms.Id"), primary_key=True)
    IdInPlatform = Column(NVARCHAR(length=512))

class FiledSmartSetConnections(Base):
    __tablename__ = "FiledSmartSetConnections"
    FiledSmartSetId = Column(BIGINT, ForeignKey("FiledSmartSets.Id"), primary_key=True)
    ExternalPlatformId = Column(BIGINT, ForeignKey("ExternalPlatforms.Id"), primary_key=True)
    IdInPlatform = Column(NVARCHAR(length=512))

class FiledSets(Base):
    __tablename__ = "FiledSets"

    Id = Column(BIGINT, primary_key=True)
    UpdatedAt = Column(DATETIME2(precision=7))
    UpdatedById = Column(BIGINT)
    UpdatedByFirstName = Column(NVARCHAR(length=128))
    UpdatedByLastName = Column(NVARCHAR(length=128))
    CreatedAt = Column(DATETIME2(precision=7))
    CreatedById = Column(BIGINT)
    CreatedByFirstName = Column(NVARCHAR(length=128))
    CreatedByLastName = Column(NVARCHAR(length=128))
    Name = Column(NVARCHAR(length=256))

    FiledProductCatalogId = Column(BIGINT, ForeignKey("FiledProductCatalogs.Id"))
    Filter = Column(NVARCHAR(length=256))
    StateId = Column(BIGINT, ForeignKey("States.Id"))
    ImportedAt =  Column(DATETIME2(precision=7))


class FiledSmartSets(Base):
    __tablename__ = "FiledSmartSets"

    Id = Column(BIGINT, primary_key=True)
    UpdatedAt = Column(DATETIME2(precision=7))
    UpdatedById = Column(BIGINT)
    UpdatedByFirstName = Column(NVARCHAR(length=128))
    UpdatedByLastName = Column(NVARCHAR(length=128))
    CreatedAt = Column(DATETIME2(precision=7))
    CreatedById = Column(BIGINT)
    CreatedByFirstName = Column(NVARCHAR(length=128))
    CreatedByLastName = Column(NVARCHAR(length=128))
    Name = Column(NVARCHAR(length=256))

    FiledProductCatalogId = Column(BIGINT, ForeignKey("FiledProductCatalogs.Id"))
    Filter = Column(NVARCHAR(length=256))
    StateId = Column(BIGINT, ForeignKey("States.Id"))
    ImportedAt =  Column(DATETIME2(precision=7))

class FiledProducts(Base):
    __tablename__ = "FiledProducts"

    Id = Column(BIGINT, primary_key=True)
    UpdatedAt = Column(DATETIME2(precision=7))
    UpdatedById = Column(BIGINT)
    UpdatedByFirstName = Column(NVARCHAR(length=128))
    UpdatedByLastName = Column(NVARCHAR(length=128))
    CreatedAt = Column(DATETIME2(precision=7))
    CreatedById = Column(BIGINT)
    CreatedByFirstName = Column(NVARCHAR(length=128))
    CreatedByLastName = Column(NVARCHAR(length=128))
    Name = Column(NVARCHAR(length=256))

    FiledProductCatalogId = Column(BIGINT, ForeignKey("FiledProductCatalogs.Id"))
    GoogleProductCategoryId = Column(BIGINT)
    ProductType = Column(NVARCHAR(length=128))
    Sku = Column(NVARCHAR(length=128))
    Issues = Column(NVARCHAR(length=128))
    Vendor = Column(NVARCHAR(length=128))
    Tags = Column(NVARCHAR(length=128))
    StateId = Column(BIGINT, ForeignKey("States.Id"))
    Description = Column(NVARCHAR(length=128))
    ImageUrl = Column(NVARCHAR(length=128))
    ImportedAt = Column(DATETIME2(precision=7))

    FiledVariants = relationship("FiledVariants", backref="FiledProducts")
    FiledProductCatalogs = relationship("FiledProductCatalogs", backref="FiledProducts")

    def __repr__(self):
        return f"<FiledProduct(id={self.Id}, name={self.Name}')>"


class FiledVariants(Base):
    __tablename__ = "FiledVariants"

    Id = Column(BIGINT, primary_key=True)
    UpdatedAt = Column(DATETIME2(precision=7))
    UpdatedById = Column(BIGINT)
    UpdatedByFirstName = Column(NVARCHAR(length=128))
    UpdatedByLastName = Column(NVARCHAR(length=128))
    CreatedAt = Column(DATETIME2(precision=7))
    CreatedById = Column(BIGINT)
    CreatedByFirstName = Column(NVARCHAR(length=128))
    CreatedByLastName = Column(NVARCHAR(length=128))
    Name = Column(NVARCHAR(length=256))

    FiledProductId = Column(BIGINT, ForeignKey("FiledProducts.Id"))
    CurrencyId = Column(BIGINT, ForeignKey("Currencies.Id"))
    Sku = Column(NVARCHAR(length=128))
    Color = Column(NVARCHAR(length=128))
    Condition = Column(NVARCHAR(length=128))
    Size = Column(BIGINT)
    Material = Column(NVARCHAR(length=128))
    Barcode = Column(NVARCHAR(length=128))
    InventoryQuantity = Column(BIGINT)
    Price = Column(DECIMAL)
    CompareAtPrice = Column(DECIMAL)
    Url = Column(NVARCHAR(length=128))
    ImageUrl = Column(NVARCHAR(length=128))
    ImportedAt = Column(DATETIME2(precision=7))
    CustomImages = Column(NVARCHAR(length=128))
    Availability = Column(BIGINT)
    Issues = Column(NVARCHAR(length=128))
    Tags = Column(NVARCHAR(length=128))
    StateId = Column(BIGINT, ForeignKey("States.Id"))
    ShortDescription = Column(NVARCHAR(length=128))
    FiledProductCatalogId = Column(BIGINT, ForeignKey("FiledProductCatalogs.Id"))

    FiledVariantConnection = relationship(
        "FiledVariantConnections", backref="FiledVariants"
    )
    FiledSetVariants = relationship("FiledSetVariants", backref="FiledVariants")
    CustomProperties = relationship("CustomProperties", backref="FiledVariants")
    FiledProductCatalogs = relationship("FiledProductCatalogs", backref="FiledVariants")

    def __repr__(self):
        return f"<FiledVariants(id={self.Id}, name={self.Name}')>"


class FiledProductCatalogs(Base):
    __tablename__ = "FiledProductCatalogs"

    Id = Column(BIGINT, primary_key=True)
    UpdatedAt = Column(DATETIME2(precision=7))
    UpdatedById = Column(BIGINT)
    UpdatedByFirstName = Column(NVARCHAR(length=128))
    UpdatedByLastName = Column(NVARCHAR(length=128))
    CreatedAt = Column(DATETIME2(precision=7))
    CreatedById = Column(BIGINT)
    CreatedByFirstName = Column(NVARCHAR(length=128))
    CreatedByLastName = Column(NVARCHAR(length=128))
    Name = Column(NVARCHAR(length=256))
    FiledBusinessOwnerId =Column(BIGINT, ForeignKey("FiledBusinessOwners.FiledBusinessOwnerId"))
    StateId = Column(BIGINT, ForeignKey("States.Id"))

    def __repr__(self):
        return f"<FiledProductCatalog(id={self.Id}, name={self.Name}')>"

class BusinessOwnerStates(Base):
    __tablename__ = "BusinessOwnerStates"

    Id = Column(BIGINT, primary_key=True)
    Name = Column(NVARCHAR(length=256))
    Value = Column(NVARCHAR(length=256))

class FiledBusinessOwners(Base):
    __tablename__ = "FiledBusinessOwners"

    FiledBusinessOwnerId = Column(BIGINT, primary_key=True)
    Name = Column(NVARCHAR(length=256))
    BusinessOwnerStateId = Column(BIGINT, ForeignKey("BusinessOwnerStates.Id"))

class FiledProductCatalogPermissions(Base):
    __tablename__ = "FiledProductCatalogPermissions"

    FiledProductCatalogId = Column(BIGINT, ForeignKey("FiledProductCatalogs.FiledBusinessOwnerId"), primary_key=True)
    FiledUserId = Column(BIGINT, primary_key=True)
    FiledBusinessOwnerId = Column(BIGINT, ForeignKey("FiledBusinessOwners.FiledBusinessOwnerId"))

class Platforms(Base):
    __tablename__ = "Platforms"

    Id = Column(BIGINT, primary_key=True)
    Name = Column(NVARCHAR(length=256))
    Value = Column(NVARCHAR(length=256))

class ExternalPlatforms(Base):
    __tablename__ = "ExternalPlatforms"

    Id = Column(BIGINT, primary_key=True)
    UpdatedAt = Column(DATETIME2(precision=7))
    UpdatedById = Column(BIGINT)
    UpdatedByFirstName = Column(NVARCHAR(length=128))
    UpdatedByLastName = Column(NVARCHAR(length=128))
    CreatedAt = Column(DATETIME2(precision=7))
    CreatedById = Column(BIGINT)
    CreatedByFirstName = Column(NVARCHAR(length=128))
    CreatedByLastName = Column(NVARCHAR(length=128))
    Name = Column(NVARCHAR(length=256))

    FiledBusinessOwnerId = Column(BIGINT, ForeignKey("FiledBusinessOwners.FiledBusinessOwnerId"))
    PlatformId = Column(BIGINT, ForeignKey("Platforms.Id"))
    MappingPreferences = Column(NVARCHAR(length=1024))
    Details = Column(NVARCHAR(length=1024))