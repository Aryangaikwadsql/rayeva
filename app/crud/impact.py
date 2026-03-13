"""Impact CRUD."""
from sqlalchemy.orm import Session
from app.db.models.impact import Impact
from app.schemas.impact import ImpactCreate

def create_impact(db: Session, obj_in: ImpactCreate, data: dict):
    impact_data = obj_in.dict()
    impact_data.update(data)
    # Validate required fields with defaults
    impact_data.setdefault("plastic_saved", 0.0)
    impact_data.setdefault("carbon_avoided", 0.0)
    impact_data.setdefault("local_impact", "No impact data available")
    impact_data.setdefault("summary", "Impact report generated")
    db_obj = Impact(**impact_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

