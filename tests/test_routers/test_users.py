def test_create_user_success(client, mock_user_service, user_payload):
    response = client.post("/users/", json=user_payload)

    assert response.status_code == 200
    assert response.json()["detail"] == "User created successfully"
    assert response.json()["user"]["id"] == "01"

    mock_user_service.create_user.assert_awaited_once()


def test_create_user_failure(client, mock_user_service_error, user_payload):
    response = client.post("/users/", json=user_payload)

    assert response.status_code == 400
    assert "Error creating entry" in response.json()["detail"]


def test_get_user_success(client, mock_user_service):
    response = client.get("/users/01")

    assert response.status_code == 200
    assert response.json()["username"] == "fredm"

    mock_user_service.get_user.assert_awaited_once_with("01")


def test_get_user_failure(client, mock_user_service_error):
    response = client.get("/users/01")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_users_success(client, mock_user_service):
    response = client.get("/users")

    assert response.status_code == 200
    assert response.json()["users"] == [
        {
            "id": "01",
            "username": "fredm",
            "email": "fredm@example.com",
        },
        {
            "id": "02",
            "username": "alext",
            "email": "alext@example.com",
        },
    ]

    mock_user_service.get_users.assert_awaited_once()


def test_get_users_failure(client, mock_user_service_error):
    response = client.get("/users")

    assert response.status_code == 500
    assert "Error retrieving entry" in response.json()["detail"]


def test_update_user_success(client, mock_user_service):
    update_payload = {"username": "fredz"}
    response = client.patch("/users/01", json=update_payload)

    assert response.status_code == 200
    assert response.json() == {
        "id": "01",
        "username": "fredz",
        "email": "fredz@example.com",
    }

    mock_user_service.update_user.assert_awaited_once_with("01", update_payload)


def test_update_user_failure(client, mock_user_service_error):
    update_payload = {"username": "fredm"}
    response = client.patch("/users/01", json=update_payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Entry not found"


def test_delete_user_success(client, mock_user_service):
    response = client.delete("/users/01")

    assert response.status_code == 200
    assert response.json()["detail"] == "Deleted user 01"

    mock_user_service.delete_user.assert_awaited_once()


def test_delete_user_failure(client, mock_user_service_error):
    response = client.delete("/users/01")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_users_success(client, mock_user_service):
    response = client.delete("/users")

    assert response.json()["detail"] == "Deleted all users"
