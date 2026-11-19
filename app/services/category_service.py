
from sqlalchemy.orm import Session

from app.crud import category_crud, user_crud
from app.schemas.category import CategoryCreate


def create_category_service(db: Session, category: CategoryCreate):
    # Check whether the user exists
    user = user_crud.get_user(db, category.user_id)

    if user is None:
        raise ValueError("User not found")

    return category_crud.create_category(db, category)


def get_category_service(db: Session, category_id: int, user_id: int):
    category = category_crud.get_category(db, category_id)

    if category is None or category.user_id != user_id:
        raise ValueError("Category not found")

    return category


def get_categories_service(db: Session, user_id: int):
    user = user_crud.get_user(db, user_id)

    if user is None:
        raise ValueError("User not found")

    return category_crud.get_categories(db, user_id)


def delete_category_service(db: Session, category_id: int, user_id: int):
    category = get_category_service(db, category_id, user_id)

    return category_crud.delete_category(db, category.category_id)
