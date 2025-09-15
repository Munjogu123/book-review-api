from dotenv import load_dotenv
from fastapi import FastAPI
from routers.users import user_router

load_dotenv()

app = FastAPI(
    title="A Book Review API",
    description="API for managing books, reviews, and ratings",
)
app.include_router(user_router)
