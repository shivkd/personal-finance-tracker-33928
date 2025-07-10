"""
Routes for authentication: register and login with JWT.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any

import src.api.models as models
import src.api.schemas as schemas
import src.api.auth as auth
from src.api.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

# PUBLIC_INTERFACE
@router.post("/register", response_model=schemas.UserRead)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)) -> Any:
    """Register a new user with email and password."""
    existing = db.query(models.User).filter_by(email=user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = auth.hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# PUBLIC_INTERFACE
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user, return a JWT token and user info.
    """
    user = db.query(models.User).filter_by(email=form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password) or user.disabled:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer", "user": schemas.UserRead.from_orm(user)}
