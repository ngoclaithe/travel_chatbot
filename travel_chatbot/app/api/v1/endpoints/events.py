from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.event import EventCreate, EventResponse
from app.models.tables import events
from app.api.deps import get_db

router = APIRouter()


@router.post("/", response_model=dict, status_code=201)
async def create_event(event: EventCreate, db=Depends(get_db)):
    query = events.insert().values(**event.model_dump())
    last_id = await db.execute(query)
    return {**event.model_dump(), "id": last_id}


@router.get("/", response_model=List[dict])
async def get_events(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    query = events.select().offset(skip).limit(limit)
    results = await db.fetch_all(query)
    return [dict(r) for r in results] 


@router.get("/{event_id}", response_model=dict)
async def get_event(event_id: int, db=Depends(get_db)):
    query = events.select().where(events.c.id == event_id)
    result = await db.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return dict(result)  
