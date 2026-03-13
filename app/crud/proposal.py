"""CRUD for Proposal (orders for Module 4)."""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional, Dict, Any

from app.schemas.proposal import ProposalCreate
from app.db.models.proposal import Proposal

def get_proposal(db: Session, skip: int = 0, limit: int = 100) -> List[Proposal]:
    return db.query(Proposal).offset(skip).limit(limit).all()

def get_proposal_by_id(db: Session, proposal_id: int) -> Optional[Proposal]:
    return db.query(Proposal).filter(Proposal.id == proposal_id).first()

def get_orders_by_phone(db: Session, phone: str, limit: int = 5) -> List[Proposal]:
    """Get latest orders by customer phone for WhatsApp."""
    return db.query(Proposal).filter(
        Proposal.customer_phone == phone
    ).order_by(desc(Proposal.created_at)).limit(limit).all()

def create_proposal(db: Session, obj_in: ProposalCreate, ai_data: Dict[str, Any] = None) -> Proposal:
    db_proposal = Proposal(**obj_in.dict(exclude_unset=True))
    if ai_data:
        db_proposal.products = ai_data.get('products')
        db_proposal.budget_alloc = ai_data.get('budget_alloc')
        db_proposal.cost_breakdown = ai_data.get('cost_breakdown')
        db_proposal.impact_summary = ai_data.get('impact_summary')
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal

def update_order_status(db: Session, proposal_id: int, status: str) -> Optional[Proposal]:
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if proposal:
        proposal.status = status
        db.commit()
        db.refresh(proposal)
    return proposal

