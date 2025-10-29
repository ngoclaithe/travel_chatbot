from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantResponse
from app.models.tables import restaurants
from app.api.deps import get_db

router = APIRouter()

@router.post("/", response_model=dict, status_code=201)
async def create_restaurant(restaurant: RestaurantCreate, db=Depends(get_db)):
    query = restaurants.insert().values(**restaurant.model_dump())
    last_id = await db.execute(query)
    return {**restaurant.model_dump(), "id": last_id}

@router.get("/", response_model=List[dict])
async def get_restaurants(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    query = restaurants.select().offset(skip).limit(limit)
    return await db.fetch_all(query)

@router.get("/{restaurant_id}", response_model=dict)
async def get_restaurant(restaurant_id: int, db=Depends(get_db)):
    query = restaurants.select().where(restaurants.c.id == restaurant_id)
    result = await db.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return result

@router.put("/{restaurant_id}", response_model=dict)
async def update_restaurant(restaurant_id: int, restaurant: RestaurantUpdate, db=Depends(get_db)):
    update_data = {k: v for k, v in restaurant.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    query = restaurants.update().where(restaurants.c.id == restaurant_id).values(**update_data)
    await db.execute(query)
    return await get_restaurant(restaurant_id, db)

@router.delete("/{restaurant_id}")
async def delete_restaurant(restaurant_id: int, db=Depends(get_db)):
    query = restaurants.delete().where(restaurants.c.id == restaurant_id)
    await db.execute(query)
    return {"message": "Restaurant deleted"}