from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import engine, get_db
from app.db.base import Base
from app.db import models
from app.api import routes

app = FastAPI(title="Ralts API")

@app.on_event("startup")
async def startup():
    # criar tabelas assincronamente em dev
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(routes.router)

@app.get("/healthcheck")
async def healthcheck(db: AsyncSession = Depends(get_db)):
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
