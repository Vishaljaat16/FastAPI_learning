# from contextlib import asynccontextmanager
# from fastapi import FastAPI
# from models import UserData
# from schemas import UserRequest
# from database import Base, async_engine

# #* -------------- This is an Modern version -------- 
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     await async_engine.dispose()

# app = FastAPI(lifespan=lifespan)

# #* ------------------ Outdated Version Depricated from python side --------------- 
# # app = FastAPI()

# # @app.on_event("startup")
# # async def startup():
# #     async with async_engine.begin() as conn:
# #         await conn.run_sync(Base.metadata.create_all)

# #     print("Database tables created successfully!")

# @app.get("/getdata")
# async def get_data():
#     return {"message": "Yes i achieve this "}






from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import Base, async_engine, get_db
from models import UserData
from schemas import UserCreate, UserResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    new_user = UserData(
        name=user.name,
        email=user.email,
        age=user.age
    )

    db.add(new_user)

    await db.commit()

    await db.refresh(new_user)

    return new_user


@app.get("/show", response_model=list[UserResponse])
async def show_users(db: AsyncSession = Depends(get_db)):
    
    userdata = await db.execute(select(UserData))
    users = userdata.scalars().all()
    return users

@app.get("/show/{user_id}", response_model=list[UserResponse])
async def show_user(user_id:int, db: AsyncSession = Depends(get_db)):
    
    user_data = await db.execute(select(UserData).where(UserData.id == user_id))
    user = user_data.scalars().all()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user 

