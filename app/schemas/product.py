from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str = Field(..., max_length=255)
    price: float = Field(..., ge=0)

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        # Pydantic v2: use from_attributes instead of orm_mode
        from_attributes = True
