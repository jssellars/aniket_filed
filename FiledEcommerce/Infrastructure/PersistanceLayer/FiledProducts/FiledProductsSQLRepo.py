from FiledEcommerce.Infrastructure.PersistanceLayer.FiledProducts.models import *
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceSQL_ORM_Model import (
    session_scope,
)
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
import json
from FiledEcommerce.Api.utils.tools.date_utils import get_utc_aware_date


class FiledProductsSQLRepo:
    @staticmethod
    def getFiledVariantsByFiledSetId(id: int):
        with session_scope() as session:
            filed_set = session.query(FiledSets).filter(FiledSets.Id == id).first()
            if filed_set and filed_set.FiledProductCatalogs:
                return filed_set.FiledProductCatalogs.FiledVariants, str(filed_set.Name)
            return [], None

    @staticmethod
    def getFiledVariantsByFiledSmartSetId(id: int):
        with session_scope() as session:
            smart_set = (
                session.query(FiledSmartSets).filter(FiledSmartSets.Id == id).first()
            )
            if smart_set and smart_set.FiledProductCatalogs:
                return smart_set.FiledProductCatalogs.FiledVariants, str(smart_set.Name)
            return [], None

    @staticmethod
    def getCurrencies():
        with session_scope() as session:
            return session.query(Currencies).all()

    @staticmethod
    def getPlatforms():
        with session_scope() as session:
            return session.query(Platforms).all()

    @staticmethod
    def getPlatformByValue(value):
        with session_scope() as session:
            return session.query(Platforms).filter(Platforms.Value == value).first()

    @staticmethod
    def getExternalPlatformByFiledBussinessId(FiledBusinessOwnerId, platformId):
        with session_scope() as session:
            return (
                session.query(ExternalPlatforms)
                .filter(
                    ExternalPlatforms.FiledBusinessOwnerId == FiledBusinessOwnerId,
                    ExternalPlatforms.PlatformId == platformId,
                )
                .first()
            )

    @staticmethod
    def getFiledProductCatalogConnection(catalogId: int, externalPlatformId: int):
        with session_scope() as session:
            return session.query(FiledProductCatalogConnections).filter(
                FiledProductCatalogConnections.FiledProductCatalogId == catalogId,
                FiledProductCatalogConnections.ExternalPlatformId == externalPlatformId,
            ).first()

    @staticmethod
    def createFiledProductCatalogConnections(
        filedProductCatalogConnections: FiledProductCatalogConnections,
    ):
        with session_scope() as session:
            return session.add(filedProductCatalogConnections)

    def createOrUpdateFiledProductCatalogConnections(
        filedProductCatalogConnections: FiledProductCatalogConnections,
    ):
        filed_product_catalog_connection_from_db = (
            FiledProductsSQLRepo.getFiledProductCatalogConnection(
                filedProductCatalogConnections.FiledProductCatalogId,
                filedProductCatalogConnections.ExternalPlatformId,
            )
        )
        if filed_product_catalog_connection_from_db:
            with session_scope() as session:
                return (
                    session.query(FiledProductCatalogConnections)
                    .filter(
                        FiledProductCatalogConnections.FiledProductCatalogId
                        == filed_product_catalog_connection_from_db.FiledProductCatalogId,
                        filedProductCatalogConnections.ExternalPlatformId
                        == filed_product_catalog_connection_from_db.ExternalPlatformId,
                    )
                    .update(filedProductCatalogConnections)
                )

        return FiledProductsSQLRepo.createFiledProductCatalogConnections(
            filedProductCatalogConnections
        )

    @staticmethod
    def createExternalPlatform(externalPlatform: ExternalPlatforms):
        with session_scope() as session:
            return session.add(externalPlatform)

    @staticmethod
    def createOrupdateExternalPlatform(externalPlatform: ExternalPlatforms):
        external_platforms_row_from_db = (
            FiledProductsSQLRepo.getExternalPlatformByFiledBussinessId(
                externalPlatform.FiledBusinessOwnerId, externalPlatform.PlatformId
            )
        )
        if external_platforms_row_from_db:
            with session_scope() as session:
                temp_external_platform = {}
                externalPlatform = externalPlatform.__dict__
                externalPlatform.pop("_sa_instance_state", None)

                pydanticExternalPlatforms = sqlalchemy_to_pydantic(ExternalPlatforms)
                pyndantic_external_platform = pydanticExternalPlatforms.from_orm(
                    external_platforms_row_from_db
                ).dict()
                # this is to make sure we only patch the value.. we should not update the values
                for key, value in pyndantic_external_platform.items():
                    if key == "Id":
                        continue
                    if key == "Details":
                        detail = value
                        if key in externalPlatform:
                            detail = json.loads(value) if value else {}
                            # updating or adding new keys in details column
                            detail.update(json.loads(externalPlatform[key]))
                        externalPlatform[key] = json.dumps(detail)
                    temp_external_platform[key] = externalPlatform.get(key, value)

                temp_external_platform["UpdatedAt"] = get_utc_aware_date()
                temp_external_platform["UpdatedById"] = temp_external_platform[
                    "CreatedById"
                ]
                temp_external_platform["UpdatedByFirstName"] = temp_external_platform[
                    "CreatedByFirstName"
                ]
                temp_external_platform["UpdatedByLastName"] = temp_external_platform[
                    "CreatedByLastName"
                ]

                return (
                    session.query(ExternalPlatforms)
                    .filter(ExternalPlatforms.Id == external_platforms_row_from_db.Id)
                    .update(dict(temp_external_platform))
                )  # update a new entry in database if not present

        return FiledProductsSQLRepo.createExternalPlatform(
            externalPlatform
        )  # create a new entry in database if not present
