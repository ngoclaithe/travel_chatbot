from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class ActivityBase(BaseModel):
    name: str
    destination_id: Optional[int] = None
    type: Optional[str] = None
    price: Optional[Decimal] = None
    duration: Optional[str] = None
    description: Optional[str] = None

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    destination_id: Optional[int] = None
    type: Optional[str] = None
    price: Optional[Decimal] = None
    duration: Optional[str] = None
    description: Optional[str] = None

class ActivityResponse(ActivityBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True