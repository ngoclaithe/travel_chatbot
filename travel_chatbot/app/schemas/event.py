from pydantic import BaseModel
from typing import Optional

class EventBase(BaseModel):
    sender_id: str
    type_name: str
    timestamp: Optional[float] = None
    intent_name: Optional[str] = None
    action_name: Optional[str] = None
    data: Optional[str] = None

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    
    class Config:
        from_attributes = True