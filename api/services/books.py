import logging
from datetime import datetime
from typing import Any, Dict, List

from db.books import PostgresDb

logger = logging.getLogger("__name__")


class BookService:
    def __init__(self, db: PostgresDb):
        self.db = db
        logger.debug("User service initialized with PostgresDb client")

    async def create_book(self, book_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Creating new entries")
        now = datetime.now()
        book = {**book_data, "created_at": now}
        logger.debug("Successfully created a book")

        return book

    async def get_book(self, book_id: str) -> Dict[str, Any]:
        logger.info("Getting book info")
        book_data = await self.db.get_book(book_id)
        if book_data:
            logger.debug("Found book %s", book_id)
        else:
            logger.warning("Could not find book %s", book_id)

        return book_data

    async def get_books(self) -> List[Dict[str, Any]]:
        logger.info("Getting all books info")
        books = await self.db.get_books()
        if books:
            logger.debug("Found all books")
        else:
            logger.warning("No books found")

        return books

    async def update_book(
        self, book_id: str, updated_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        logger.info("Updating book info")
        old_book = await self.db.get_book(book_id)
        if not old_book:
            logger.warning("Book %s not found", book_id)
            return None

        new_book = {
            **old_book,
            **updated_data,
            "id": book_id,
            "created_at": old_book["created_at"],
        }
        await self.db.update_book(book_id, new_book)
        logger.debug("Successfully updated book info")

        return new_book

    async def delete_book(self, book_id: str) -> None:
        logger.info("Deleting a book")
        book = await self.db.get_book(book_id)
        if not book:
            logger.warning("Book %s not found", book_id)
            return None

        await self.db.delete_book(book_id)
        logger.debug("Successfully deleted a book")

    async def delete_books(self) -> None:
        logger.info("Deleting all books")
        users = await self.db.get_books()
        if not users:
            logger.warning("Books not found")
            return None

        await self.db.delete_books()
        logger.debug("Successfully deleted all books")
