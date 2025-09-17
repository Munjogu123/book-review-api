import logging
from datetime import datetime
from typing import Any, Dict, List

from db.reviews import PostgresDb

logger = logging.getLogger("__name__")


class ReviewService:
    def __init__(self, db: PostgresDb):
        self.db = db
        logger.debug("Review service initialized with PostgresDb client")

    async def create_review(self, review_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Creating new entries")
        now = datetime.now()
        review = {**review_data, "created_at": now, "updated_at": now}
        logger.debug("Successfully created a review")

        return review

    async def get_book_reviews(self, book_id: str) -> List[Dict[str, Any]]:
        logger.info("Getting review info")
        review_data = await self.db.get_book_reviews(book_id)
        if review_data:
            logger.debug("Found review %s", book_id)
        else:
            logger.warning("Could not find review %s", book_id)

        return review_data

    async def update_review(
        self, review_id: str, updated_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        logger.info("Updating review info")
        old_review = await self.db.get_review(review_id)
        if not old_review:
            logger.warning("Review %s not found", review_id)
            return None

        new_review = {
            **old_review,
            **updated_data,
            "id": review_id,
            "user_id": old_review["user_id"],
            "book_id": old_review["book_id"],
            "created_at": old_review["created_at"],
            "updated_at": datetime.now(),
        }
        await self.db.update_review(review_id, new_review)
        logger.debug("Successfully updated review info")

        return new_review

    async def delete_review(self, review_id: str) -> None:
        logger.info("Deleting a review")
        review = await self.db.get_review(review_id)
        if not review:
            logger.warning("Review %s not found", review_id)
            return None

        await self.db.delete_review(review_id)
        logger.debug("Successfully deleted a review")

    async def delete_reviews(self) -> None:
        logger.info("Deleting all reviews")
        reviews = await self.db.get_reviews()
        if not reviews:
            logger.warning("Reviews not found")
            return None

        await self.db.delete_reviews()
        logger.debug("Successfully deleted all reviews")
