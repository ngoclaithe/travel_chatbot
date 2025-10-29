from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse
from app.models.tables import reviews
from app.api.deps import get_db

router = APIRouter()

@router.post("/", response_model=dict, status_code=201)
async def create_review(review: ReviewCreate, db=Depends(get_db)):
    query = reviews.insert().values(**review.model_dump())
    last_id = await db.execute(query)
    return {**review.model_dump(), "id": last_id}

@router.get("/", response_model=List[dict])
async def get_reviews(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    query = reviews.select().offset(skip).limit(limit)
    return await db.fetch_all(query)

@router.get("/{review_id}", response_model=dict)
async def get_review(review_id: int, db=Depends(get_db)):
    query = reviews.select().where(reviews.c.id == review_id)
    result = await db.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Review not found")
    return result

@router.put("/{review_id}", response_model=dict)
async def update_review(review_id: int, review: ReviewUpdate, db=Depends(get_db)):
    update_data = {k: v for k, v in review.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    query = reviews.update().where(reviews.c.id == review_id).values(**update_data)
    await db.execute(query)
    return await get_review(review_id, db)

@router.delete("/{review_id}")
async def delete_review(review_id: int, db=Depends(get_db)):
    query = reviews.delete().where(reviews.c.id == review_id)
    await db.execute(query)
    return {"message": "Review deleted"}