from dotenv import load_dotenv
from fastapi import FastAPI

from api.routers import books, reviews, users

load_dotenv()

app = FastAPI(
    title="A Book Review API",
    description="API for managing books, reviews, and ratings",
)
app.include_router(users.user_router)
app.include_router(books.book_router)
app.include_router(reviews.review_router)
