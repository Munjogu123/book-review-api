from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException

from api.db.reviews import PostgresDb
from api.models.entry import Review, ReviewCreate, ReviewUpdate
from api.services.reviews import ReviewService

review_router = APIRouter()


async def get_review_service() -> AsyncGenerator[ReviewService, None]:
    async with PostgresDb() as db:
        yield ReviewService(db)


@review_router.post("/books/{book_id}/reviews")
async def create_review(
    review_data: ReviewCreate,
    review_service: ReviewService = Depends(get_review_service),
):
    try:
        review = Review(
            user_id=review_data.user_id,
            book_id=review_data.book_id,
            rating=review_data.rating,
            comment=review_data.comment,
        )
        review_dict = review.model_dump()
        created_review = await review_service.db.create_review(review_dict)

        return {"detail": "Review created successfully", "review": created_review}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating entry: {str(e)}")


@review_router.get("/books/{book_id}/reviews")
async def get_review(
    book_id: str, review_service: ReviewService = Depends(get_review_service)
):
    reviews = await review_service.get_book_reviews(book_id)
    if not reviews:
        raise HTTPException(status_code=404, detail="User not found")

    return reviews


@review_router.patch("/reviews/{review_id}")
async def update_review(
    review_id: str,
    updated_data: ReviewUpdate,
    review_service: ReviewService = Depends(get_review_service),
):
    partial_data = updated_data.model_dump(exclude_unset=True)
    updated_review = await review_service.update_review(review_id, partial_data)
    if not updated_review:
        raise HTTPException(status_code=404, detail="Entry not found")

    return updated_review


@review_router.delete("/reviews/{review_id}")
async def delete_review(
    review_id: str, review_service: ReviewService = Depends(get_review_service)
):
    review = await review_service.db.get_review(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    await review_service.delete_review(review_id)
    return {"detail": f"Deleted review {review_id}"}
