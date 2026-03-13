# app/db/models/__init__.py
from .product import Product
from .proposal import Proposal
from .log import Log
from .impact import Impact

__all__ = ["Product", "Proposal", "Log", "Impact"]

