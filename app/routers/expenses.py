from datetime import datetime
from decimal import Decimal
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.services import expense_service
from app.crud import expense_crud , user_crud

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


@router.post(
    "/",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
):
    try:
        return expense_service.create_expense_service(db, expense)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/", response_model=list[ExpenseResponse])
def get_user_expenses(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        return expense_service.get_user_expenses_service(db, user_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get("/filter/", response_model=list[ExpenseResponse])
def filter_expenses(
    user_id: int,
    category_id: int | None = None,
    min_amount: Decimal | None = None,
    max_amount: Decimal | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    db: Session = Depends(get_db)
):
    try:
        return expense_service.filter_expenses_service(
            db=db,
            user_id=user_id,
            category_id=category_id,
            min_amount=min_amount,
            max_amount=max_amount,
            start_date=start_date,
            end_date=end_date
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )



@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        return expense_service.get_expense_service(
            db, expense_id, user_id
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    user_id: int,
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db)
):
    try:
        return expense_service.update_expense_service(
            db, expense_id, user_id, expense_data
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.patch("/{expense_id}", response_model=ExpenseResponse)
def partial_update_expense(
    expense_id: int,
    user_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db)
):
    try:
        return expense_service.partial_update_expense_service(
            db=db,
            expense_id=expense_id,
            user_id=user_id,
            expense_data=expense_data
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))



@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        expense_service.delete_expense_service(
            db, expense_id, user_id
        )
        return {"message": "Expense deleted successfully"}
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))



from datetime import datetime
from decimal import Decimal


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
            raise ValueError("Minimum amount cannot exceed maximum amount")

    return expense_crud.filter_expenses(
        db=db,
        user_id=user_id,
        category_id=category_id,
        min_amount=min_amount,
        max_amount=max_amount,
        start_date=start_date,
        end_date=end_date
    )
