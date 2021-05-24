from dataclasses import dataclass


@dataclass
class ShopifyVariant:
    available_for_sale: bool
    barcode: str
    compare_at_price: float
    display_name: str
    image: str
    inventory_quantity: int
    price: float
    product: str
    selected_options: str
    sku: str
    id: str
    tax_code: str
    taxable: bool
    title: str
    weight: float


@dataclass
class ShopifyProduct:
    description: str
    description_html: str
    featured_image: str
    image: str
    online_store_url: str
    price: float
    product_type: str
    id: str
    tags: str
    title: str
    total_inventory: int
    total_variants: int
    vendor: int
