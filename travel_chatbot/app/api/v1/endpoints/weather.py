from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.weather import WeatherCreate, WeatherUpdate, WeatherResponse
from app.models.tables import weather
from app.api.deps import get_db

router = APIRouter()

@router.post("/", response_model=dict, status_code=201)
async def create_weather(w: WeatherCreate, db=Depends(get_db)):
    query = weather.insert().values(**w.model_dump())
    last_id = await db.execute(query)
    return {**w.model_dump(), "id": last_id}

@router.get("/", response_model=List[dict])
async def get_weathers(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    query = weather.select().offset(skip).limit(limit)
    return await db.fetch_all(query)

@router.get("/{weather_id}", response_model=dict)
async def get_weather(weather_id: int, db=Depends(get_db)):
    query = weather.select().where(weather.c.id == weather_id)
    result = await db.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Weather not found")
    return result

@router.put("/{weather_id}", response_model=dict)
async def update_weather(weather_id: int, w: WeatherUpdate, db=Depends(get_db)):
    update_data = {k: v for k, v in w.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    query = weather.update().where(weather.c.id == weather_id).values(**update_data)
    await db.execute(query)
    return await get_weather(weather_id, db)

@router.delete("/{weather_id}")
async def delete_weather(weather_id: int, db=Depends(get_db)):
    query = weather.delete().where(weather.c.id == weather_id)
    await db.execute(query)
    return {"message": "Weather deleted"}
