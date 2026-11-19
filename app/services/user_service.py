
from sqlalchemy.orm import Session

from app.crud import user_crud
from app.schemas.user import UserCreate


def create_user_service(db: Session, user: UserCreate):
    existing_user = user_crud.get_user_by_email(db, user.email)

    if existing_user:
        raise ValueError("Email already registered")

    return user_crud.create_user(db, user)


def get_user_service(db: Session, user_id: int):
    user = user_crud.get_user(db, user_id)

    if user is None:
        raise ValueError("User not found")

    return user


def get_users_service(db: Session, skip: int = 0, limit: int = 10):
    return user_crud.get_users(db, skip, limit)
