from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.transportation import TransportationCreate, TransportationUpdate, TransportationResponse
from app.models.tables import transportation
from app.api.deps import get_db

router = APIRouter()

@router.post("/", response_model=dict, status_code=201)
async def create_transportation(trans: TransportationCreate, db=Depends(get_db)):
    query = transportation.insert().values(**trans.model_dump())
    last_id = await db.execute(query)
    return {**trans.model_dump(), "id": last_id}

@router.get("/", response_model=List[dict])
async def get_transportations(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    query = transportation.select().offset(skip).limit(limit)
    return await db.fetch_all(query)

@router.get("/{trans_id}", response_model=dict)
async def get_transportation(trans_id: int, db=Depends(get_db)):
    query = transportation.select().where(transportation.c.id == trans_id)
    result = await db.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Transportation not found")
    return result

@router.put("/{trans_id}", response_model=dict)
async def update_transportation(trans_id: int, trans: TransportationUpdate, db=Depends(get_db)):
    update_data = {k: v for k, v in trans.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    query = transportation.update().where(transportation.c.id == trans_id).values(**update_data)
    await db.execute(query)
    return await get_transportation(trans_id, db)

@router.delete("/{trans_id}")
async def delete_transportation(trans_id: int, db=Depends(get_db)):
    query = transportation.delete().where(transportation.c.id == trans_id)
    await db.execute(query)
    return {"message": "Transportation deleted"}