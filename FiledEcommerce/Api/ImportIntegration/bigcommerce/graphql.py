from sgqlc.types import String, Float, Type, Int, Field, list_of, Boolean
from sgqlc.types.relay import Node, Connection, connection_args


class BigCommercePrice(Type):
    currencyCode = String
    value = Float


class BigCommercePriceEdge(Type):
    price = Field(BigCommercePrice)


class BigCommerceImage(Type):
    url = Field(String, args={
        "width": Int
    })
    urlOriginal = String
    altText = String
    isDefault = Boolean


class BigCommerceMeasurement(Type):
    value = Float
    unit = String


class BigCommerceProductOption(Type):
    entityId = Int
    displayName = String
    isRequired = Boolean


class BigCommerceProductOptionEdge(Type):
    node = Field(BigCommerceProductOption)


class BigCommerceProductOptionConnection(Connection):
    edges = Field(BigCommerceProductOptionEdge)


class BigCommerceAggregated(Type):
    availableToSell = Float
    warningLevel = Int


class BigCommerceInventoryByLocations(Type):
    locationEntityId = Float
    availableToSell = Float
    warningLevel = Int
    isInStock = Boolean
    locationEntityTypeId = String
    locationEntityServiceTypeIds = list_of(String)
    locationEntityCode = String


class BigCommerceInventoryByLocationsEdge(Type):
    node = Field(BigCommerceInventoryByLocations)


class BigCommerceInventoryByLocationsConnection(Connection):
    edges = Field(BigCommerceInventoryByLocationsEdge)


class BigCommerceVariantInventory(Type):
    aggregated = Field(BigCommerceAggregated)
    isInStock = Boolean
    byLocation = Field(BigCommerceInventoryByLocationsConnection)


class BigCommerceVariant(Node):
    entityId = Int
    sku = String
    weight = Field(BigCommerceMeasurement)
    height = Field(BigCommerceMeasurement)
    width = Field(BigCommerceMeasurement)
    depth = Field(BigCommerceMeasurement)
    options = Field(BigCommerceProductOptionConnection)
    prices = Field(BigCommercePriceEdge)
    defaultImage = Field(BigCommerceImage)
    inventory = Field(BigCommerceVariantInventory)
    upc = String
    mpn = String
    gtin = String


class BigCommerceVariantEdge(Type):
    node = Field(BigCommerceVariant)


class BigCommerceVariantConnection(Connection):
    edges = Field(BigCommerceVariantEdge)


class BigCommerceCategory(Node):
    entityId = Int
    name = String
    path = String
    defaultImage = Field(BigCommerceImage)
    description = String


class BigCommerceCategoryEdge(Type):
    node = Field(BigCommerceCategory)


class BigCommerceCategoryConnection(Connection):
    edges = Field(BigCommerceCategoryEdge)


class BigCommerceBrand(Type):
    entityId = Int
    name = String
    defaultImage = Field(BigCommerceImage)
    pageTitle = String
    metaDesc = String
    metaKeywords = list_of(String)
    searchKeywords = list_of(String)
    path = String


class BigCommerceCustomField(Type):
    entityId = Int
    name = String
    value = String


class BigCommerceCustomFieldEdge(Type):
    node = Field(BigCommerceCustomField)


class BigCommerceCustomFieldConnection(Connection):
    edges = Field(BigCommerceCustomFieldEdge)


class BigCommerceAggregatedInventory(Type):
    availableToSell = Int
    warningLevel = Int


class BigCommerceProductInventory(Type):
    isInStock = Boolean
    hasVariantInventory = Boolean
    aggregated = Field(BigCommerceAggregatedInventory)


class BigCommerceProduct(Node):
    entity_id = Int
    name = String
    sku = String
    type = String
    path = String
    description = String
    plainTextDescription = String
    addToCartUrl = String
    prices = Field(BigCommercePriceEdge)
    weight = Field(BigCommerceMeasurement)
    height = Field(BigCommerceMeasurement)
    width = Field(BigCommerceMeasurement)
    depth = Field(BigCommerceMeasurement)
    options = Field(BigCommerceProductOptionConnection)
    categories = Field(BigCommerceCategoryConnection)
    brand = Field(BigCommerceBrand)
    variants = list_of(BigCommerceVariantConnection)
    customFields = Field(BigCommerceCustomFieldConnection)
    defaultImage = Field(BigCommerceImage)
    inventory = Field(BigCommerceProductInventory)
    upc = String
    mpn = String
    gtin = String


class BigCommerceProductEdges(Type):
    node = Field(BigCommerceProduct)


class BigCommerceProductConnection(Connection):
    edges = list_of(BigCommerceProductEdges)


class BigCommerceSite(Type):
    products = Field(BigCommerceProductConnection, args={
        **connection_args()
    })


class Query(Type):
    site = Field(BigCommerceSite)
