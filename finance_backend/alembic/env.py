import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from dotenv import load_dotenv
from pathlib import Path
import sys

# Include app in sys.path for `import src.api.models`
sys.path.append(str(Path(__file__).resolve().parents[1] / "src" / "api"))

# Load environment if needed
load_dotenv(dotenv_path=str(Path(__file__).resolve().parents[2] / ".env"), override=True)

# Alembic Config object, works both online and offline mode
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Import your models here for Alembic's 'autogenerate' support
from models import Base

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = os.getenv("SUPABASE_DB_URL") or os.getenv("SUPABASE_URL") or config.get_main_option("sqlalchemy.url")
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    url = os.getenv("SUPABASE_DB_URL") or os.getenv("SUPABASE_URL") or configuration.get("sqlalchemy.url")
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    configuration["sqlalchemy.url"] = url
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
