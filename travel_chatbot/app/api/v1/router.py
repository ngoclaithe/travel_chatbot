from fastapi import APIRouter
from app.api.v1.endpoints import (
    destinations,
    activities,
    hotels,
    restaurants,
    tours,
    transportation,
    weather,
    reviews,
    events
)

api_router = APIRouter()

api_router.include_router(destinations.router, prefix="/destinations", tags=["Destinations"])
api_router.include_router(activities.router, prefix="/activities", tags=["Activities"])
api_router.include_router(hotels.router, prefix="/hotels", tags=["Hotels"])
api_router.include_router(restaurants.router, prefix="/restaurants", tags=["Restaurants"])
api_router.include_router(tours.router, prefix="/tours", tags=["Tours"])
api_router.include_router(transportation.router, prefix="/transportation", tags=["Transportation"])
api_router.include_router(weather.router, prefix="/weather", tags=["Weather"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
api_router.include_router(events.router, prefix="/events", tags=["Events"])
