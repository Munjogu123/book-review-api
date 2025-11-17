from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.routers.books import get_book_service
from api.routers.reviews import get_review_service


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def book_payload():
    return {
        "title": "1984",
        "author": "George Owell",
        "isbn": "1234567890",
    }


@pytest.fixture
def review_payload():
    return {
        "id": "100",
        "user_id": "10",
        "book_id": "1",
        "rating": 4.5,
        "comment": "This was such an interesting read. Got to learn a lot and I have been applying some of the lessons I learned and I can already see some difference.",
    }


@pytest.fixture
def mock_book_service():
    class MockService:
        def __init__(self):
            self.db = AsyncMock()
            self.create_book = self.db.create_book
            self.get_book = self.db.get_book
            self.get_books = self.db.get_books
            self.update_book = self.db.update_book
            self.delete_book = self.db.delete_book
            self.delete_books = self.db.delete_books

    service = MockService()

    service.create_book.return_value = {
        "id": "1",
        "title": "1984",
        "author": "George Owell",
        "isbn": "1234567890",
    }

    service.get_book.return_value = {
        "id": "1",
        "title": "1984",
        "author": "George Owell",
        "isbn": "1234567890",
    }

    service.get_books.return_value = [
        {"id": "1", "title": "1984", "author": "George Orwell", "isbn": "1234567890"},
        {
            "id": "2",
            "title": "Animal Farm",
            "author": "George Orwell",
            "isbn": "9876543210",
        },
    ]

    service.update_book.return_value = {
        "id": "1",
        "title": "1984 (Updated)",
        "author": "George Orwell",
        "isbn": "1234567890",
    }

    service.delete_book.return_value = {"detail": "Deleted book 1"}
    service.delete_books.return_value = {"detail": "Deleted all books"}

    app.dependency_overrides[get_book_service] = lambda: service
    yield service
    app.dependency_overrides.clear()


@pytest.fixture
def mock_review_service():
    class MockService:
        def __init__(self):
            self.db = AsyncMock()
            self.create_review = self.db.create_review
            self.get_review = self.db.get_review
            self.update_review = self.db.update_review
            self.delete_review = self.db.delete_review

        async def get_book_reviews(self, book_id):
            return [
                {
                    "id": "100",
                    "user_id": "10",
                    "book_id": book_id,
                    "rating": 4.5,
                    "comment": "This was such an interesting read. Got to learn a lot and I have been applying some of the lessons I learned and I can already see some difference.",
                },
                {
                    "id": "101",
                    "user_id": "11",
                    "book_id": book_id,
                    "rating": 4.2,
                    "comment": "I absolutely loved the book. I have a new perspective on life and how I can make it better. Highly recommend!",
                },
            ]

    service = MockService()

    service.create_review.return_value = {
        "id": "100",
        "user_id": "10",
        "book_id": "1",
        "rating": 4.5,
        "comment": "This was such an interesting read. Got to learn a lot and I have been applying some of the lessons I learned and I can already see some difference.",
    }

    service.update_review.return_value = {
        "id": "100",
        "user_id": "10",
        "book_id": "1",
        "rating": 3.7,
        "comment": "This was such an interesting read. Got to learn a lot and I have been applying some of the lessons I learned and I can already see some difference.",
    }

    service.delete_review.return_value = {"detail": "Deleted review 100"}

    app.dependency_overrides[get_review_service] = lambda: service
    yield service
    app.dependency_overrides.clear()


@pytest.fixture
def mock_book_service_error():
    class MockService:
        def __init__(self):
            self.db = AsyncMock()
            self.create_book = self.db.create_book
            self.get_book = self.db.get_book
            self.get_books = self.db.get_books
            self.update_book = self.db.update_book
            self.delete_book = self.db.delete_book
            self.delete_books = self.db.delete_books

    service = MockService()

    service.create_book.side_effect = Exception("DB error")
    service.get_book.return_value = None
    service.get_books.side_effect = Exception("DB error")
    service.update_book.return_value = None
    service.delete_book.return_value = None

    app.dependency_overrides[get_book_service] = lambda: service
    yield service
    app.dependency_overrides.clear()


@pytest.fixture
def mock_review_service_error():
    class MockService:
        def __init__(self):
            self.db = AsyncMock()
            self.create_review = self.db.create_review
            self.get_review = self.db.get_review
            self.get_book_reviews = AsyncMock(return_value=None)
            self.update_review = self.db.update_review
            self.delete_review = self.db.delete_review

    service = MockService()

    service.create_review.side_effect = Exception("DB error")
    service.update_review.return_value = None
    service.delete_review.return_value = None
    service.get_review.return_value = None

    app.dependency_overrides[get_review_service] = lambda: service
    yield service
    app.dependency_overrides.clear()
