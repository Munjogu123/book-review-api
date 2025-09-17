from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field, field_serializer


class UserCreate(BaseModel):
    username: str = Field(
        min_length=5, max_length=50, description="The name of the user"
    )
    email: EmailStr


class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        None, min_length=5, max_length=50, description="The name of the user"
    )
    email: EmailStr | None = None


class User(BaseModel):
    id: str = Field(default_factory=lambda v: str(uuid4()), description="The user's id")
    username: str = Field(
        min_length=5, max_length=50, description="The name of the user"
    )
    email: EmailStr
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now, description="When the entry was created"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now, description="When the entry was modified"
    )

    @field_serializer("created_at", when_used="json")
    def datetime_serialize(self, dt: datetime, _info):
        return dt.isoformat()


class BookCreate(BaseModel):
    title: str = Field(min_length=10, description="This is the title of the book")
    author: str = Field(
        min_length=10, max_length=100, description="This is the name of the author"
    )
    isbn: Optional[str] = Field(None, description="The ISBN of the book")


class BookUpdate(BaseModel):
    title: str = Field(None, min_length=10, description="This is the title of the book")
    author: str = Field(
        None,
        min_length=10,
        max_length=100,
        description="This is the name of the author",
    )
    isbn: Optional[str] = Field(None, description="The ISBN of the book")


class Book(BaseModel):
    id: str = Field(default_factory=lambda v: str(uuid4()), description="The book's id")
    title: str = Field(min_length=10, description="This is the title of the book")
    author: str = Field(
        min_length=10, max_length=100, description="This is the name of the author"
    )
    isbn: Optional[str] = Field(None, description="The ISBN of the book")
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now, description="The date this entry was created"
    )


class ReviewCreate(BaseModel):
    user_id: str = Field(description="This is the id of the user creating a review")
    book_id: str = Field(description="This is the id of the book being reviewed")
    rating: float = Field(ge=1, le=5)
    comment: str = Field(
        min_length=20, description="This is the actual review of the book"
    )


class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(
        None, ge=1, le=5, description="This is the rating of the book (1-5)"
    )
    comment: Optional[str] = Field(
        None, min_length=20, description="This is the actual review of the book"
    )


class Review(BaseModel):
    id: str = Field(
        default_factory=lambda v: str(uuid4()), description="The id of the review entry"
    )
    user_id: str = Field(description="This is the id of the user creating a review")
    book_id: str = Field(description="This is the id of the book being reviewed")
    rating: float = Field(
        ge=1, le=5, description="This is the rating of the book (1-5)"
    )
    comment: str = Field(
        min_length=20, description="This is the actual review of the book"
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now, description="When the entry was created"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now, description="When the entry was modified"
    )

    @field_serializer("created_at", "updated_at", when_used="json")
    def datetime_serialize(self, dt: datetime, _info):
        return dt.isoformat()
