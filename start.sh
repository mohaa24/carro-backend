#!/bin/bash
# Railway startup script

echo "Starting Carro Backend..."

# Initialize database if it doesn't exist
python -c "
import asyncio
import os
from app.db import engine, Base

async def init_db():
    print('Checking database...')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Database ready!')

if __name__ == '__main__':
    asyncio.run(init_db())
"

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
