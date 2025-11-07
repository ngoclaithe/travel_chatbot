from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    rating: Optional[int] = None
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    rating: Optional[int] = None
    comment: Optional[str] = None

class ReviewResponse(ReviewBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
