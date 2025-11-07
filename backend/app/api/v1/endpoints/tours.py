from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.tour import TourCreate, TourUpdate, TourResponse
from app.models.tables import tours
from app.api.deps import get_db

router = APIRouter()

@router.post("/", response_model=dict, status_code=201)
async def create_tour(tour: TourCreate, db=Depends(get_db)):
    query = tours.insert().values(**tour.model_dump())
    last_id = await db.execute(query)
    return {**tour.model_dump(), "id": last_id}

@router.get("/", response_model=List[dict])
async def get_tours(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    query = tours.select().offset(skip).limit(limit)
    results = await db.fetch_all(query)
    return [dict(r) for r in results]

@router.get("/{tour_id}", response_model=dict)
async def get_tour(tour_id: int, db=Depends(get_db)):
    query = tours.select().where(tours.c.id == tour_id)
    result = await db.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Tour not found")
    return dict(result)

@router.put("/{tour_id}", response_model=dict)
async def update_tour(tour_id: int, tour: TourUpdate, db=Depends(get_db)):
    update_data = {k: v for k, v in tour.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    query = tours.update().where(tours.c.id == tour_id).values(**update_data)
    await db.execute(query)
    query_select = tours.select().where(tours.c.id == tour_id)
    updated = await db.fetch_one(query_select)
    if not updated:
        raise HTTPException(status_code=404, detail="Tour not found after update")
    return dict(updated)

@router.delete("/{tour_id}")
async def delete_tour(tour_id: int, db=Depends(get_db)):
    query = tours.delete().where(tours.c.id == tour_id)
    await db.execute(query)
    return {"message": "Tour deleted"}
