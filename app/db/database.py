from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.config import load_config


config = load_config()
DATABASE_URL = config.db.database_url
SYNC_URL = DATABASE_URL.replace("asyncpg", "psycopg2")
sync_engine = create_engine(SYNC_URL, echo=False)
Base = automap_base()
Base.prepare(sync_engine, reflect=True)
User = Base.classes.users
print(Base.classes.keys())


sync_engine.dispose()

async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(async_engine, class_=AsyncSession)

async def get_async_session():
    async with async_session_maker() as session:
        yield session




