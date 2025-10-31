from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import models
from app.schemas.product import ProductCreate, ProductRead
from app.db.session import get_db

router = APIRouter()

@router.post("/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    product = models.Product(name=product_in.name, price=product_in.price)
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

@router.get("/products", response_model=List[ProductRead])
async def list_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Product).order_by(models.Product.id))
    products = result.scalars().all()
    return products

@router.get("/products/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Product).where(models.Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product
