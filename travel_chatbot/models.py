from sqlalchemy import Column, Integer, String, Numeric, Text, Boolean, DateTime, ARRAY
from sqlalchemy.sql import func
from database import Base

class Destination(Base):
    __tablename__ = "destinations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    province = Column(String(100), nullable=False)
    region = Column(String(50), nullable=False)
    category = Column(String(100))
    rating = Column(Numeric(2, 1), default=0)
    description = Column(Text)
    best_time_to_visit = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    destination_id = Column(Integer)
    type = Column(String(100))
    price = Column(Numeric(10, 2))
    duration = Column(String(100))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Hotel(Base):
    __tablename__ = "hotels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text)
    destination_id = Column(Integer)
    star_rating = Column(Integer)
    price_range = Column(String(50))
    rating = Column(Numeric(2, 1), default=0)
    amenities = Column(ARRAY(Text))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Restaurant(Base):
    __tablename__ = "restaurants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text)
    destination_id = Column(Integer)
    cuisine_type = Column(String(100))
    price_range = Column(String(50))
    rating = Column(Numeric(2, 1), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Tour(Base):
    __tablename__ = "tours"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    destinations = Column(Text)
    duration_days = Column(Integer)
    price = Column(Numeric(10, 2))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Transportation(Base):
    __tablename__ = "transportation"
    
    id = Column(Integer, primary_key=True, index=True)
    from_destination_id = Column(Integer)
    to_destination_id = Column(Integer)
    type = Column(String(50))
    duration = Column(String(100))
    price_range = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Weather(Base):
    __tablename__ = "weather"
    
    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer)
    month = Column(Integer)
    avg_temp = Column(Numeric(4, 1))
    description = Column(Text)
    is_best_time = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50))
    entity_id = Column(Integer)
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(String(255), nullable=False)
    type_name = Column(String(255), nullable=False)
    timestamp = Column(Numeric(53, 2))
    intent_name = Column(String(255))
    action_name = Column(String(255))
    data = Column(Text)