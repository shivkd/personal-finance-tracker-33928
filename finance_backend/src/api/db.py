"""
SQLAlchemy session/engine configuration and helpers.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import get_supabase_database_url
from .models import Base

DB_URL = get_supabase_database_url()

engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize tables. Should be called once (e.g., for development)."""
    Base.metadata.create_all(bind=engine)

# PUBLIC_INTERFACE
def get_db():
    """FastAPI dependency for providing a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
