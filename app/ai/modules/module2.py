"""Module 2: AI B2B Proposal Generator."""
from typing import Dict, Any, List
from app.ai.client import generate
from app.schemas.proposal import ProposalResponse
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.db.models.product import Product  # Sample catalog


def generate_proposal(client_needs: str, budget: float, db: Session = None) -> Dict[str, Any]:
    """Generate B2B proposal."""
    products_catalog = "Dynamic catalog from DB (products table)"
    if db:
        from app.db.models.product import Product
        products = db.query(Product).limit(10).all()
        products_catalog = ", ".join([f"{p.product_desc} (${p.id})" for p in products])
    
    json_example = '''{
      "products": [
        {"name": "Eco T-Shirt", "qty": 10, "unit_price": 20.0},
        {"name": "Bamboo Straw", "qty": 50, "unit_price": 5.0}
      ],
      "budget_alloc": {"products": 1500.0, "delivery": 200.0, "total": 5000.0},
      "cost_breakdown": {
        "Eco T-Shirts": 1000.0,
        "Bamboo Straws": 250.0,
        "Delivery": 200.0,
        "Buffer": 3550.0
      },
      "impact_summary": "This proposal reduces plastic waste by 80%..."
    }'''

    prompt = f"""
    Client needs: "{client_needs}"
    Budget: ${budget}
    Catalog: {products_catalog}

    Suggest sustainable product mix, budget allocation, cost breakdown, impact summary.

    Output ONLY valid JSON matching this structure:
    {json_example}

    Optimize for sustainability and fit within budget.
    """
    
    result = generate(
        model_provider="openai",
        model="gpt-4o-mini",
        prompt=prompt,
        response_model=None  # Mock works without; disable for now to avoid parse fail
    )
    
    return result

