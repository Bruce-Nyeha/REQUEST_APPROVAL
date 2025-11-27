from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from config import settings

# Database URL
DATABASE_URL = settings.DATABASE_URL  

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

#  Create the async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,   # 
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

#  Base for all models
Base = declarative_base()

#  Dependency for routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
