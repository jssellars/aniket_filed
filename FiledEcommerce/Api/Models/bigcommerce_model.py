from dataclasses import dataclass


@dataclass
class BigCommerceVariant:
    Id: str
    sku: str
    weight: int
    height: int
    width: int
    depth: int
    basePrice: float
    salePrice: float
    Image: str
    inventory: int
    upc: int
    mpn: int
    gtin: int


@dataclass
class BigCommerceProduct:
    id: int
    name: str
    sku: str
    type: str
    path: str
    description: str
    plainTextDescription: str
    addToCartUrl: str
    prices: float
    weight: int
    height: int
    width: int
    depth: int
    options: str
    categories: str
    brand: str
    customFields: str
    Image: str
    inventory: int
    upc: int
    mpn: int
    gtin: int
