
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from decimal import Decimal


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    description: str | None = None
    expense_date: datetime
    user_id: int = Field(gt=0)
    category_id: int = Field(gt=0)



class ExpenseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=150)
    amount: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=2
    )
    description: str | None = None
    expense_date: datetime | None = None
    category_id: int | None = Field(default=None, gt=0)


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    expense_id: int
    title: str
    amount: Decimal
    description: str | None
    expense_date: datetime
    user_id: int
    category_id: int
    created_at: datetime
    updated_at: datetime | None
