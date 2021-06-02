from dataclasses import dataclass

@dataclass
class MagentoProductVariant:
  id : int
  name : str
  sku : str
  attribute_set_id: int
  stock_status: str
  canonical_url: str
  image: str
  price : float
  created_at: str
  updated_at: str
  description : str

@dataclass
class MagentoProduct:
  id: str
  name : str
  attribute_set_id : int
  sku : str
  price : float
  currency :str
  stock_status : str
  canonical_url : str
  category : str
  image : str
  created_at: str
  updated_at: str
  custom_fields: dict
  description : str