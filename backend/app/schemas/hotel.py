from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

class HotelBase(BaseModel):
    name: str
    address: Optional[str] = None
    destination_id: Optional[int] = None
    star_rating: Optional[int] = None
    price_range: Optional[str] = None
    rating: Optional[Decimal] = 0
    amenities: Optional[List[str]] = None

class HotelCreate(HotelBase):
    pass

class HotelUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    destination_id: Optional[int] = None
    star_rating: Optional[int] = None
    price_range: Optional[str] = None
    rating: Optional[Decimal] = None
    amenities: Optional[List[str]] = None

class HotelResponse(HotelBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True