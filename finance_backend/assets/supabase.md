# Supabase Integration for Personal Finance FastAPI Backend

This backend integrates with Supabase for authentication and as a PostgreSQL database.

## Environment Variables

Set the following variables in your `.env` file:
- `SUPABASE_URL=<your_supabase_url>`
- `SUPABASE_KEY=<your_supabase_api_key>`
- `SUPABASE_DB_URL=<your_supabase_postgres_connection_url>` (optional, or use `SUPABASE_URL` if compatible)

## Database Connection

- The FastAPI backend uses SQLAlchemy to connect directly to the Supabase PostgreSQL instance for all data models (User, Transactions, Budget, etc).
- The connection string is loaded via `SUPABASE_DB_URL` or `SUPABASE_URL` from environment.

## Recommended Setup

1. Copy the PostgreSQL connection string from Supabase project dashboard.
2. Add all keys to your backend `.env` file.
3. On app start, tables are auto-created in Supabase (development only).

## Security

- Keep your Supabase Key secure and never commit it to public repos.
- JWT auth tokens are signed locally by backend, not managed by Supabase.

## Code Reference

- See `src/api/config.py` and `src/api/db.py` for integration details.
