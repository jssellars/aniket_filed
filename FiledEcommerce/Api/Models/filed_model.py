from dataclasses import dataclass
from typing import List


@dataclass
class FiledCustomProperties:
    properties: dict


@dataclass
class FiledVariant:
    variant_id: str
    filed_product_id: str
    display_name: str
    price: str
    compare_at_price: str
    availability: bool
    url: str
    image_url: str
    sku: str
    barcode: str
    inventory_quantity: int
    tags: str
    description: str
    created_at: str
    updated_at: str
    imported_at: str
    material: str = None
    condition: str = None
    brand: str = None
    color: str = None
    size: str = None
    custom_props: FiledCustomProperties = None


@dataclass
class FiledProduct:
    product_id: str
    title: str
    product_type: str
    vendor: str
    description: str
    tags: str
    sku: str
    image_url: str
    created_at: str
    updated_at: str
    imported_at: str
    variants: List[FiledVariant]
