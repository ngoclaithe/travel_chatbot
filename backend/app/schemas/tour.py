from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class TourBase(BaseModel):
    name: str
    destinations: Optional[str] = None
    duration_days: Optional[int] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class TourCreate(TourBase):
    pass

class TourUpdate(BaseModel):
    name: Optional[str] = None
    destinations: Optional[str] = None
    duration_days: Optional[int] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class TourResponse(TourBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True