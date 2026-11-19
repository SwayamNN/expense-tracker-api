
def test_create_category(client):
    # First, create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Category Test User",
            "email": "categorytest@example.com"
        }
    )

    user_id = user_response.json()["user_id"]

    # Create a category for that user
    response = client.post(
        "/categories/",
        json={
            "name": "Food",
            "description": "Food and dining expenses",
            "user_id": user_id
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Food"
    assert response.json()["user_id"] == user_id



def test_get_categories(client):
    # Create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Retrieval User",
            "email": "retrieval@example.com"
        }
    )

    user_id = user_response.json()["user_id"]

    # Create a category
    client.post(
        "/categories/",
        json={
            "name": "Travel",
            "description": "Travel expenses",
            "user_id": user_id
        }
    )

    # Retrieve categories belonging to this user
    response = client.get(
        "/categories/",
        params={"user_id": user_id}
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Travel"



def test_get_category_by_id(client):
    # Create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Single Category User",
            "email": "singlecategory@example.com"
        }
    )

    user_id = user_response.json()["user_id"]

    # Create a category
    category_response = client.post(
        "/categories/",
        json={
            "name": "Shopping",
            "description": "Shopping expenses",
            "user_id": user_id
        }
    )

    category_id = category_response.json()["category_id"]

    # Retrieve the category by ID
    response = client.get(
        f"/categories/{category_id}",
        params={"user_id": user_id}
    )

    assert response.status_code == 200
    assert response.json()["category_id"] == category_id
    assert response.json()["name"] == "Shopping"



def test_delete_category(client):
    # Create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Delete Test User",
            "email": "deletecategory@example.com"
        }
    )

    user_id = user_response.json()["user_id"]

    # Create a category
    category_response = client.post(
        "/categories/",
        json={
            "name": "Entertainment",
            "description": "Entertainment expenses",
            "user_id": user_id
        }
    )

    category_id = category_response.json()["category_id"]

    # Delete the category
    response = client.delete(
        f"/categories/{category_id}",
        params={"user_id": user_id}
    )

    assert response.status_code == 200

    # Confirm the category no longer exists
    get_response = client.get(
        f"/categories/{category_id}",
        params={"user_id": user_id}
    )

    assert get_response.status_code == 404



def test_reject_another_users_category(client):
    # Create first user
    user1_response = client.post(
        "/users/",
        json={
            "name": "First User",
            "email": "firstuser@example.com"
        }
    )
    user1_id = user1_response.json()["user_id"]

    # Create second user
    user2_response = client.post(
        "/users/",
        json={
            "name": "Second User",
            "email": "seconduser@example.com"
        }
    )
    user2_id = user2_response.json()["user_id"]

    # Create a category belonging to first user
    category_response = client.post(
        "/categories/",
        json={
            "name": "Food",
            "description": "Food expenses",
            "user_id": user1_id
        }
    )
    category_id = category_response.json()["category_id"]

    # Second user attempts to use first user's category
    response = client.post(
        "/expenses/",
        json={
            "title": "Lunch",
            "amount": "200.00",
            "description": "Unauthorized category usage",
            "expense_date": "2026-11-19T13:00:00",
            "user_id": user2_id,
            "category_id": category_id
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Category does not belong to this user"
    )

def test_reject_another_users_category(client):
    # Create two users
    user1 = client.post(
        "/users/",
        json={"name": "First User", "email": "first@example.com"}
    ).json()

    user2 = client.post(
        "/users/",
        json={"name": "Second User", "email": "second@example.com"}
    ).json()

    # Create a category for the first user
    category = client.post(
        "/categories/",
        json={
            "name": "Food",
            "description": "Food expenses",
            "user_id": user1["user_id"]
        }
    ).json()

    # Second user attempts to access it
    response = client.get(
        f"/categories/{category['category_id']}",
        params={"user_id": user2["user_id"]}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"



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


def test_reject_category_for_nonexistent_user(client):
    response = client.post(
        "/categories/",
        json={
            "name": "Food",
            "description": "Food expenses",
            "user_id": 9999
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_categories_for_nonexistent_user(client):
    response = client.get(
        "/categories/",
        params={"user_id": 9999}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_nonexistent_category(client):
    response = client.delete(
        "/categories/9999",
        params={"user_id": 9999}
    )

    assert response.status_code == 404
