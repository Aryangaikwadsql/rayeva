"""AI client wrapper for OpenAI/Groq."""
import json
from typing import Dict, Any, Optional, Literal
import httpx

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from pydantic import BaseModel

from app.core.config import get_settings


settings = get_settings()

client_map = {
        "openai": OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None,
        "openrouter": OpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        ) if settings.OPENROUTER_API_KEY else None,
        "groq": None  # Import groq if needed
    }
if settings.OPENAI_API_KEY:
    client_map

class StructuredOutput(BaseModel):
    """Base for structured JSON."""
    pass


def generate(
    model_provider: Literal["openai", "openrouter", "groq"],
    model: str,
    prompt: str,
    system_prompt: str = "You are a helpful AI for sustainable commerce.",
    max_tokens: int = 1000,
    temperature: float = 0.1,
    response_model: Optional[type[StructuredOutput]] = None,
) -> Dict[str, Any]:
    """Generate response with structured output."""
    # Auto-select client with fallback/mock
    client = None
    used_provider = None
    
    # Select best available client
    for provider, client in client_map.items():
        if client:
            used_provider = provider
            break
    
    if settings.GROQ_API_KEY and 'groq' not in client_map:
        try:
            from groq import Groq
            client_map['groq'] = Groq(api_key=settings.GROQ_API_KEY)
            client = client_map['groq']
            used_provider = 'groq'
        except ImportError:
            pass
    
    if client is None:
        # Dynamic mock based on prompt/model
        if 'category' in prompt.lower() or 'tag' in prompt.lower():
            mock_data = {
                "primary_category": "Beauty & Personal Care",
                "sub_category": "Oral Care", 
                "tags": ["eco-friendly", "sustainable", "bamboo"],
                "sustainability": [{"name": "plastic-free", "confidence": 0.95}]
            }
        elif 'proposal' in prompt.lower() or 'budget' in prompt.lower():
            mock_data = {
                "products": [
                    {"name": "Eco Notebooks", "qty": 100, "unit_price": 8.5},
                    {"name": "Bamboo Pens", "qty": 300, "unit_price": 1.8}
                ],
                "budget_alloc": {"products": 2200, "delivery": 300, "total": 5000},
                "cost_breakdown": {"Notebooks": 850, "Pens": 540, "Delivery": 300, "Buffer": 3310},
                "impact_summary": "80% waste reduction, carbon neutral supply chain."
            }
        elif 'impact' in prompt.lower() or 'plastic_saved' in prompt.lower() or 'carbon_avoided' in prompt.lower():
            mock_data = {
                "plastic_saved": 500.0,
                "carbon_avoided": 2000.0,
                "local_impact": "Supports 50 local artisan jobs and community development",
                "summary": "This initiative diverts 500kg of plastic from landfills, avoids 2 tons CO2e emissions, and creates sustainable local employment opportunities."
            }
        else:
            mock_data = {"message": "Sustainable commerce recommendation"}
        return {"success": True, "content": mock_data, "provider": "mock"}
    
    if client is None:
        raise ValueError("No API keys available")
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
    except Exception as e:
        return {"success": False, "error": str(e), "provider": used_provider}
    content = response.choices[0].message.content
    
    if response_model:
        # Parse JSON from content
        try:
            parsed = response_model.model_validate_json(content)
            return {"success": True, "data": parsed.model_dump()}
        except:
            return {"success": False, "raw": content}
    
    return {"success": True, "content": content}


def log_ai_call(module: str, prompt: str, response: str, metadata: Dict[str, Any], db=None):
    """Log to DB - call from endpoint."""
    if db:
        from app.crud.product import log_ai
        log_ai(db, module, prompt, response, metadata)
    print(f"AI LOG {module}: {metadata}")  # Fallback

