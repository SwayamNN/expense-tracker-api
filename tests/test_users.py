
def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Expense Tracker API"
    }


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "name": "Testing User",
            "email": "testing@example.com"
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Testing User"
    assert response.json()["email"] == "testing@example.com"


def test_duplicate_email(client):
    user_data = {
        "name": "Testing User",
        "email": "testing@example.com"
    }

    first_response = client.post("/users/", json=user_data)
    second_response = client.post("/users/", json=user_data)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Email already registered"



def test_reject_invalid_email(client):
    response = client.post(
        "/users/",
        json={
            "name": "Invalid Email User",
            "email": "not-an-email"
        }
    )

    assert response.status_code == 422



def test_get_nonexistent_user(client):
    response = client.get("/users/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_users_list(client):
    client.post(
        "/users/",
        json={"name": "User One", "email": "one@example.com"}
    )
    client.post(
        "/users/",
        json={"name": "User Two", "email": "two@example.com"}
    )

    response = client.get("/users/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_users_pagination(client):
    for i in range(3):
        client.post(
            "/users/",
            json={
                "name": f"User {i}",
                "email": f"user{i}@example.com"
            }
        )

    response = client.get("/users/?skip=1&limit=1")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == "user1@example.com"
