def test_create_book_success(client, mock_book_service, payload):
    response = client.post("/books/", json=payload)

    assert response.status_code == 200
    assert response.json()["detail"] == "Book created successfully"
    assert response.json()["book"]["title"] == "1984"

    mock_book_service.create_book.assert_awaited_once()


def test_create_book_failure(client, mock_book_service_error, payload):
    response = client.post("/books/", json=payload)

    assert response.status_code == 400
    assert "Error creating book" in response.json()["detail"]


def test_get_book_success(client, mock_book_service):
    response = client.get("/books/1")

    assert response.status_code == 200
    assert response.json()["title"] == "1984"

    mock_book_service.db.get_book.assert_awaited_once_with("1")


def test_get_book_failure(client, mock_book_service_error):
    response = client.get("/books/200")

    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_get_books_success(client, mock_book_service):
    response = client.get("/books")

    assert response.status_code == 200
    assert response.json()["books"] == [
        {"id": "1", "title": "1984", "author": "George Orwell", "isbn": "1234567890"},
        {
            "id": "2",
            "title": "Animal Farm",
            "author": "George Orwell",
            "isbn": "9876543210",
        },
    ]

    mock_book_service.get_books.assert_awaited_once()


def test_get_books_failure(client, mock_book_service_error):
    response = client.get("/books")

    assert response.status_code == 500
    assert "Error retrieving book" in response.json()["detail"]


def test_update_book_success(client, mock_book_service):
    update_payload = {"title": "1984 (Updated)"}
    response = client.patch("/books/1", json=update_payload)

    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "title": "1984 (Updated)",
        "author": "George Orwell",
        "isbn": "1234567890",
    }

    mock_book_service.update_book.assert_awaited_once_with("1", update_payload)


def test_update_book_failure(client, mock_book_service_error):
    update_payload = {"title": "Atomic Habits"}
    response = client.patch("/books/200", json=update_payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_delete_book_success(client, mock_book_service):
    response = client.delete("/books/1")

    assert response.status_code == 200
    assert response.json()["detail"] == "Deleted book 1"

    mock_book_service.delete_book.assert_awaited_once()


def test_delete_book_failure(client, mock_book_service_error):
    response = client.delete("/books/1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_delete_books_success(client, mock_book_service):
    response = client.delete("/books")

    assert response.json()["detail"] == "Deleted all books"
