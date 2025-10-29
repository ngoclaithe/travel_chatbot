from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.hotel import HotelCreate, HotelUpdate, HotelResponse
from app.models.tables import hotels
from app.api.deps import get_db

router = APIRouter()

@router.post("/", response_model=dict, status_code=201)
async def create_hotel(hotel: HotelCreate, db=Depends(get_db)):
    query = hotels.insert().values(**hotel.model_dump())
    last_id = await db.execute(query)
    return {**hotel.model_dump(), "id": last_id}

@router.get("/", response_model=List[dict])
async def get_hotels(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    query = hotels.select().offset(skip).limit(limit)
    return await db.fetch_all(query)

@router.get("/{hotel_id}", response_model=dict)
async def get_hotel(hotel_id: int, db=Depends(get_db)):
    query = hotels.select().where(hotels.c.id == hotel_id)
    result = await db.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return result

@router.put("/{hotel_id}", response_model=dict)
async def update_hotel(hotel_id: int, hotel: HotelUpdate, db=Depends(get_db)):
    update_data = {k: v for k, v in hotel.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    query = hotels.update().where(hotels.c.id == hotel_id).values(**update_data)
    await db.execute(query)
    return await get_hotel(hotel_id, db)

@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db=Depends(get_db)):
    query = hotels.delete().where(hotels.c.id == hotel_id)
    await db.execute(query)
    return {"message": "Hotel deleted"}