from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransportationBase(BaseModel):
    from_destination_id: Optional[int] = None
    to_destination_id: Optional[int] = None
    type: Optional[str] = None
    duration: Optional[str] = None
    price_range: Optional[str] = None

class TransportationCreate(TransportationBase):
    pass

class TransportationUpdate(BaseModel):
    from_destination_id: Optional[int] = None
    to_destination_id: Optional[int] = None
    type: Optional[str] = None
    duration: Optional[str] = None
    price_range: Optional[str] = None

class TransportationResponse(TransportationBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True