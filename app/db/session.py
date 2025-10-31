import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# usa DATABASE_URL da env quando disponível; fallback para sqlite local
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./ralts.db")

# para sqlite+aiosqlite é útil passar connect_args
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args=connect_args,
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            # o context manager fecha a sessão
            pass
