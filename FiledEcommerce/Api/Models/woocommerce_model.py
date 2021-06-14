from dataclasses import dataclass


@dataclass
class WoocommerceVariant:
    id: str
    display_name: str
    price: str
    compare_at_price: str
    purchasable: bool
    permalink: str
    image: str
    price: float
    sku: str
    stock_quantity: int
    description: str
    date_created: str
    date_modified: str
    imported_at: str


@dataclass
class WoocommerceProduct:
    id: str
    title: str
    type: str
    permalink: str
    price: float
    description: str
    purchasable: bool
    tags: str                
    sku: str
    images: str
    date_created: str
    date_modified: str
