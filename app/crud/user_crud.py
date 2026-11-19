
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.user import UserCreate


def create_user(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        email=user.email
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except Exception:
        db.rollback()
        raise


def get_user(db: Session, user_id: int):
    return db.query(User).filter(
        User.user_id == user_id
    ).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(
        User.email == email
    ).first()


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)

    if user is None:
        return None

    try:
        db.delete(user)
        db.commit()
        return user

    except Exception:
        db.rollback()
        raise
