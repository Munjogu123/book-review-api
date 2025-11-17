from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException

from api.db.books import PostgresDb
from api.models.entry import Book, BookCreate, BookUpdate
from api.services.books import BookService

book_router = APIRouter()


async def get_book_service() -> AsyncGenerator[BookService, None]:
    async with PostgresDb() as db:
        yield BookService(db)


@book_router.post("/books/")
async def create_book(
    book_data: BookCreate, book_service: BookService = Depends(get_book_service)
):
    try:
        book = Book(title=book_data.title, author=book_data.author, isbn=book_data.isbn)
        book_dict = book.model_dump()
        created_book = await book_service.db.create_book(book_dict)

        return {"detail": "Book created successfully", "book": created_book}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating book: {str(e)}")


@book_router.get("/books/{book_id}")
async def get_book(book_id: str, book_service: BookService = Depends(get_book_service)):
    book = await book_service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@book_router.get("/books")
async def get_books(book_service: BookService = Depends(get_book_service)):
    try:
        book = await book_service.get_books()
        return {"books": book}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving book {str(e)}")


@book_router.patch("/books/{book_id}")
async def update_book(
    book_id: str,
    updated_data: BookUpdate,
    book_service: BookService = Depends(get_book_service),
):
    partial_data = updated_data.model_dump(exclude_unset=True)
    updated_book = await book_service.update_book(book_id, partial_data)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return updated_book


@book_router.delete("/books/{book_id}")
async def delete_book(
    book_id: str, book_service: BookService = Depends(get_book_service)
):
    book = await book_service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    await book_service.delete_book(book_id)
    return {"detail": f"Deleted book {book_id}"}


@book_router.delete("/books")
async def delete_books(book_service: BookService = Depends(get_book_service)):
    await book_service.delete_books()
    return {"detail": "Deleted all books"}
