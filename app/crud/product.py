"""CRUD for Product."""
from sqlalchemy.orm import Session

from app.db.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse


def create_product(db: Session, obj_in: ProductCreate, ai_data: dict = None) -> Product:
    db_obj = Product(
        product_desc=obj_in.product_desc,
        primary_category=ai_data.get("primary_category") if ai_data else None,
        sub_category=ai_data.get("sub_category") if ai_data else None,
        tags=ai_data.get("tags") if ai_data else None,
        sustainability=ai_data.get("sustainability") if ai_data else None
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def log_ai(db: Session, module: str, prompt: str, response: str, metadata: dict) -> None:
    from app.db.models.log import Log
    log = Log(module=module, prompt=prompt, response=response, extra_data=metadata)
    db.add(log)
    db.commit()

