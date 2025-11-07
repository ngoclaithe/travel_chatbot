from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class RestaurantBase(BaseModel):
    name: str
    address: Optional[str] = None
    destination_id: Optional[int] = None
    cuisine_type: Optional[str] = None
    price_range: Optional[str] = None
    rating: Optional[Decimal] = 0

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    destination_id: Optional[int] = None
    cuisine_type: Optional[str] = None
    price_range: Optional[str] = None
    rating: Optional[Decimal] = None

class RestaurantResponse(RestaurantBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True