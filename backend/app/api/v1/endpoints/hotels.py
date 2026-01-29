from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.hotel import HotelCreate, HotelUpdate, HotelResponse
from app.models.tables import hotels
from app.api.deps import get_db

router = APIRouter()


@router.post("/", response_model=dict, status_code=201)
async def create_hotel(hotel: HotelCreate, db=Depends(get_db)):
    query = hotels.insert().values(**hotel.dict())
    last_id = await db.execute(query)
    return {**hotel.dict(), "id": last_id}


@router.get("/", response_model=List[dict])
async def get_hotels(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    query = hotels.select().offset(skip).limit(limit)
    results = await db.fetch_all(query)
    return [dict(r) for r in results]  


@router.get("/{hotel_id}", response_model=dict)
async def get_hotel(hotel_id: int, db=Depends(get_db)):
    query = hotels.select().where(hotels.c.id == hotel_id)
    result = await db.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return dict(result) 


@router.put("/{hotel_id}", response_model=dict)
async def update_hotel(hotel_id: int, hotel: HotelUpdate, db=Depends(get_db)):
    update_data = {k: v for k, v in hotel.dict(exclude_unset=True).items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    query = hotels.update().where(hotels.c.id == hotel_id).values(**update_data)
    await db.execute(query)

    query_select = hotels.select().where(hotels.c.id == hotel_id)
    updated = await db.fetch_one(query_select)
    if not updated:
        raise HTTPException(status_code=404, detail="Hotel not found after update")
    return dict(updated)  


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db=Depends(get_db)):
    query = hotels.delete().where(hotels.c.id == hotel_id)
    await db.execute(query)
    return {"message": "Hotel deleted"}
