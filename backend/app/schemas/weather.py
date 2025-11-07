from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class WeatherBase(BaseModel):
    destination_id: Optional[int] = None
    month: Optional[int] = None
    avg_temp: Optional[Decimal] = None
    description: Optional[str] = None
    is_best_time: Optional[bool] = False

class WeatherCreate(WeatherBase):
    pass

class WeatherUpdate(BaseModel):
    destination_id: Optional[int] = None
    month: Optional[int] = None
    avg_temp: Optional[Decimal] = None
    description: Optional[str] = None
    is_best_time: Optional[bool] = None

class WeatherResponse(WeatherBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True