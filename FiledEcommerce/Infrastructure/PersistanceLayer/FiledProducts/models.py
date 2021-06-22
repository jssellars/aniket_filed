''' SQl Alchmemy model for filed product '''
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mssql import BIGINT, DATETIME2, DECIMAL, NVARCHAR, BIT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Currencies(Base):
    __tablename__ = "Currencies"
    Id = Column(BIGINT, primary_key=True)
    Name = Column(NVARCHAR())
    Value = Column(NVARCHAR())


class States(Base):
    __tablename__ = "States"
    Id = Column(BIGINT, primary_key=True)
    Name = Column(NVARCHAR())


class CustomProperties(Base):
    __tablename__ = "CustomProperties"
    Id = Column(BIGINT, primary_key=True)
    FiledVariantId = Column(BIGINT, ForeignKey("FiledVariants.Id"))
    Properties = Column(NVARCHAR())



class FiledSetVariants(Base):
    __tablename__ = "FiledSetVariants"
    FiledVariantId = Column(BIGINT, ForeignKey("FiledVariants.Id"), primary_key=True)
    FiledSetId = Column(BIGINT, primary_key=True)


class FiledVariantConnections(Base):
    __tablename__ = "FiledVariantConnections"
    FiledVariantId = Column(BIGINT, ForeignKey("FiledVariants.Id"), primary_key=True)
    ExternalPlatformId = Column(BIGINT, ForeignKey("ExternalPlatforms.Id"), primary_key=True)
    IdInPlatform = Column(NVARCHAR())

class FiledProductConnections(Base):
    __tablename__ = "FiledProductConnections"
    
    FiledVariantId = Column(BIGINT, ForeignKey("FiledVariants.Id"), primary_key=True)
    ExternalPlatformId = Column(BIGINT, ForeignKey("ExternalPlatforms.Id"), primary_key=True)
    IdInPlatform = Column(NVARCHAR())

class FiledSetConnections(Base):
    __tablename__ = "FiledSetConnections"
    FiledSetId = Column(BIGINT, ForeignKey("FiledSets.Id"), primary_key=True)
    ExternalPlatformId = Column(BIGINT, ForeignKey("ExternalPlatforms.Id"), primary_key=True)
    IdInPlatform = Column(NVARCHAR())

class FiledSmartSetConnections(Base):
    __tablename__ = "FiledSmartSetConnections"
    FiledSmartSetId = Column(BIGINT, ForeignKey("FiledSmartSets.Id"), primary_key=True)
    ExternalPlatformId = Column(BIGINT, ForeignKey("ExternalPlatforms.Id"), primary_key=True)
    IdInPlatform = Column(NVARCHAR())

class FiledSets(Base):
    __tablename__ = "FiledSets"

    Id = Column(BIGINT, primary_key=True)
    UpdatedAt = Column(DATETIME2(precision=7))
    UpdatedById = Column(BIGINT)
    UpdatedByFirstName = Column(NVARCHAR())
    UpdatedByLastName = Column(NVARCHAR())
    CreatedAt = Column(DATETIME2(precision=7))
    CreatedById = Column(BIGINT)
    CreatedByFirstName = Column(NVARCHAR())
    CreatedByLastName = Column(NVARCHAR())
    Name = Column(NVARCHAR())

    FiledProductCatalogId = Column(BIGINT, ForeignKey("FiledProductCatalogs.Id"))
    StateId = Column(BIGINT, ForeignKey("States.Id"))
    ImportedAt =  Column(DATETIME2(precision=7))

    FiledProductCatalogs = relationship("FiledProductCatalogs", backref="FiledSets")

class FiledSmartSets(Base):
    __tablename__ = "FiledSmartSets"

    Id = Column(BIGINT, primary_key=True)
    UpdatedAt = Column(DATETIME2(precision=7))
    UpdatedById = Column(BIGINT)
    UpdatedByFirstName = Column(NVARCHAR())
    UpdatedByLastName = Column(NVARCHAR())
    CreatedAt = Column(DATETIME2(precision=7))
    CreatedById = Column(BIGINT)
    CreatedByFirstName = Column(NVARCHAR())
    CreatedByLastName = Column(NVARCHAR())
    Name = Column(NVARCHAR())

    FiledProductCatalogId = Column(BIGINT, ForeignKey("FiledProductCatalogs.Id"))
    StateId = Column(BIGINT, ForeignKey("States.Id"))
    ImportedAt =  Column(DATETIME2(precision=7))

    FiledProductCatalogs = relationship("FiledProductCatalogs", backref="FiledSmartSets")

class FiledProducts(Base):
    __tablename__ = "FiledProducts"

    Id = Column(BIGINT, primary_key=True)
    UpdatedAt = Column(DATETIME2(precision=7))
    UpdatedById = Column(BIGINT)
    UpdatedByFirstName = Column(NVARCHAR())
    UpdatedByLastName = Column(NVARCHAR())
    CreatedAt = Column(DATETIME2(precision=7))
    CreatedById = Column(BIGINT)
    CreatedByFirstName = Column(NVARCHAR())
    CreatedByLastName = Column(NVARCHAR())
    Name = Column(NVARCHAR())

    FiledProductCatalogId = Column(BIGINT, ForeignKey("FiledProductCatalogs.Id"))
    GoogleProductCategoryId = Column(BIGINT)
    ProductType = Column(NVARCHAR())
    Sku = Column(NVARCHAR())
    Issues = Column(NVARCHAR())
    Tags = Column(NVARCHAR())
    StateId = Column(BIGINT, ForeignKey("States.Id"))
    Description = Column(NVARCHAR())
    ImageUrl = Column(NVARCHAR())
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
    UpdatedByFirstName = Column(NVARCHAR())
    UpdatedByLastName = Column(NVARCHAR())
    CreatedAt = Column(DATETIME2(precision=7))
    CreatedById = Column(BIGINT)
    CreatedByFirstName = Column(NVARCHAR())
    CreatedByLastName = Column(NVARCHAR())
    Name = Column(NVARCHAR())

    FiledProductId = Column(BIGINT, ForeignKey("FiledProducts.Id"))
    CurrencyId = Column(BIGINT, ForeignKey("Currencies.Id"))
    Sku = Column(NVARCHAR())
    Color = Column(NVARCHAR())
    Condition = Column(NVARCHAR())
    Size = Column(NVARCHAR())
    Material = Column(NVARCHAR())
    Barcode = Column(NVARCHAR())
    InventoryQuantity = Column(BIGINT)
    Price = Column(DECIMAL)
    CompareAtPrice = Column(DECIMAL)
    Url = Column(NVARCHAR())
    ImageUrl = Column(NVARCHAR())
    ImportedAt = Column(DATETIME2(precision=7))
    CustomImages = Column(NVARCHAR())
    Availability = Column(BIGINT)
    Issues = Column(NVARCHAR())
    Tags = Column(NVARCHAR())
    StateId = Column(BIGINT, ForeignKey("States.Id"))
    ShortDescription = Column(NVARCHAR())
    FiledProductCatalogId = Column(BIGINT, ForeignKey("FiledProductCatalogs.Id"))

    FiledVariantConnection = relationship(
        "FiledVariantConnections", backref="FiledVariants"
    )
    FiledSetVariants = relationship("FiledSetVariants", backref="FiledVariants")
    Currencies = relationship("Currencies", backref="FiledVariants")
    CustomProperties = relationship("CustomProperties", backref="FiledVariants")
    FiledProductCatalogs = relationship("FiledProductCatalogs", backref="FiledVariants")

    def __repr__(self):
        return f"<FiledVariants(id={self.Id}, name={self.Name}')>"


class FiledProductCatalogs(Base):
    __tablename__ = "FiledProductCatalogs"

    Id = Column(BIGINT, primary_key=True)
    UpdatedAt = Column(DATETIME2(precision=7))
    UpdatedById = Column(BIGINT)
    UpdatedByFirstName = Column(NVARCHAR())
    UpdatedByLastName = Column(NVARCHAR())
    CreatedAt = Column(DATETIME2(precision=7))
    CreatedById = Column(BIGINT)
    CreatedByFirstName = Column(NVARCHAR())
    CreatedByLastName = Column(NVARCHAR())
    Name = Column(NVARCHAR())
    FiledBusinessOwnerId =Column(BIGINT, ForeignKey("FiledBusinessOwners.FiledBusinessOwnerId"))
    StateId = Column(BIGINT, ForeignKey("States.Id"))

    def __repr__(self):
        return f"<FiledProductCatalog(id={self.Id}, name={self.Name}')>"

class BusinessOwnerStates(Base):
    __tablename__ = "BusinessOwnerStates"

    Id = Column(BIGINT, primary_key=True)
    Name = Column(NVARCHAR())
    Value = Column(NVARCHAR())

class FiledBusinessOwners(Base):
    __tablename__ = "FiledBusinessOwners"

    FiledBusinessOwnerId = Column(BIGINT, primary_key=True)
    Name = Column(NVARCHAR())
    BusinessOwnerStateId = Column(BIGINT, ForeignKey("BusinessOwnerStates.Id"))

class FiledProductCatalogPermissions(Base):
    __tablename__ = "FiledProductCatalogPermissions"

    FiledProductCatalogId = Column(BIGINT, ForeignKey("FiledProductCatalogs.FiledBusinessOwnerId"), primary_key=True)
    FiledUserId = Column(BIGINT, primary_key=True)
    FiledBusinessOwnerId = Column(BIGINT, ForeignKey("FiledBusinessOwners.FiledBusinessOwnerId"))

class Platforms(Base):
    __tablename__ = "Platforms"

    Id = Column(BIGINT, primary_key=True)
    Name = Column(NVARCHAR())
    Value = Column(NVARCHAR())

class ExternalPlatforms(Base):
    __tablename__ = "ExternalPlatforms"

    Id = Column(BIGINT, primary_key=True)
    UpdatedAt = Column(DATETIME2(precision=7))
    UpdatedById = Column(BIGINT)
    UpdatedByFirstName = Column(NVARCHAR())
    UpdatedByLastName = Column(NVARCHAR())
    CreatedAt = Column(DATETIME2(precision=7))
    CreatedById = Column(BIGINT)
    CreatedByFirstName = Column(NVARCHAR())
    CreatedByLastName = Column(NVARCHAR())
    IsSource = Column(BIGINT())

    FiledBusinessOwnerId = Column(BIGINT, ForeignKey("FiledBusinessOwners.FiledBusinessOwnerId"))
    PlatformId = Column(BIGINT, ForeignKey("Platforms.Id"))
    MappingPreferences = Column(NVARCHAR())
    Details = Column(NVARCHAR())

class FiledProductCatalogConnections(Base):
    __tablename__ = "FiledProductCatalogConnections"

    FiledProductCatalogId = Column(BIGINT, ForeignKey("FiledProductCatalogs.Id"), primary_key=True)
    ExternalPlatformId = Column(BIGINT, ForeignKey("ExternalPlatforms.Id"), primary_key=True)
    IdInPlatform = Column(NVARCHAR(), default="")

