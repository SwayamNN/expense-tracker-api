# Expense Tracker API

A RESTful backend application built with **FastAPI, PostgreSQL, and SQLAlchemy** for managing users, expense categories, and personal expenses.

## Features

- User creation and retrieval
- Expense category management
- Expense creation, retrieval, updating, and deletion
- Full and partial expense updates
- Expense filtering by category, amount, and date
- Pagination for user records
- Total expense analytics
- Monthly expense analytics
- Category-wise expense analytics
- Input validation using Pydantic
- Layered architecture (Router, Service, CRUD)
- Automated API tests using Pytest

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Uvicorn
- Pytest
- python-dotenv

## Project Structure

```text
expense_tracker_api/
├── app/
│   ├── crud/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── database.py
│   ├── main.py
│   └── models.py
├── tests/
├── .env.example
├── .gitignore
├── create_tables.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd expense_tracker_api
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using the example:

```bash
cp .env.example .env
```

Update the database credentials in `.env`.

### 5. Create the PostgreSQL database

Create a database named:

```sql
CREATE DATABASE expense_tracker;
```

### 6. Create database tables

```bash
python create_tables.py
```

### 7. Start the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome endpoint |
| POST | `/users/` | Create user |
| GET | `/users/` | Retrieve users |
| GET | `/users/{user_id}` | Retrieve user |
| POST | `/categories/` | Create category |
| GET | `/categories/` | Retrieve user categories |
| GET | `/categories/{category_id}` | Retrieve category |
| DELETE | `/categories/{category_id}` | Delete category |
| POST | `/expenses/` | Create expense |
| GET | `/expenses/` | Retrieve user expenses |
| GET | `/expenses/filter/` | Filter expenses |
| GET | `/expenses/{expense_id}` | Retrieve expense |
| PUT | `/expenses/{expense_id}` | Fully update expense |
| PATCH | `/expenses/{expense_id}` | Partially update expense |
| DELETE | `/expenses/{expense_id}` | Delete expense |
| GET | `/analytics/total/{user_id}` | Total expenses |
| GET | `/analytics/monthly/{user_id}` | Monthly analytics |
| GET | `/analytics/category/{user_id}` | Category-wise analytics |

## Testing

Run the automated test suite:

```bash
pytest -v
```

Run tests with code coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

Latest recorded results:

- 39 tests passed
- 84% code coverage

## Architecture

```text
Client
  |
  v
FastAPI Router
  |
  v
Service Layer
  |
  v
CRUD Layer
  |
  v
SQLAlchemy ORM
  |
  v
PostgreSQL
```

## Current Scope

This project focuses on backend development, database engineering, REST API design, and automated testing.

Authentication and authorization are planned as a subsequent learning phase.

## Future Improvements

- JWT authentication
- Password hashing
- Role-based access control
- Database migrations with Alembic
- Docker deployment
- CI/CD integration

## Author

Developed as part of a six-month Python Backend + ML/AI learning roadmap.
