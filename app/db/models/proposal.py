"""Proposal model enhanced for Module 4 WhatsApp orders."""
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from enum import Enum as PyEnum

from app.db.base import Base

class OrderStatus(PyEnum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    RETURNED = "RETURNED"

class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    client_needs = Column(String, nullable=False)
    budget = Column(Float, nullable=False)
    products = Column(JSON)
    budget_alloc = Column(JSON)
    cost_breakdown = Column(JSON)
    impact_summary = Column(String)
    customer_phone = Column(String, nullable=True, index=True)  # For WhatsApp user lookup
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
