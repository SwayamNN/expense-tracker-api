
from sqlalchemy.orm import Session
from app.models import Category
from app.schemas.category import CategoryCreate


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.model_dump())

    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    except Exception:
        db.rollback()
        raise


def get_category(db: Session, category_id: int):
    return db.query(Category).filter(
        Category.category_id == category_id
    ).first()


def get_categories(db: Session, user_id: int):
    return db.query(Category).filter(
        Category.user_id == user_id
    ).all()


def update_category(db: Session, category_id: int, category_data: CategoryCreate):
    category = get_category(db, category_id)

    if category is None:
        return None

    try:
        category.name = category_data.name
        category.description = category_data.description

        db.commit()
        db.refresh(category)
        return category

    except Exception:
        db.rollback()
        raise


def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id)

    if category is None:
        return None

    try:
        db.delete(category)
        db.commit()
        return category

    except Exception:
        db.rollback()
        raise
