def test_create_review_success(client, mock_review_service, review_payload):
    response = client.post("/books/1/reviews", json=review_payload)

    assert response.status_code == 200
    assert response.json()["detail"] == "Review created successfully"
    assert response.json()["review"] == review_payload

    mock_review_service.create_review.assert_awaited_once()


def test_create_review_failure(client, mock_review_service_error, review_payload):
    response = client.post("/books/1/reviews", json=review_payload)

    assert response.status_code == 400
    assert "Error creating entry" in response.json()["detail"]


def test_get_review_success(client, mock_review_service):
    response = client.get("/books/1/reviews")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id"] == "100"
    assert data[1]["id"] == "101"


def test_get_review_failure(client, mock_review_service_error):
    response = client.get("/books/1/reviews")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_review_success(client, mock_review_service):
    payload = {"rating": 3.7}
    response = client.patch("/reviews/100", json=payload)

    assert response.status_code == 200
    assert response.json()["rating"] == 3.7

    mock_review_service.update_review.assert_awaited_once_with("100", payload)


def test_update_review_failure(client, mock_review_service_error):
    payload = {"rating": 3.7}
    response = client.patch("/reviews/100", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Entry not found"


def test_delete_review_success(client, mock_review_service):
    response = client.delete("/reviews/100")

    assert response.status_code == 200
    assert response.json()["detail"] == "Deleted review 100"

    mock_review_service.delete_review.assert_awaited_once()


def test_delete_review_failure(client, mock_review_service_error):
    response = client.delete("/reviews/100")

    assert response.status_code == 404
    assert response.json()["detail"] == "Review not found"
