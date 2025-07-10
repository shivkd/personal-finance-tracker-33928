"""Initial tables for User, Category, Transaction, Budget, Audit

Revision ID: 0001
Revises: 
Create Date: 2024-07-01 00:00:00

"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('email', sa.String, unique=True, nullable=False, index=True),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('full_name', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('disabled', sa.Boolean, default=False)
    )
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    )
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), index=True, nullable=False),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('category_id', sa.Integer, sa.ForeignKey('categories.id'), nullable=True),
        sa.Column('date', sa.DateTime, nullable=False),
        sa.Column('receipt_url', sa.String, nullable=True),
        sa.Column('type', sa.Enum('income', 'expense', name='transaction_type'), nullable=False)
    )
    op.create_table(
        'budgets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), index=True, nullable=False),
        sa.Column('category_id', sa.Integer, sa.ForeignKey('categories.id'), nullable=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('start_date', sa.DateTime, nullable=False),
        sa.Column('end_date', sa.DateTime, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )
    op.create_table(
        'audits',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), index=True, nullable=True),
        sa.Column('action', sa.String, nullable=False),
        sa.Column('entity', sa.String, nullable=False),
        sa.Column('entity_id', sa.Integer, nullable=True),
        sa.Column('details', sa.Text, nullable=True),
        sa.Column('timestamp', sa.DateTime, server_default=sa.func.now())
    )


def downgrade():
    op.drop_table('audits')
    op.drop_table('budgets')
    op.drop_table('transactions')
    op.drop_table('categories')
    op.drop_table('users')
    op.execute("DROP TYPE IF EXISTS transaction_type")
