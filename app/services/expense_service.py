
from sqlalchemy.orm import Session
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.crud import expense_crud, user_crud, category_crud
from app.schemas.expense import ExpenseCreate
from datetime import datetime
from decimal import Decimal

def create_expense_service(db: Session, expense: ExpenseCreate):
    # 1. Check whether the user exists
    user = user_crud.get_user(db, expense.user_id)

    if user is None:
        raise ValueError("User not found")

    # 2. Check whether the category exists
    category = category_crud.get_category(db, expense.category_id)

    if category is None:
        raise ValueError("Category not found")

    # 3. Check category ownership
    if category.user_id != expense.user_id:
        raise ValueError("Category does not belong to this user")

    # 4. Create expense
    return expense_crud.create_expense(db, expense)


def get_expense_service(db: Session, expense_id: int, user_id: int):
    expense = expense_crud.get_expense(db, expense_id)

    if expense is None or expense.user_id != user_id:
        raise ValueError("Expense not found")

    return expense


def get_user_expenses_service(db: Session, user_id: int):
    user = user_crud.get_user(db, user_id)

    if user is None:
        raise ValueError("User not found")

    return expense_crud.get_user_expenses(db, user_id)


def update_expense_service(
    db: Session,
    expense_id: int,
    user_id: int,
    expense_data: ExpenseCreate
):
    expense = get_expense_service(db, expense_id, user_id)

    # Validate the new category
    category = category_crud.get_category(db, expense_data.category_id)

    if category is None or category.user_id != user_id:
        raise ValueError("Invalid category for this user")

    # Prevent changing expense ownership
    if expense_data.user_id != user_id:
        raise ValueError("Cannot change expense owner")

    return expense_crud.update_expense(db, expense_id, expense_data)


def delete_expense_service(db: Session, expense_id: int, user_id: int):
    expense = get_expense_service(db, expense_id, user_id)

    return expense_crud.delete_expense(db, expense.expense_id)


def filter_expenses_service(
    db: Session,
    user_id: int,
    category_id: int | None = None,
    min_amount: Decimal | None = None,
    max_amount: Decimal | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None
):
    user = user_crud.get_user(db, user_id)

    if user is None:
        raise ValueError("User not found")

    if min_amount is not None and max_amount is not None:
        if min_amount > max_amount:
            raise ValueError(
                "Minimum amount cannot exceed maximum amount"
            )

    return expense_crud.filter_expenses(
        db=db,
        user_id=user_id,
        category_id=category_id,
        min_amount=min_amount,
        max_amount=max_amount,
        start_date=start_date,
        end_date=end_date
    )


def partial_update_expense_service(
    db: Session,
    expense_id: int,
    user_id: int,
    expense_data: ExpenseUpdate
):
    expense = get_expense_service(db, expense_id, user_id)

    update_data = expense_data.model_dump(exclude_unset=True)

    if "category_id" in update_data:
        category = category_crud.get_category(
            db, update_data["category_id"]
        )

        if category is None or category.user_id != user_id:
            raise ValueError("Invalid category for this user")

    for key, value in update_data.items():
        setattr(expense, key, value)

    try:
        db.commit()
        db.refresh(expense)
        return expense
    except Exception:
        db.rollback()
        raise
