"""Pydantic schemas for Product."""
from typing import List
from pydantic import BaseModel, Field


class SustainabilityFilter(BaseModel):
    name: str
    confidence: float = 0.0


class CategoryOutput(BaseModel):
    primary_category: str
    sub_category: str | None = None
    tags: List[str] = []
    sustainability: List[SustainabilityFilter] = []


class ProductCreate(BaseModel):
    product_desc: str


class ProductResponse(CategoryOutput):
    id: int
    product_desc: str
    created_at: str

    class Config:
        from_attributes = True

