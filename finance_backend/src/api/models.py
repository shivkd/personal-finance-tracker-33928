"""
SQLAlchemy ORM models for personal finance tracker.
Includes User, Transaction, Category, Budget, Audit, and receipt handling.
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Enum, Boolean, func
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class User(Base):
    """
    Users of the finance tracker.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    disabled = Column(Boolean, default=False)

    transactions = relationship("Transaction", back_populates="user")
    budgets = relationship("Budget", back_populates="user")
    audits = relationship("Audit", back_populates="user")


class Category(Base):
    """
    Categories for classifying transactions.
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")
    transactions = relationship("Transaction", back_populates="category")


class Transaction(Base):
    """
    Stateful record of money movement (income/expense).
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    receipt_url = Column(String, nullable=True)
    type = Column(Enum("income", "expense", name="transaction_type"), nullable=False)

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")


class Budget(Base):
    """
    Monthly/periodic budget.
    """
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="budgets")
    category = relationship("Category")


class Audit(Base):
    """
    Audit log of actions.
    """
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)
    action = Column(String, nullable=False)
    entity = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=True)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, server_default=func.now())
    user = relationship("User", back_populates="audits")
