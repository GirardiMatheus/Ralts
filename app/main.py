from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db.session import engine, get_db
from app.db.base import Base
from app.db import models

app = FastAPI(title="Ralts API")

Base.metadata.create_all(bind=engine)

@app.get("/healthcheck")
async def healthcheck(db: Session = Depends(get_db)):
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
