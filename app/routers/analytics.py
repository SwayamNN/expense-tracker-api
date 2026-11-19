from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import analytics_service
from app.crud import user_crud

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/total/{user_id}")
def total_expenses(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = user_crud.get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    total = analytics_service.get_total_expenses(db, user_id)

    return {
        "user_id": user_id,
        "total_expenses": total
    }


@router.get("/monthly/{user_id}")
def monthly_expenses(
    user_id: int,
    year: int,
    db: Session = Depends(get_db)
):
    user = user_crud.get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    results = analytics_service.get_monthly_expenses(
        db, user_id, year
    )

    return [
        {
            "month": int(row.month),
            "total": row.total
        }
        for row in results
    ]


@router.get("/category/{user_id}")
def category_expenses(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = user_crud.get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    results = analytics_service.get_category_expenses(db, user_id)

    return [
        {
            "category_id": row.category_id,
            "total": row.total
        }
        for row in results
    ]