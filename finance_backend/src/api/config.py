"""
Configuration and setup utilities for FastAPI app.
Handles environment loading, DB URL extraction, and JWT constants.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# PUBLIC_INTERFACE
def get_supabase_database_url():
    """
    Returns the PostgreSQL database URL configured for Supabase.
    Reads from the SUPABASE_URL or DATABASE_URL environment variable.
    """
    url = os.getenv("SUPABASE_DB_URL") or os.getenv("SUPABASE_URL") or os.getenv("DATABASE_URL")
    assert url, (
        "SUPABASE_DB_URL, SUPABASE_URL, or DATABASE_URL must be set in environment."
        " Refer to Supabase connection settings."
    )
    # For SQLAlchemy, ensure correct prefix if needed
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url

# JWT settings
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60 * 24 * 7  # Token valid for 1 week

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
