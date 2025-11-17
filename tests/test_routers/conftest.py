from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.routers.books import get_book_service


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def payload():
    return {
        "title": "1984",
        "author": "George Owell",
        "isbn": "1234567890",
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
