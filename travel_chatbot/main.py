from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas
import crud

app = FastAPI(title="Travel Chatbot API", version="1.0.0")

# Destination endpoints
@app.post("/destinations/", response_model=schemas.Destination)
def create_destination(destination: schemas.DestinationCreate, db: Session = Depends(get_db)):
    return crud.crud_destination.create(db, destination)

@app.get("/destinations/", response_model=List[schemas.Destination])
def read_destinations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.crud_destination.get_all(db, skip=skip, limit=limit)

@app.get("/destinations/{destination_id}", response_model=schemas.Destination)
def read_destination(destination_id: int, db: Session = Depends(get_db)):
    db_destination = crud.crud_destination.get(db, destination_id)
    if db_destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")
    return db_destination

@app.put("/destinations/{destination_id}", response_model=schemas.Destination)
def update_destination(destination_id: int, destination: schemas.DestinationUpdate, db: Session = Depends(get_db)):
    db_destination = crud.crud_destination.update(db, destination_id, destination)
    if db_destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")
    return db_destination

@app.delete("/destinations/{destination_id}")
def delete_destination(destination_id: int, db: Session = Depends(get_db)):
    success = crud.crud_destination.delete(db, destination_id)
    if not success:
        raise HTTPException(status_code=404, detail="Destination not found")
    return {"message": "Destination deleted successfully"}

# Activity endpoints
@app.post("/activities/", response_model=schemas.Activity)
def create_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    return crud.crud_activity.create(db, activity)

@app.get("/activities/", response_model=List[schemas.Activity])
def read_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.crud_activity.get_all(db, skip=skip, limit=limit)

@app.get("/activities/{activity_id}", response_model=schemas.Activity)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    db_activity = crud.crud_activity.get(db, activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity

@app.put("/activities/{activity_id}", response_model=schemas.Activity)
def update_activity(activity_id: int, activity: schemas.ActivityUpdate, db: Session = Depends(get_db)):
    db_activity = crud.crud_activity.update(db, activity_id, activity)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity

@app.delete("/activities/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    success = crud.crud_activity.delete(db, activity_id)
    if not success:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"message": "Activity deleted successfully"}

# Hotel endpoints
@app.post("/hotels/", response_model=schemas.Hotel)
def create_hotel(hotel: schemas.HotelCreate, db: Session = Depends(get_db)):
    return crud.crud_hotel.create(db, hotel)

@app.get("/hotels/", response_model=List[schemas.Hotel])
def read_hotels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.crud_hotel.get_all(db, skip=skip, limit=limit)

@app.get("/hotels/{hotel_id}", response_model=schemas.Hotel)
def read_hotel(hotel_id: int, db: Session = Depends(get_db)):
    db_hotel = crud.crud_hotel.get(db, hotel_id)
    if db_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return db_hotel

@app.put("/hotels/{hotel_id}", response_model=schemas.Hotel)
def update_hotel(hotel_id: int, hotel: schemas.HotelUpdate, db: Session = Depends(get_db)):
    db_hotel = crud.crud_hotel.update(db, hotel_id, hotel)
    if db_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return db_hotel

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    success = crud.crud_hotel.delete(db, hotel_id)
    if not success:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return {"message": "Hotel deleted successfully"}

# Restaurant endpoints
@app.post("/restaurants/", response_model=schemas.Restaurant)
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    return crud.crud_restaurant.create(db, restaurant)

@app.get("/restaurants/", response_model=List[schemas.Restaurant])
def read_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.crud_restaurant.get_all(db, skip=skip, limit=limit)

@app.get("/restaurants/{restaurant_id}", response_model=schemas.Restaurant)
def read_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    db_restaurant = crud.crud_restaurant.get(db, restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant

@app.put("/restaurants/{restaurant_id}", response_model=schemas.Restaurant)
def update_restaurant(restaurant_id: int, restaurant: schemas.RestaurantUpdate, db: Session = Depends(get_db)):
    db_restaurant = crud.crud_restaurant.update(db, restaurant_id, restaurant)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant

@app.delete("/restaurants/{restaurant_id}")
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    success = crud.crud_restaurant.delete(db, restaurant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return {"message": "Restaurant deleted successfully"}

# Tour endpoints
@app.post("/tours/", response_model=schemas.Tour)
def create_tour(tour: schemas.TourCreate, db: Session = Depends(get_db)):
    return crud.crud_tour.create(db, tour)

@app.get("/tours/", response_model=List[schemas.Tour])
def read_tours(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.crud_tour.get_all(db, skip=skip, limit=limit)

@app.get("/tours/{tour_id}", response_model=schemas.Tour)
def read_tour(tour_id: int, db: Session = Depends(get_db)):
    db_tour = crud.crud_tour.get(db, tour_id)
    if db_tour is None:
        raise HTTPException(status_code=404, detail="Tour not found")
    return db_tour

@app.put("/tours/{tour_id}", response_model=schemas.Tour)
def update_tour(tour_id: int, tour: schemas.TourUpdate, db: Session = Depends(get_db)):
    db_tour = crud.crud_tour.update(db, tour_id, tour)
    if db_tour is None:
        raise HTTPException(status_code=404, detail="Tour not found")
    return db_tour

@app.delete("/tours/{tour_id}")
def delete_tour(tour_id: int, db: Session = Depends(get_db)):
    success = crud.crud_tour.delete(db, tour_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tour not found")
    return {"message": "Tour deleted successfully"}

# Transportation endpoints
@app.post("/transportation/", response_model=schemas.Transportation)
def create_transportation(transportation: schemas.TransportationCreate, db: Session = Depends(get_db)):
    return crud.crud_transportation.create(db, transportation)

@app.get("/transportation/", response_model=List[schemas.Transportation])
def read_transportation(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.crud_transportation.get_all(db, skip=skip, limit=limit)

@app.get("/transportation/{transportation_id}", response_model=schemas.Transportation)
def read_transportation_item(transportation_id: int, db: Session = Depends(get_db)):
    db_transportation = crud.crud_transportation.get(db, transportation_id)
    if db_transportation is None:
        raise HTTPException(status_code=404, detail="Transportation not found")
    return db_transportation

@app.put("/transportation/{transportation_id}", response_model=schemas.Transportation)
def update_transportation(transportation_id: int, transportation: schemas.TransportationUpdate, db: Session = Depends(get_db)):
    db_transportation = crud.crud_transportation.update(db, transportation_id, transportation)
    if db_transportation is None:
        raise HTTPException(status_code=404, detail="Transportation not found")
    return db_transportation

@app.delete("/transportation/{transportation_id}")
def delete_transportation(transportation_id: int, db: Session = Depends(get_db)):
    success = crud.crud_transportation.delete(db, transportation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transportation not found")
    return {"message": "Transportation deleted successfully"}

# Weather endpoints
@app.post("/weather/", response_model=schemas.Weather)
def create_weather(weather: schemas.WeatherCreate, db: Session = Depends(get_db)):
    return crud.crud_weather.create(db, weather)

@app.get("/weather/", response_model=List[schemas.Weather])
def read_weather(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.crud_weather.get_all(db, skip=skip, limit=limit)

@app.get("/weather/{weather_id}", response_model=schemas.Weather)
def read_weather_item(weather_id: int, db: Session = Depends(get_db)):
    db_weather = crud.crud_weather.get(db, weather_id)
    if db_weather is None:
        raise HTTPException(status_code=404, detail="Weather not found")
    return db_weather

@app.put("/weather/{weather_id}", response_model=schemas.Weather)
def update_weather(weather_id: int, weather: schemas.WeatherUpdate, db: Session = Depends(get_db)):
    db_weather = crud.crud_weather.update(db, weather_id, weather)
    if db_weather is None:
        raise HTTPException(status_code=404, detail="Weather not found")
    return db_weather

@app.delete("/weather/{weather_id}")
def delete_weather(weather_id: int, db: Session = Depends(get_db)):
    success = crud.crud_weather.delete(db, weather_id)
    if not success:
        raise HTTPException(status_code=404, detail="Weather not found")
    return {"message": "Weather deleted successfully"}

# Review endpoints
@app.post("/reviews/", response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.crud_review.create(db, review)

@app.get("/reviews/", response_model=List[schemas.Review])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.crud_review.get_all(db, skip=skip, limit=limit)

@app.get("/reviews/{review_id}", response_model=schemas.Review)
def read_review(review_id: int, db: Session = Depends(get_db)):
    db_review = crud.crud_review.get(db, review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@app.put("/reviews/{review_id}", response_model=schemas.Review)
def update_review(review_id: int, review: schemas.ReviewUpdate, db: Session = Depends(get_db)):
    db_review = crud.crud_review.update(db, review_id, review)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@app.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    success = crud.crud_review.delete(db, review_id)
    if not success:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted successfully"}

# Event endpoints
@app.post("/events/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.crud_event.create(db, event)

@app.get("/events/", response_model=List[schemas.Event])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.crud_event.get_all(db, skip=skip, limit=limit)

@app.get("/events/{event_id}", response_model=schemas.Event)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.crud_event.get(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@app.put("/events/{event_id}", response_model=schemas.Event)
def update_event(event_id: int, event: schemas.EventUpdate, db: Session = Depends(get_db)):
    db_event = crud.crud_event.update(db, event_id, event)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@app.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    success = crud.crud_event.delete(db, event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted successfully"}

@app.get("/")
def read_root():
    return {"message": "Travel Chatbot API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)