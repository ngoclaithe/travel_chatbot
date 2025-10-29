from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Destination Schemas
class DestinationBase(BaseModel):
    name: str
    province: str
    region: str
    category: Optional[str] = None
    rating: Optional[float] = 0
    description: Optional[str] = None
    best_time_to_visit: Optional[str] = None

class DestinationCreate(DestinationBase):
    pass

class DestinationUpdate(BaseModel):
    name: Optional[str] = None
    province: Optional[str] = None
    region: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    description: Optional[str] = None
    best_time_to_visit: Optional[str] = None

class Destination(DestinationBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Activity Schemas
class ActivityBase(BaseModel):
    name: str
    destination_id: Optional[int] = None
    type: Optional[str] = None
    price: Optional[float] = None
    duration: Optional[str] = None
    description: Optional[str] = None

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    destination_id: Optional[int] = None
    type: Optional[str] = None
    price: Optional[float] = None
    duration: Optional[str] = None
    description: Optional[str] = None

class Activity(ActivityBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Hotel Schemas
class HotelBase(BaseModel):
    name: str
    address: Optional[str] = None
    destination_id: Optional[int] = None
    star_rating: Optional[int] = None
    price_range: Optional[str] = None
    rating: Optional[float] = 0
    amenities: Optional[List[str]] = None

class HotelCreate(HotelBase):
    pass

class HotelUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    destination_id: Optional[int] = None
    star_rating: Optional[int] = None
    price_range: Optional[str] = None
    rating: Optional[float] = None
    amenities: Optional[List[str]] = None

class Hotel(HotelBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Restaurant Schemas
class RestaurantBase(BaseModel):
    name: str
    address: Optional[str] = None
    destination_id: Optional[int] = None
    cuisine_type: Optional[str] = None
    price_range: Optional[str] = None
    rating: Optional[float] = 0

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    destination_id: Optional[int] = None
    cuisine_type: Optional[str] = None
    price_range: Optional[str] = None
    rating: Optional[float] = None

class Restaurant(RestaurantBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Tour Schemas
class TourBase(BaseModel):
    name: str
    destinations: Optional[str] = None
    duration_days: Optional[int] = None
    price: Optional[float] = None
    description: Optional[str] = None

class TourCreate(TourBase):
    pass

class TourUpdate(BaseModel):
    name: Optional[str] = None
    destinations: Optional[str] = None
    duration_days: Optional[int] = None
    price: Optional[float] = None
    description: Optional[str] = None

class Tour(TourBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Transportation Schemas
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

class Transportation(TransportationBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Weather Schemas
class WeatherBase(BaseModel):
    destination_id: Optional[int] = None
    month: Optional[int] = None
    avg_temp: Optional[float] = None
    description: Optional[str] = None
    is_best_time: Optional[bool] = False

class WeatherCreate(WeatherBase):
    pass

class WeatherUpdate(BaseModel):
    destination_id: Optional[int] = None
    month: Optional[int] = None
    avg_temp: Optional[float] = None
    description: Optional[str] = None
    is_best_time: Optional[bool] = None

class Weather(WeatherBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Review Schemas
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

class Review(ReviewBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Event Schemas
class EventBase(BaseModel):
    sender_id: str
    type_name: str
    timestamp: Optional[float] = None
    intent_name: Optional[str] = None
    action_name: Optional[str] = None
    data: Optional[str] = None

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    sender_id: Optional[str] = None
    type_name: Optional[str] = None
    timestamp: Optional[float] = None
    intent_name: Optional[str] = None
    action_name: Optional[str] = None
    data: Optional[str] = None

class Event(EventBase):
    id: int
    
    class Config:
        from_attributes = True