"""
Main API routers: categories, transactions, budget, dashboard, audit.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import shutil, os
from datetime import datetime

from . import models, schemas, auth
from .db import get_db

router = APIRouter(prefix="/api", tags=["api"])

#### CATEGORIES ####

@router.post("/categories/", response_model=schemas.CategoryRead)
def create_category(cat: schemas.CategoryCreate, db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    existing = db.query(models.Category).filter_by(name=cat.name, user_id=user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    new_cat = models.Category(name=cat.name, user_id=user.id)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat

@router.get("/categories/", response_model=List[schemas.CategoryRead])
def list_categories(db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Category).filter_by(user_id=user.id).all()

@router.delete("/categories/{cat_id}")
def delete_category(cat_id: int, db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    cat = db.query(models.Category).filter_by(id=cat_id, user_id=user.id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(cat)
    db.commit()
    return {"ok": True}

#### TRANSACTIONS ####

@router.post("/transactions/", response_model=schemas.TransactionRead)
def add_transaction(tran: schemas.TransactionCreate, db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    category = None
    if tran.category_id:
        category = db.query(models.Category).filter_by(id=tran.category_id, user_id=user.id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Invalid category for user")
    db_tran = models.Transaction(
        user_id=user.id,
        amount=tran.amount,
        description=tran.description,
        category_id=tran.category_id,
        date=tran.date or datetime.utcnow(),
        receipt_url=tran.receipt_url,
        type=tran.type,
    )
    db.add(db_tran)
    db.commit()
    db.refresh(db_tran)
    return db_tran

@router.get("/transactions/", response_model=List[schemas.TransactionRead])
def list_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Transaction).filter_by(user_id=user.id).order_by(models.Transaction.date.desc()).offset(skip).limit(limit).all()

@router.get("/transactions/{tran_id}", response_model=schemas.TransactionRead)
def get_transaction(tran_id: int, db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    t = db.query(models.Transaction).filter_by(id=tran_id, user_id=user.id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return t

@router.put("/transactions/{tran_id}", response_model=schemas.TransactionRead)
def update_transaction(tran_id: int, tran: schemas.TransactionCreate, db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    db_tran = db.query(models.Transaction).filter_by(id=tran_id, user_id=user.id).first()
    if not db_tran:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for attr, value in tran.dict().items():
        setattr(db_tran, attr, value)
    db.commit()
    db.refresh(db_tran)
    return db_tran

@router.delete("/transactions/{tran_id}")
def delete_transaction(tran_id: int, db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    db_tran = db.query(models.Transaction).filter_by(id=tran_id, user_id=user.id).first()
    if not db_tran:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(db_tran)
    db.commit()
    return {"ok": True}

@router.post("/transactions/{tran_id}/receipt")
def upload_receipt(tran_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    db_tran = db.query(models.Transaction).filter_by(id=tran_id, user_id=user.id).first()
    if not db_tran:
        raise HTTPException(status_code=404, detail="Transaction not found")
    upload_dir = "uploaded_receipts"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{user.id}_{tran_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    db_tran.receipt_url = file_path
    db.commit()
    db.refresh(db_tran)
    return {"receipt_url": file_path}

#### BUDGETS ####

@router.post("/budgets/", response_model=schemas.BudgetRead)
def create_budget(budget: schemas.BudgetCreate, db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    db_budget = models.Budget(**budget.dict(), user_id=user.id)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

@router.get("/budgets/", response_model=List[schemas.BudgetRead])
def list_budgets(db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Budget).filter_by(user_id=user.id).all()

@router.delete("/budgets/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    b = db.query(models.Budget).filter_by(id=budget_id, user_id=user.id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Budget not found")
    db.delete(b)
    db.commit()
    return {"ok": True}

#### DASHBOARD SUMMARY ####

@router.get("/dashboard", response_model=schemas.DashboardSummary)
def dashboard(db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    transactions = db.query(models.Transaction).filter_by(user_id=user.id).all()
    income = sum(t.amount for t in transactions if t.type == "income")
    expense = sum(t.amount for t in transactions if t.type == "expense")
    balance = income - expense
    budgets = db.query(models.Budget).filter_by(user_id=user.id).all()
    # Budget progress
    prog = []
    for b in budgets:
        tx_query = db.query(models.Transaction).filter(
            models.Transaction.user_id == user.id,
            models.Transaction.date >= b.start_date,
            models.Transaction.date <= b.end_date,
            models.Transaction.type == "expense"
        )
        if b.category_id:
            tx_query = tx_query.filter(models.Transaction.category_id == b.category_id)
        period_tx = tx_query.all()
        spent = sum(t.amount for t in period_tx)
        percent = spent / b.amount * 100 if b.amount else 0
        prog.append({
            "budget_id": b.id,
            "name": b.name,
            "spent": spent,
            "max": b.amount,
            "percent_spent": percent,
            "over_budget": spent > b.amount,
        })
    recent = sorted(transactions, key=lambda t: t.date, reverse=True)[:5]
    return schemas.DashboardSummary(
        balance=balance,
        expense_total=expense,
        income_total=income,
        budgets_progress=prog,
        recent_transactions=recent
    )

#### AUDIT (stub for extension) ####

@router.get("/audits/", response_model=List[schemas.AuditRead])
def list_audits(db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Audit).filter_by(user_id=user.id).order_by(models.Audit.timestamp.desc()).all()

#### NOTIFICATIONS (stub) ####

@router.get("/notifications")
def notifications():
    """Stub notifications endpoint."""
    return []
