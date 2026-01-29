from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class DestinationBase(BaseModel):
    name: str
    province: str
    region: str
    category: Optional[str] = None
    rating: Optional[Decimal] = 0
    description: Optional[str] = None
    best_time_to_visit: Optional[str] = None
    image_url: Optional[str] = None

class DestinationCreate(DestinationBase):
    pass

class DestinationUpdate(BaseModel):
    name: Optional[str] = None
    province: Optional[str] = None
    region: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[Decimal] = None
    description: Optional[str] = None
    best_time_to_visit: Optional[str] = None
    image_url: Optional[str] = None

class DestinationResponse(DestinationBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
