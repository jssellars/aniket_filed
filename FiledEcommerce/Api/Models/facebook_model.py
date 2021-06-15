from dataclasses import dataclass

@dataclass
class FacebookProduct:
    id: str
    name: str
    description: str
    availability: str
    condition: str
    price: str
    link: str
    addToCartUrl: str
    image_link: str
    brand: str
    quantity_to_sell_on_facebook: str
    fb_product_category: str
    google_product_category: str
    product_type: str
    sale_price: str
    sale_price_effective_date: str
    shipping: str
    shipping_weight: str
    item_group_id: int
    size: str
    age_group: str
    color: str
    gender: str
    material: str
    disabled_capabilities: str
