from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from collections.abc import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="config.env")
DATABASE_URL = os.environ.get("DATABASE_URL")

async_engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
            
            
# Create database tables asynchronously           
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        
        
# Close the engine when the application shuts down
async def close_database():
    await async_engine.dispose()
    
    
    
from contextlib import asynccontextmanager
from fastapi import FastAPI

from db.database import create_tables, async_engine
import models  # Registers UserTable with Base.metadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()

    yield

    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)