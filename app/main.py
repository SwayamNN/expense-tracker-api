from fastapi import FastAPI

from app.routers import users, categories, expenses, analytics

app = FastAPI(
    title="Expense Tracker API",
    description="A REST API for managing users, categories, and expenses",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(categories.router)
app.include_router(expenses.router)
app.include_router(analytics.router)


@app.get("/")
def home():
    return {"message": "Welcome to Expense Tracker API"}