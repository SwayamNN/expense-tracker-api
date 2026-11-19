
from sqlalchemy.orm import Session
from sqlalchemy import and_
import datetime
from app.models import Expense
from app.schemas.expense import ExpenseCreate


def create_expense(db: Session, expense: ExpenseCreate):
    db_expense = Expense(**expense.model_dump())

    try:
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
        return db_expense

    except Exception:
        db.rollback()
        raise


def get_expense(db: Session, expense_id: int):
    return db.query(Expense).filter(
        Expense.expense_id == expense_id
    ).first()


def get_user_expenses(db: Session, user_id: int):
    return db.query(Expense).filter(
        Expense.user_id == user_id
    ).all()


def update_expense(
    db: Session,
    expense_id: int,
    expense_data: ExpenseCreate
):
    expense = get_expense(db, expense_id)

    if expense is None:
        return None

    try:
        for key, value in expense_data.model_dump().items():
            setattr(expense, key, value)

        db.commit()
        db.refresh(expense)
        return expense

    except Exception:
        db.rollback()
        raise


def delete_expense(db: Session, expense_id: int):
    expense = get_expense(db, expense_id)

    if expense is None:
        return None

    try:
        db.delete(expense)
        db.commit()
        return expense

    except Exception:
        db.rollback()
        raise



from datetime import datetime

def filter_expenses(
    db: Session,
    user_id: int,
    category_id: int = None,
    min_amount: float = None,
    max_amount: float = None,
    start_date: datetime = None,
    end_date: datetime = None
):
    filters = [Expense.user_id == user_id]

    if category_id is not None:
        filters.append(Expense.category_id == category_id)

    if min_amount is not None:
        filters.append(Expense.amount >= min_amount)

    if max_amount is not None:
        filters.append(Expense.amount <= max_amount)

    if start_date is not None:
        filters.append(Expense.expense_date >= start_date)

    if end_date is not None:
        filters.append(Expense.expense_date <= end_date)

    return db.query(Expense).filter(
        and_(*filters)
    ).all()
