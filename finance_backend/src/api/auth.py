"""
Authentication/authorization helpers for FastAPI backend.
Handles password hashing, JWT encode/decode, dependency for current user, and security.
"""
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import src.api.models as models
import src.api.config as config
from src.api.db import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# PUBLIC_INTERFACE
def verify_password(plain_password, hashed_password):
    """Verify a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

# PUBLIC_INTERFACE
def hash_password(password):
    """Hash a password for storing in db."""
    return pwd_context.hash(password)

# PUBLIC_INTERFACE
def create_access_token(data: dict, expires_delta: timedelta = None):
    """Generate a JWT access token with expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=config.JWT_EXPIRATION_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt

# PUBLIC_INTERFACE
def decode_access_token(token: str):
    """Decode a JWT access token and return the payload if valid."""
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

# PUBLIC_INTERFACE
def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
    ) -> models.User:
    """FastAPI dependency to get user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not authenticate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == payload["sub"]).first()
    if not user or user.disabled:
        raise credentials_exception
    return user
