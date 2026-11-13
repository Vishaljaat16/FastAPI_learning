from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=("config.env"))

DATABASE_URL = os.environ.get("DATABASE_URL")

async_engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


#* ----------------- Lengthy process ------------------------ 
# async def get_db():
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#         finally:
#             session.close()

#* ---------------- Simple process ------------------------------
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
            
            
            
print("this page is working perfectly")