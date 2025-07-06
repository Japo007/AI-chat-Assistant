from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from app.models.query_cache import QueryCache

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "startups.db")

DATABASE_URL = f"sqlite+aiosqlite:///{os.path.abspath(DB_PATH)}"

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    from app.models.company import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(QueryCache.metadata.create_all)