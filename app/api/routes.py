from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import models
from app.schemas.product import ProductCreate, ProductRead
from app.db.session import get_db
from app.services.scraper_runner import start_scraper
from app.services.processor import average_price, most_expensive, cheapest, count_by_category

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

@router.post("/scrape/start", status_code=status.HTTP_202_ACCEPTED)
async def scrape_start():
    info = start_scraper("product_spider")
    return {"status": "started", **info}

@router.get("/products/stats", status_code=status.HTTP_200_OK)
async def products_stats(db: AsyncSession = Depends(get_db), top: int = 5):

    result = await db.execute(select(models.Product))
    products = result.scalars().all()

    avg = average_price(products)
    most = most_expensive(products, n=top)
    least = cheapest(products, n=top)
    counts = count_by_category(products, key="source")

    def to_simple(p):
        return {"id": getattr(p, "id", None), "name": getattr(p, "name", None), "price": float(getattr(p, "price", 0) or 0)}

    return {
        "average_price": avg,
        "most_expensive": [to_simple(p) for p in most],
        "cheapest": [to_simple(p) for p in least],
        "count_by_source": counts,
    }
