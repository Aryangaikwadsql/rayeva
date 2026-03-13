"""Product model for Module 1."""
from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_desc = Column(String, nullable=False)
    primary_category = Column(String)
    sub_category = Column(String)
    tags = Column(JSON)  # list[str]
    sustainability = Column(JSON)  # list[str]
    created_at = Column(DateTime(timezone=True), server_default=func.now())

