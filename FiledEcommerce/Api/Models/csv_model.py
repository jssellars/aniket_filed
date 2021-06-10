from dataclasses import dataclass


@dataclass
class CsvVariant:
    variant_id: str
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


@dataclass
class CsvProduct:
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
