import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback for Railway deployment
if not DATABASE_URL:
    print("WARNING: DATABASE_URL not set, using default SQLite")
    DATABASE_URL = "sqlite+aiosqlite:///./carro.db"

print(f"Using database: {DATABASE_URL}")

try:
    # Configure engine based on database type
    if "sqlite" in DATABASE_URL:
        # SQLite configuration
        engine = create_async_engine(DATABASE_URL, echo=False)  # Disable echo for production
    else:
        # PostgreSQL/MySQL configuration with connection pooling
        engine = create_async_engine(
            DATABASE_URL, 
            echo=False,  # Disable echo for production
            pool_size=20,
            max_overflow=0
        )

    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    print("✅ Database engine created successfully")

except Exception as e:
    print(f"❌ Database engine creation failed: {e}")
    raise

Base = declarative_base()
