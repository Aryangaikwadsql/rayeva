"""FastAPI main app."""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.config import get_settings
from app.schemas.product import ProductCreate, ProductResponse
from app.schemas.proposal import ProposalCreate, ProposalResponse
from app.schemas.impact import ImpactCreate, ImpactResponse
from app.ai.modules.module1 import generate_category
from app.ai.modules.module2 import generate_proposal
from app.ai.modules.module3 import generate_impact
from app.ai.modules.module4 import handle_whatsapp_query
from app.crud.product import create_product, log_ai
from app.crud.proposal import create_proposal
from app.crud.impact import create_impact

app = FastAPI(title="Rayeva AI Systems")

settings = get_settings()


@app.on_event("startup")
def create_tables():
    from app.db.base import Base, engine
    from app.db.models import Product, Proposal, Log, Impact
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"msg": "Rayeva AI Systems ready"}


@app.post("/ai/category", response_model=ProductResponse)
def ai_category(product: ProductCreate, db: Session = Depends(get_db)):
    """Module 1 endpoint."""
    try:
        result = generate_category(product.product_desc)
        if not result.get("success"):
            raise HTTPException(500, f"AI failed: {result.get('raw', result)}")
        
        ai_data = result.get("content", result.get("data", {}))
        db_product = create_product(db, product, ai_data)  # Pass AI data
        
        log_ai(db, "module1", product.product_desc, str(result), {"ai_data": ai_data})
        db.commit()
        db.refresh(db_product)
        return ProductResponse(
            id=db_product.id,
            product_desc=db_product.product_desc,
            primary_category=db_product.primary_category,
            sub_category=db_product.sub_category,
            tags=db_product.tags,
            sustainability=db_product.sustainability,
            created_at=str(db_product.created_at)
        )
    except Exception as e:
        raise HTTPException(400, str(e))


@app.post("/ai/proposal", response_model=ProposalResponse)
def ai_proposal(proposal: ProposalCreate, db: Session = Depends(get_db)):
    """Module 2 endpoint."""
    try:
        result = generate_proposal(proposal.client_needs, proposal.budget)
        if not result.get("success"):
            raise HTTPException(500, "AI generation failed")
        
        ai_data = result.get("content", result.get("data", {}))
        db_proposal = create_proposal(db, proposal, ai_data)
        log_ai(db, "module2", str(proposal), str(result), {"result": ai_data})
        
        db.commit()
        db.refresh(db_proposal)
        return ProposalResponse(
            id=db_proposal.id,
            client_needs=db_proposal.client_needs,
            budget=db_proposal.budget,
            products=db_proposal.products,
            budget_alloc=db_proposal.budget_alloc,
            cost_breakdown=db_proposal.cost_breakdown,
            impact_summary=db_proposal.impact_summary,
            created_at=str(db_proposal.created_at)
        )
    except Exception as e:
        raise HTTPException(400, str(e))

@app.post("/ai/impact", response_model=ImpactResponse)
def ai_impact(impact_request: ImpactCreate, db: Session = Depends(get_db)):
    try:
        result = generate_impact(impact_request.product_id, impact_request.proposal_id, db)
        if not result.get("success"):
            raise HTTPException(500, f"Impact generation failed: {result.get('error', 'Unknown')}")
        impact_data = result["impact"]
        db_impact = create_impact(db, impact_request, impact_data)
        return ImpactResponse(**impact_data, created_at=str(db_impact.created_at))
    except KeyError as e:
        raise HTTPException(500, f"Invalid impact data structure: {str(e)}")
    except Exception as e:
        raise HTTPException(500, f"Impact endpoint error: {str(e)}")

@app.post("/ai/whatsapp")
def ai_whatsapp(message: str, phone: str, db: Session = Depends(get_db)):
    """Module 4: AI WhatsApp Support Bot - 1.Order status DB, 2.Returns, 3.Escalate refunds, 4.Log."""
    try:
        result = handle_whatsapp_query(message, phone, db)
        return result
    except Exception as e:
        return {"success": False, "response": f"Support temporarily unavailable. Reply HELP. ({str(e)})", "escalate": True}
