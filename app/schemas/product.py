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
        orm_mode = True
