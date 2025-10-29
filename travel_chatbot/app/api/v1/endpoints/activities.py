from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityResponse
from app.models.tables import activities
from app.api.deps import get_db

router = APIRouter()

@router.post("/", response_model=dict, status_code=201)
async def create_activity(activity: ActivityCreate, db=Depends(get_db)):
    query = activities.insert().values(**activity.model_dump())
    last_id = await db.execute(query)
    return {**activity.model_dump(), "id": last_id}

@router.get("/", response_model=List[dict])
async def get_activities(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    query = activities.select().offset(skip).limit(limit)
    return await db.fetch_all(query)

@router.get("/{activity_id}", response_model=dict)
async def get_activity(activity_id: int, db=Depends(get_db)):
    query = activities.select().where(activities.c.id == activity_id)
    result = await db.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Activity not found")
    return result

@router.put("/{activity_id}", response_model=dict)
async def update_activity(activity_id: int, activity: ActivityUpdate, db=Depends(get_db)):
    update_data = {k: v for k, v in activity.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    query = activities.update().where(activities.c.id == activity_id).values(**update_data)
    await db.execute(query)
    return await get_activity(activity_id, db)

@router.delete("/{activity_id}")
async def delete_activity(activity_id: int, db=Depends(get_db)):
    query = activities.delete().where(activities.c.id == activity_id)
    await db.execute(query)
    return {"message": "Activity deleted"}