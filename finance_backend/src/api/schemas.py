"""
Pydantic models for FastAPI request validation and response serialization.
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# ---------- USER ----------
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(UserBase):
    id: int
    full_name: Optional[str] = None
    created_at: datetime
    disabled: bool

    class Config:
        orm_mode = True

# ---------- CATEGORY ----------
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int

    class Config:
        orm_mode = True

# ---------- TRANSACTION ----------
class TransactionBase(BaseModel):
    amount: float
    description: Optional[str]
    category_id: Optional[int]
    date: Optional[datetime]
    receipt_url: Optional[str]
    type: str = Field(..., pattern="^(income|expense)$", description="Transaction type: income or expense")

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: int

    class Config:
        orm_mode = True

# ---------- BUDGET ----------
class BudgetBase(BaseModel):
    name: str
    amount: float
    category_id: Optional[int]
    start_date: datetime
    end_date: datetime

class BudgetCreate(BudgetBase):
    pass

class BudgetRead(BudgetBase):
    id: int

    class Config:
        orm_mode = True

# ---------- AUDIT ----------
class AuditRead(BaseModel):
    id: int
    user_id: Optional[int]
    action: str
    entity: str
    entity_id: Optional[int]
    details: Optional[str]
    timestamp: datetime

    class Config:
        orm_mode = True

# ---------- DASHBOARD RESPONSES ----------
class DashboardSummary(BaseModel):
    balance: float
    expense_total: float
    income_total: float
    budgets_progress: List[dict]
    recent_transactions: List[TransactionRead]
