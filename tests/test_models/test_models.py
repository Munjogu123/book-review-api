from datetime import datetime

import pytest
from pydantic import ValidationError

from api.models.entry import BookCreate, ReviewCreate, User


def test_book_create_success():
    data = {"title": "A Great Book", "author": "George Orwell", "isbn": "1234567890"}

    book = BookCreate(**data)

    assert book.title == "A Great Book"
    assert book.author == "George Orwell"
    assert book.isbn == "1234567890"


def test_book_create_validation_error():
    data = {
        "title": "Short Title",
        "author": "TooShort",
        "isbn": "1234567890",
    }

    with pytest.raises(ValidationError):
        BookCreate(**data)


def test_user_model_defaults():
    user = User(
        username="testuser",
        email="test@example.com",
    )

    assert user.id is not None
    assert isinstance(user.id, str)

    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)

    json_data = user.model_dump_json()
    assert "created_at" in json_data
    assert "updated_at" in json_data
    assert "T" in user.created_at.isoformat()


def test_review_create_success():
    review = ReviewCreate(
        user_id="1",
        book_id="10",
        rating=4,
        comment="This book was extremely insightful and interesting.",
    )

    assert review.rating == 4
    assert review.comment.startswith("This book")


def test_review_create_validation_error():
    with pytest.raises(ValidationError):
        ReviewCreate(user_id="1", book_id="10", rating=6, comment="Too short")
