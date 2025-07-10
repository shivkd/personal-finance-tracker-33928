from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.api.db as db  # Absolute import for db
from src.api.routers_auth import router as auth_router  # Absolute import for auth_router
from src.api.routers_main import router as api_router  # Absolute import for api_router

tags_metadata = [
    {"name": "auth", "description": "User authentication and JWT."},
    {"name": "api", "description": "Main data API: categories, transactions, dashboard, budgets, audit, notifications."},
]

app = FastAPI(
    title="Personal Finance Tracker API",
    description="Backend API for user auth, transactions, budgets, and dashboard.",
    version="0.1.0",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(api_router)

@app.get("/", tags=["root"])
def health_check():
    """Health check to see if service is running."""
    return {"message": "Healthy"}

@app.on_event("startup")
def on_startup():
    db.init_db()
