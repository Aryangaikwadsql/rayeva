"""Module 3: AI Impact Reporting Generator."""
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.ai.client import generate
from app.db.models.product import Product
from app.db.models.proposal import Proposal

IMPACT_FACTORS = {
    "plastic_saved_kg": 0.5,  # per product avg
    "carbon_avoided_kg": 2.0,
    "local_jobs": 0.1
}

def generate_impact(product_id: int = None, proposal_id: int = None, db: Session = None) -> Dict[str, Any]:
    """Generate impact report from DB data."""
    base_impact = {
        "plastic_saved": 0,
        "carbon_avoided": 0,
        "local_impact": "Supports regional artisans"
    }
    
    if db:
        if product_id:
            product = db.query(Product).filter(Product.id == product_id).first()
            if product:
                base_impact["plastic_saved"] = len(product.tags or []) * IMPACT_FACTORS["plastic_saved_kg"]
                base_impact["carbon_avoided"] = IMPACT_FACTORS["carbon_avoided_kg"]
        
        if proposal_id:
            proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
            if proposal:
                products_count = len(proposal.products or [])
                base_impact["plastic_saved"] += products_count * IMPACT_FACTORS["plastic_saved_kg"] * 10
                base_impact["carbon_avoided"] += products_count * IMPACT_FACTORS["carbon_avoided_kg"] * 10
    
    prompt = f"""
    Generate human-readable impact statement from data:
    Plastic saved: {base_impact['plastic_saved']}kg
    Carbon avoided: {base_impact['carbon_avoided']}kg CO2e
    Local impact: {base_impact['local_impact']}
    
    Output JSON: {{"plastic_saved": float, "carbon_avoided": float, "local_impact": str, "summary": str}}
    Make persuasive for sustainability report.
    """
    
    result = generate(
        model_provider="openai",
        model="gpt-4o-mini",
        prompt=prompt,
        response_model=None
    )
    
    # Ensure consistent structure even if mock/content mismatch
    impact_data = {**base_impact, **(result.get("content") or {})}
    # Fill defaults if missing
    impact_data.setdefault("plastic_saved", base_impact.get("plastic_saved", 0.0))
    impact_data.setdefault("carbon_avoided", base_impact.get("carbon_avoided", 0.0))
    impact_data.setdefault("local_impact", base_impact.get("local_impact", "Supports regional artisans"))
    impact_data.setdefault("summary", "Generated sustainability impact report.")
    return {"success": True, "impact": impact_data}
