from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./ralts.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=False
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
            pass
