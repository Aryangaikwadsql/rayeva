"""Impact model."""
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Impact(Base):
    __tablename__ = "impacts"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    proposal_id = Column(Integer, ForeignKey("proposals.id"))
    plastic_saved = Column(Float)
    carbon_avoided = Column(Float)
    local_impact = Column(String)
    summary = Column(String)
    created_at = Column(DateTime, server_default=func.now())

