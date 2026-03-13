"""Pydantic schemas for Proposal (enhanced for Module 4)."""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    RETURNED = "RETURNED"


class ProposalCreate(BaseModel):
    client_needs: str
    budget: float
    customer_phone: Optional[str] = None

class ProposalResponse(BaseModel):
    id: int
    client_needs: str
    budget: float
    products: Optional[List[Dict[str, Any]]] = None
    budget_alloc: Optional[Dict[str, float]] = None
    cost_breakdown: Optional[Dict[str, float]] = None
    impact_summary: Optional[str] = None
    customer_phone: Optional[str] = None
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime

    class Config:
        from_attributes = True

