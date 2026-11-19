
def test_get_total_expenses(client):
    # Create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Analytics Test User",
            "email": "analyticstest@example.com"
        }
    )
    user_id = user_response.json()["user_id"]

    # Create a category
    category_response = client.post(
        "/categories/",
        json={
            "name": "Food",
            "description": "Food expenses",
            "user_id": user_id
        }
    )
    category_id = category_response.json()["category_id"]

    # Create two expenses
    for title, amount in [
        ("Lunch", "200.00"),
        ("Dinner", "300.00")
    ]:
        client.post(
            "/expenses/",
            json={
                "title": title,
                "amount": amount,
                "description": "Food expense",
                "expense_date": "2026-11-18T13:00:00",
                "user_id": user_id,
                "category_id": category_id
            }
        )

    # Get total expenses
    response = client.get(
    f"/analytics/total/{user_id}"
)

    assert response.status_code == 200
    assert float(response.json()["total_expenses"]) == 500.00


def test_get_monthly_expenses(client):
    # Create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Monthly Analytics User",
            "email": "monthlyanalytics@example.com"
        }
    )
    user_id = user_response.json()["user_id"]

    # Create a category
    category_response = client.post(
        "/categories/",
        json={
            "name": "Food",
            "description": "Food expenses",
            "user_id": user_id
        }
    )
    category_id = category_response.json()["category_id"]

    # Create expenses in January and February
    expenses = [
        ("January Lunch", "200.00", "2026-01-15T13:00:00"),
        ("February Dinner", "300.00", "2026-02-15T19:00:00"),
        ("February Breakfast", "100.00", "2026-02-20T08:00:00")
    ]

    for title, amount, date in expenses:
        client.post(
            "/expenses/",
            json={
                "title": title,
                "amount": amount,
                "description": "Monthly test expense",
                "expense_date": date,
                "user_id": user_id,
                "category_id": category_id
            }
        )

    # Request monthly analytics for 2026
    response = client.get(
        f"/analytics/monthly/{user_id}",
        params={"year": 2026}
    )

    assert response.status_code == 200

    results = response.json()

    assert len(results) == 2
    assert results[0]["month"] == 1
    assert float(results[0]["total"]) == 200.00
    assert results[1]["month"] == 2
    assert float(results[1]["total"]) == 400.00


def test_get_category_expenses(client):
    # Create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Category Analytics User",
            "email": "categoryanalytics@example.com"
        }
    )
    user_id = user_response.json()["user_id"]

    # Create two categories
    food_response = client.post(
        "/categories/",
        json={
            "name": "Food",
            "description": "Food expenses",
            "user_id": user_id
        }
    )
    food_id = food_response.json()["category_id"]

    travel_response = client.post(
        "/categories/",
        json={
            "name": "Travel",
            "description": "Travel expenses",
            "user_id": user_id
        }
    )
    travel_id = travel_response.json()["category_id"]

    # Create expenses in both categories
    expenses = [
        ("Lunch", "200.00", food_id),
        ("Dinner", "300.00", food_id),
        ("Bus Ticket", "100.00", travel_id)
    ]

    for title, amount, category_id in expenses:
        client.post(
            "/expenses/",
            json={
                "title": title,
                "amount": amount,
                "description": "Analytics test expense",
                "expense_date": "2026-11-18T13:00:00",
                "user_id": user_id,
                "category_id": category_id
            }
        )

    # Request category-wise analytics
    response = client.get(
        f"/analytics/category/{user_id}"
    )

    assert response.status_code == 200

    results = response.json()

    assert len(results) == 2

    totals = {
        item["category_id"]: float(item["total"])
        for item in results
    }

    assert totals[food_id] == 500.00
    assert totals[travel_id] == 100.00


def test_total_expenses_without_expenses(client):
    user = client.post("/users/", json={
        "name": "Empty User", "email": "empty@example.com"
    }).json()

    response = client.get(
        f"/analytics/total/{user['user_id']}"
    )

    assert response.status_code == 200
    assert float(response.json()["total_expenses"]) == 0.0


def test_monthly_expenses_without_expenses(client):
    user = client.post("/users/", json={
        "name": "Empty User", "email": "monthlyempty@example.com"
    }).json()

    response = client.get(
        f"/analytics/monthly/{user['user_id']}?year=2026"
    )

    assert response.status_code == 200
    assert response.json() == []


def test_category_expenses_without_expenses(client):
    user = client.post("/users/", json={
        "name": "Empty User", "email": "categoryempty@example.com"
    }).json()

    response = client.get(
        f"/analytics/category/{user['user_id']}"
    )

    assert response.status_code == 200
    assert response.json() == []
