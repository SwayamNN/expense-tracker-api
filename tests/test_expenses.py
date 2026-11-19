
def test_create_expense(client):
    # Create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Expense Test User",
            "email": "expensetest@example.com"
        }
    )

    assert user_response.status_code == 201
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

    assert category_response.status_code == 201
    category_id = category_response.json()["category_id"]

    # Create an expense
    response = client.post(
        "/expenses/",
        json={
            "title": "Lunch",
            "amount": "250.00",
            "description": "Lunch at a restaurant",
            "expense_date": "2026-11-18T13:00:00",
            "user_id": user_id,
            "category_id": category_id
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Lunch"
    assert response.json()["amount"] == "250.00"
    assert response.json()["user_id"] == user_id
    assert response.json()["category_id"] == category_id



def test_get_user_expenses(client):
    # Create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Expense Retrieval User",
            "email": "retrievalexpense@example.com"
        }
    )
    user_id = user_response.json()["user_id"]

    # Create a category
    category_response = client.post(
        "/categories/",
        json={
            "name": "Transport",
            "description": "Transport expenses",
            "user_id": user_id
        }
    )
    category_id = category_response.json()["category_id"]

    # Create an expense
    client.post(
        "/expenses/",
        json={
            "title": "Bus Ticket",
            "amount": "50.00",
            "description": "Daily commute",
            "expense_date": "2026-11-18T09:00:00",
            "user_id": user_id,
            "category_id": category_id
        }
    )

    # Retrieve all expenses for this user
    response = client.get(
        "/expenses/",
        params={"user_id": user_id}
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Bus Ticket"


def test_get_expense_by_id(client):
    # Create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Single Expense User",
            "email": "singleexpense@example.com"
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

    # Create an expense
    expense_response = client.post(
        "/expenses/",
        json={
            "title": "Headphones",
            "amount": "1500.00",
            "description": "Wireless headphones",
            "expense_date": "2026-11-18T15:00:00",
            "user_id": user_id,
            "category_id": category_id
        }
    )
    expense_id = expense_response.json()["expense_id"]

    # Retrieve the expense by ID
    response = client.get(
        f"/expenses/{expense_id}",
        params={"user_id": user_id}
    )

    assert response.status_code == 200
    assert response.json()["expense_id"] == expense_id
    assert response.json()["title"] == "Headphones"


def test_update_expense(client):
    # Create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Update Expense User",
            "email": "updateexpense@example.com"
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

    # Create an expense
    expense_response = client.post(
        "/expenses/",
        json={
            "title": "Breakfast",
            "amount": "100.00",
            "description": "Morning meal",
            "expense_date": "2026-11-18T08:00:00",
            "user_id": user_id,
            "category_id": category_id
        }
    )
    expense_id = expense_response.json()["expense_id"]

    # Update the expense
    response = client.put(
        f"/expenses/{expense_id}",
        params={"user_id": user_id},
        json={
            "title": "Breakfast and Coffee",
            "amount": "180.00",
            "description": "Morning meal with coffee",
            "expense_date": "2026-11-18T08:00:00",
            "user_id": user_id,
            "category_id": category_id
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Breakfast and Coffee"
    assert response.json()["amount"] == "180.00"


def test_delete_expense(client):
    # Create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Delete Expense User",
            "email": "deleteexpense@example.com"
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

    # Create an expense
    expense_response = client.post(
        "/expenses/",
        json={
            "title": "Movie Ticket",
            "amount": "300.00",
            "description": "Cinema ticket",
            "expense_date": "2026-11-18T18:00:00",
            "user_id": user_id,
            "category_id": category_id
        }
    )
    expense_id = expense_response.json()["expense_id"]

    # Delete the expense
    response = client.delete(
        f"/expenses/{expense_id}",
        params={"user_id": user_id}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Expense deleted successfully"

    # Confirm it no longer exists
    get_response = client.get(
        f"/expenses/{expense_id}",
        params={"user_id": user_id}
    )

    assert get_response.status_code == 404


def test_filter_expenses_by_amount(client):
    # Create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Filter Test User",
            "email": "filterexpense@example.com"
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
        ("Lunch", "150.00"),
        ("Dinner", "500.00")
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

    # Filter expenses with amount >= 200
    response = client.get(
        "/expenses/filter/",
        params={
            "user_id": user_id,
            "min_amount": "200.00"
        }
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Dinner"



def test_filter_expenses_by_category(client):
    # Create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Category Filter User",
            "email": "categoryfilter@example.com"
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

    # Create one expense in each category
    for title, category_id in [
        ("Lunch", food_id),
        ("Bus Ticket", travel_id)
    ]:
        client.post(
            "/expenses/",
            json={
                "title": title,
                "amount": "100.00",
                "description": "Test expense",
                "expense_date": "2026-11-18T13:00:00",
                "user_id": user_id,
                "category_id": category_id
            }
        )

    # Filter by Food category
    response = client.get(
        "/expenses/filter/",
        params={
            "user_id": user_id,
            "category_id": food_id
        }
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Lunch"
    assert response.json()[0]["category_id"] == food_id



def test_filter_expenses_by_date(client):
    # Create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Date Filter User",
            "email": "datefilter@example.com"
        }
    )
    user_id = user_response.json()["user_id"]

    # Create a category
    category_response = client.post(
        "/categories/",
        json={
            "name": "Travel",
            "description": "Travel expenses",
            "user_id": user_id
        }
    )
    category_id = category_response.json()["category_id"]

    # Create expenses on two different dates
    for title, date in [
        ("Bus Ticket", "2026-11-10T09:00:00"),
        ("Train Ticket", "2026-11-18T09:00:00")
    ]:
        client.post(
            "/expenses/",
            json={
                "title": title,
                "amount": "200.00",
                "description": "Travel expense",
                "expense_date": date,
                "user_id": user_id,
                "category_id": category_id
            }
        )

    # Filter expenses from November 15 onwards
    response = client.get(
        "/expenses/filter/",
        params={
            "user_id": user_id,
            "start_date": "2026-11-15T00:00:00"
        }
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Train Ticket"



def test_partial_update_expense(client):
    # Create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Patch Test User",
            "email": "patchtest@example.com"
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

    # Create an expense
    expense_response = client.post(
        "/expenses/",
        json={
            "title": "Lunch",
            "amount": "200.00",
            "description": "Lunch expense",
            "expense_date": "2026-11-18T13:00:00",
            "user_id": user_id,
            "category_id": category_id
        }
    )
    expense_id = expense_response.json()["expense_id"]

    # Update only the amount
    response = client.patch(
        f"/expenses/{expense_id}",
        params={"user_id": user_id},
        json={"amount": "450.00"}
    )

    assert response.status_code == 200
    assert response.json()["amount"] == "450.00"
    assert response.json()["title"] == "Lunch"
    assert response.json()["description"] == "Lunch expense"


def test_reject_invalid_expense_amounts(client):
    # Create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Validation Test User",
            "email": "validation@example.com"
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

    # Try creating expenses with invalid amounts
    for amount in ["0.00", "-100.00"]:
        response = client.post(
            "/expenses/",
            json={
                "title": "Invalid Expense",
                "amount": amount,
                "description": "Testing validation",
                "expense_date": "2026-11-18T13:00:00",
                "user_id": user_id,
                "category_id": category_id
            }
        )

        assert response.status_code == 422



def test_reject_invalid_expense_filter_range(client):
    # Create a user
    user_response = client.post(
        "/users/",
        json={
            "name": "Filter Validation User",
            "email": "filtervalidation@example.com"
        }
    )
    user_id = user_response.json()["user_id"]

    # Set minimum amount greater than maximum amount
    response = client.get(
        "/expenses/filter/",
        params={
            "user_id": user_id,
            "min_amount": "500.00",
            "max_amount": "100.00"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Minimum amount cannot exceed maximum amount"
    )



def test_get_expenses_for_nonexistent_user(client):
    response = client.get(
        "/expenses/",
        params={"user_id": 9999}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_reject_another_users_expense(client):
    user1 = client.post("/users/", json={
        "name": "User One", "email": "one@example.com"
    }).json()

    user2 = client.post("/users/", json={
        "name": "User Two", "email": "two@example.com"
    }).json()

    category = client.post("/categories/", json={
        "name": "Food",
        "user_id": user1["user_id"]
    }).json()

    expense = client.post("/expenses/", json={
        "title": "Lunch",
        "amount": "200.00",
        "expense_date": "2026-11-19T13:00:00",
        "user_id": user1["user_id"],
        "category_id": category["category_id"]
    }).json()

    response = client.get(
        f"/expenses/{expense['expense_id']}",
        params={"user_id": user2["user_id"]}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


def test_reject_another_users_expense_update(client):
    user1 = client.post("/users/", json={
        "name": "User One", "email": "one@example.com"
    }).json()

    user2 = client.post("/users/", json={
        "name": "User Two", "email": "two@example.com"
    }).json()

    category = client.post("/categories/", json={
        "name": "Food", "user_id": user1["user_id"]
    }).json()

    expense = client.post("/expenses/", json={
        "title": "Lunch",
        "amount": "200.00",
        "expense_date": "2026-11-19T13:00:00",
        "user_id": user1["user_id"],
        "category_id": category["category_id"]
    }).json()

    response = client.put(
        f"/expenses/{expense['expense_id']}",
        params={"user_id": user2["user_id"]},
        json={
            "title": "Updated Lunch",
            "amount": "300.00",
            "expense_date": "2026-11-19T13:00:00",
            "user_id": user2["user_id"],
            "category_id": category["category_id"]
        }
    )

    assert response.status_code == 400


def test_reject_another_users_expense_delete(client):
    user1 = client.post("/users/", json={
        "name": "User One", "email": "one@example.com"
    }).json()

    user2 = client.post("/users/", json={
        "name": "User Two", "email": "two@example.com"
    }).json()

    category = client.post("/categories/", json={
        "name": "Food", "user_id": user1["user_id"]
    }).json()

    expense = client.post("/expenses/", json={
        "title": "Lunch",
        "amount": "200.00",
        "expense_date": "2026-11-19T13:00:00",
        "user_id": user1["user_id"],
        "category_id": category["category_id"]
    }).json()

    response = client.delete(
        f"/expenses/{expense['expense_id']}",
        params={"user_id": user2["user_id"]}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


def test_partial_update_only_changes_title(client):
    user = client.post("/users/", json={
        "name": "Test User", "email": "partial@example.com"
    }).json()

    category = client.post("/categories/", json={
        "name": "Food", "user_id": user["user_id"]
    }).json()

    expense = client.post("/expenses/", json={
        "title": "Lunch",
        "amount": "200.00",
        "expense_date": "2026-11-19T13:00:00",
        "user_id": user["user_id"],
        "category_id": category["category_id"]
    }).json()

    response = client.patch(
        f"/expenses/{expense['expense_id']}",
        params={"user_id": user["user_id"]},
        json={"title": "Dinner"}
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Dinner"
    assert response.json()["amount"] == "200.00"


def test_reject_partial_update_with_negative_amount(client):
    user = client.post("/users/", json={
        "name": "Test User", "email": "negative@example.com"
    }).json()

    response = client.patch(
        "/expenses/9999",
        params={"user_id": user["user_id"]},
        json={"amount": "-100.00"}
    )

    assert response.status_code == 422
