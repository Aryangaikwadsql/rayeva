"""Impact schemas."""
from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class ImpactCreate(BaseModel):
    product_id: int | None = None
    proposal_id: int | None = None

class ImpactResponse(BaseModel):
    plastic_saved: float
    carbon_avoided: float
    local_impact: str
    summary: str
    created_at: str = str(datetime.now())

    class Config:
        from_attributes = True

