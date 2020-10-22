from Core.Tools.Misc.EnumerationBase import EnumerationBase


class RequestTypeEnum(EnumerationBase):
    GET_PRODUCT_CATALOGS_FOR_BUSINESS = "GetProductCatalogsForBusinessRequest"
    GET_PRODUCT_SETS_FOR_CATALOG = "GetProductSetsForCatalogRequest"
    GET_PRODUCTS_FOR_CATALOG = "GetProductsForCatalogRequest"


class ResponseTypeEnum(EnumerationBase):
    GET_PRODUCT_CATALOGS_FOR_BUSINESS = "GetProductCatalogsForBusinessResponse"
    GET_PRODUCT_SETS_FOR_CATALOG = "GetProductSetsForCatalogResponse"
    GET_PRODUCTS_FOR_CATALOG = "GetProductsForCatalogResponse"
