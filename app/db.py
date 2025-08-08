import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Configure engine based on database type
if "sqlite" in DATABASE_URL:
    # SQLite configuration
    engine = create_async_engine(DATABASE_URL, echo=True)
else:
    # PostgreSQL/MySQL configuration with connection pooling
    engine = create_async_engine(
        DATABASE_URL, 
        echo=True,
        pool_size=20,
        max_overflow=0
    )

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()
