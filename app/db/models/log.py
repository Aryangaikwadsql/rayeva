"""Log model for prompts/responses."""
from sqlalchemy import Column, Integer, String, JSON, DateTime, Text
from sqlalchemy.sql import func

from app.db.base import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    module = Column(String, nullable=False)  # e.g., "module1"
    prompt = Column(Text)
    response = Column(Text)
    extra_data = Column(JSON)  # input params etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

