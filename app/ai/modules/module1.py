"""Module 1: AI Auto-Category & Tag Generator."""
from typing import Dict, Any

from app.ai.client import generate, StructuredOutput
from app.schemas.product import CategoryOutput


PREDEFINED_CATEGORIES = [
    "Clothing & Apparel",
    "Electronics",
    "Home & Kitchen",
    "Beauty & Personal Care",
    "Food & Grocery",
    "Sports & Outdoors",
    "Books & Stationery",
    "Toys & Games",
    "Health & Wellness",
    "Sustainable Packaging"
]

SUSTAINABILITY_FILTERS = [
    "plastic-free", "compostable", "vegan", "recycled", "organic", 
    "carbon-neutral", "fair-trade", "biodegradable"
]


def generate_category(product_desc: str) -> Dict[str, Any]:
    """Generate category/tags."""
    categories_str = ", ".join(PREDEFINED_CATEGORIES)
    filters_str = ", ".join(SUSTAINABILITY_FILTERS)
    
    prompt = f"""
    Analyze this product: "{product_desc}"

    1. Primary category (exact from: {categories_str})
    2. Sub-category (specific)
    3. 5-10 SEO tags
    4. Relevant sustainability filters (from: {filters_str}, with confidence 0-1)

    Respond ONLY with valid JSON matching this schema:
    {{"primary_category": "str", "sub_category": "str|null", "tags": ["str"], "sustainability": [{{"name": "str", "confidence": float}}]}}

    Be precise and business-oriented for sustainable commerce.
    """
    
    result = generate(
        model_provider="openrouter",
        model="gpt-4o-mini",
        prompt=prompt,
        response_model=CategoryOutput
    )
    
    return result

