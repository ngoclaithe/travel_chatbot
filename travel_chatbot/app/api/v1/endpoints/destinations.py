from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.destination import DestinationCreate, DestinationUpdate, DestinationResponse
from app.models.tables import destinations
from app.api.deps import get_db

router = APIRouter()

@router.post("/", response_model=dict, status_code=201)
async def create_destination(destination: DestinationCreate, db=Depends(get_db)):
    query = destinations.insert().values(**destination.model_dump())
    last_id = await db.execute(query)
    return {**destination.model_dump(), "id": last_id}


@router.get("/", response_model=List[dict])
async def get_destinations(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    query = destinations.select().offset(skip).limit(limit)
    results = await db.fetch_all(query)
    return [dict(r) for r in results] 


@router.get("/{destination_id}", response_model=dict)
async def get_destination(destination_id: int, db=Depends(get_db)):
    query = destinations.select().where(destinations.c.id == destination_id)
    result = await db.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Destination not found")
    return dict(result)  


@router.put("/{destination_id}", response_model=dict)
async def update_destination(destination_id: int, destination: DestinationUpdate, db=Depends(get_db)):
    update_data = {k: v for k, v in destination.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    query = destinations.update().where(destinations.c.id == destination_id).values(**update_data)
    await db.execute(query)
    
    query_select = destinations.select().where(destinations.c.id == destination_id)
    updated = await db.fetch_one(query_select)
    if not updated:
        raise HTTPException(status_code=404, detail="Destination not found after update")
    return dict(updated)  

@router.delete("/{destination_id}")
async def delete_destination(destination_id: int, db=Depends(get_db)):
    query = destinations.delete().where(destinations.c.id == destination_id)
    await db.execute(query)
    return {"message": "Destination deleted"}
