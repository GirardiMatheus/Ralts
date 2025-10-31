from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ProductBase(BaseModel):
    name: str = Field(..., max_length=255)
    price: float = Field(..., ge=0)

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    created_at: Optional[datetime] = None

