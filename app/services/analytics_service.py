
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models import Expense


def get_total_expenses(db: Session, user_id: int):
    return db.query(
        func.coalesce(func.sum(Expense.amount), 0)
    ).filter(
        Expense.user_id == user_id
    ).scalar()


def get_monthly_expenses(
    db: Session,
    user_id: int,
    year: int
):
    return db.query(
        extract("month", Expense.expense_date).label("month"),
        func.sum(Expense.amount).label("total")
    ).filter(
        Expense.user_id == user_id,
        extract("year", Expense.expense_date) == year
    ).group_by(
        extract("month", Expense.expense_date)
    ).order_by(
        extract("month", Expense.expense_date)
    ).all()


def get_category_expenses(db: Session, user_id: int):
    return db.query(
        Expense.category_id,
        func.sum(Expense.amount).label("total")
    ).filter(
        Expense.user_id == user_id
    ).group_by(
        Expense.category_id
    ).all()
