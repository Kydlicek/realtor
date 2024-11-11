from pydantic import BaseModel
from typing import List, Optional, Dict


class Property(BaseModel):
    hash_id: Optional[str] = None
    transaction: str
    property_type: str
    city: Optional[str]
    city_part: Optional[str] = None
    street: Optional[str]
    size_m2: str
    size_kk: Optional[str] = None

    price: Optional[str] = None
    rk: bool
    contact: Dict

    gps: Dict
    url: Optional[str] = None
    additional_info: Optional[Dict] = None
    description: Optional[str] = None
    meta_description: Optional[str] = None
    photos: List[str]
