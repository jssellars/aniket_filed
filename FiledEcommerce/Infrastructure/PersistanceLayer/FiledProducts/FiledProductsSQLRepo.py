from FiledEcommerce.Infrastructure.PersistanceLayer.FiledProducts.models import *
from FiledEcommerce.Infrastructure.PersistanceLayer.EcommerceSQL_ORM_Model import session_scope

class FiledProductsSQLRepo:

    @staticmethod
    def getFiledVariantsByFiledSetId(id:int):
        with session_scope() as session:
            filed_set =  session.query(FiledSets).filter(FiledSets.Id == id).first()
            if filed_set and filed_set.FiledProductCatalogs:
                return filed_set.FiledProductCatalogs.FiledVariants, str(filed_set.Name)
            return [], None

    @staticmethod
    def getFiledVariantsByFiledSmartSetId(id:int):
        with session_scope() as session:
            smart_set = session.query(FiledSmartSets).filter(FiledSmartSets.Id == id).first()
            if smart_set and smart_set.FiledProductCatalogs:
                return smart_set.FiledProductCatalogs.FiledVariants, str(smart_set.Name)
            return [], None

    @staticmethod
    def getCurrencies():
        with session_scope() as session:
            return session.query(Currencies).all()
    
    # @staticmethod
    # def getFiledProductCatalogById(id):
    #     with session_scope() as session:
    #         return session.query(FiledProductCatalogs).filter(FiledProductCatalogs.Id == id).first()
    
    # @staticmethod
    # def getFiledProductById(id):
    #     with session_scope() as session:
    #         return session.query(FiledProducts).filter(FiledProducts.Id == id).first()

    # @staticmethod
    # def getFiledProductVariantById(id):
    #     with session_scope() as session:
    #         return session.query(FiledVariants).filter(FiledVariants.Id == id).first()
