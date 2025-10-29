from sqlalchemy.orm import Session
from typing import List, Optional, Type, TypeVar, Generic
from models import (
    Destination, Activity, Hotel, Restaurant, Tour, 
    Transportation, Weather, Review, Event
)
from schemas import (
    DestinationCreate, DestinationUpdate,
    ActivityCreate, ActivityUpdate,
    HotelCreate, HotelUpdate,
    RestaurantCreate, RestaurantUpdate,
    TourCreate, TourUpdate,
    TransportationCreate, TransportationUpdate,
    WeatherCreate, WeatherUpdate,
    ReviewCreate, ReviewUpdate,
    EventCreate, EventUpdate
)

ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType')
UpdateSchemaType = TypeVar('UpdateSchemaType')

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, id: int, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if db_obj:
            update_data = obj_in.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_obj, field, value)
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> bool:
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False

# CRUD instances for each model
crud_destination = CRUDBase[Destination, DestinationCreate, DestinationUpdate](Destination)
crud_activity = CRUDBase[Activity, ActivityCreate, ActivityUpdate](Activity)
crud_hotel = CRUDBase[Hotel, HotelCreate, HotelUpdate](Hotel)
crud_restaurant = CRUDBase[Restaurant, RestaurantCreate, RestaurantUpdate](Restaurant)
crud_tour = CRUDBase[Tour, TourCreate, TourUpdate](Tour)
crud_transportation = CRUDBase[Transportation, TransportationCreate, TransportationUpdate](Transportation)
crud_weather = CRUDBase[Weather, WeatherCreate, WeatherUpdate](Weather)
crud_review = CRUDBase[Review, ReviewCreate, ReviewUpdate](Review)
crud_event = CRUDBase[Event, EventCreate, EventUpdate](Event)