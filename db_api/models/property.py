from pydantic import BaseModel
from typing import List, Optional, Dict


class Property(BaseModel):
    hash_id: Optional[str]
    transaction: str
    property_type: str
    city: Optional[str]
    city_part: Optional[str] 
    street: Optional[str]
    size_m2: int
    size_kk: Optional[str]

    price: int
    rk: bool
    contact: Dict

    gps: Dict
    url:  str
    additional_info: Optional[Dict] = None
    description: Optional[str] = None
    meta_description: Optional[str] = None
    photos: List[str]
