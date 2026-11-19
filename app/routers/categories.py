from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services import category_service

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    try:
        return category_service.create_category_service(db, category)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        return category_service.get_category_service(
            db, category_id, user_id
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.get("/", response_model=list[CategoryResponse])
def get_categories(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        return category_service.get_categories_service(db, user_id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        category_service.delete_category_service(
            db, category_id, user_id
        )
        return {"message": "Category deleted successfully"}
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )