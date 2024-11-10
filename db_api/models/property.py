from pydantic import BaseModel
from typing import List, Optional, Dict

class Property(BaseModel):
    hash_id: Optional[str] = None
    user_id: Optional[str] = None
    transaction: str
    property_type: str
    city: Optional[str]
    city_part: Optional[str] = None
    street: Optional[str]
    size_m2: int
    size_kk: Optional[str] = None
    price: Dict
    rk: bool
    contact: Dict
    additional_info: Optional[Dict] = None
    gps: Dict
    description: Optional[str] = None
    photos: List[str]
    url: Optional[str] = None

