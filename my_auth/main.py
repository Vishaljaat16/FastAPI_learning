from fastapi import FastAPI, Depends, HTTPException, status

from contextlib import asynccontextmanager
from database import get_db, AsyncSession, Base, async_engine, get_password_hash, verify_password
from models import User
from schemas import UserLogin, UserRegistraion

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Application shutdown
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)



#* ---------------------------- User Registration -----------------------------
#-------------------- getting user Details ------------ 
from sqlalchemy import select
# async def check_user(db,user_email):
#     query = select(User).where(User.email == user_email)
#     result = await db.execute(query)
#     user = result.scalars().all()
#     if not user:
#         return False 
#     return True

async def get_current_user(db, user_email):
    query = select(User).where(User.email == user_email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if user:
        return user 
    return []

# ------------------ User Registration Endpoint ---------------------- 
@app.post("/registration")
async def userRegistration(user: UserRegistraion, db: AsyncSession = Depends(get_db)):
    
    user_check = await get_current_user(db, user.email)
    # print(check_user(db, user.email))
    if user_check:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already Exists")
    
    save_user = User(
        name = user.name,
        email = user.email,
        phone = user.phone,
        password = get_password_hash(user.password)
    )
    db.add(save_user)
    await db.commit()
    await db.refresh(save_user)
    return {
        "message":"User Registered Successfully",
        "Details": user
    }


#--------------------------- User Login ----------------------
# @app.post("/login") 
# async def user_login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    
#     user_check = await check_user(db, user.email)
    
#     if not user_check:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user doesn't exists")
    
#     return {
#         "message" : "Use Login successfully",
#     }


#* -------------------------------------------------------------
# ------ jwt access token and refresh token creation logic ------
import jwt

SECKRET_KEY = "my-secret-keydljaslkdjflaldfjlasadjfljaldjflkasjdflkjdlkfjlasjdfljk"
ALGORITHM = "HS256"

def create_access_token(access_payload:dict):
    return jwt.encode(access_payload, SECKRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(refresh_payload:dict):
    return jwt.encode(refresh_payload, SECKRET_KEY, algorithm=ALGORITHM)
    
# --------- User Login with OAuth2PasswordRequestForm + JWT Implementation --------------
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Response
from typing import Annotated
from datetime import datetime, timedelta, timezone

@app.post("/login") 
async def user_login(
    UserForm: Annotated[OAuth2PasswordRequestForm, Depends()],
    response:Response, 
    db: AsyncSession = Depends(get_db)):
    
    get_user = await get_current_user(db, UserForm.username)
    
    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Does not exists")
    
    verify_user = verify_password(UserForm.password, get_user.password)
    
    if not verify_user:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Wrong Password")
    
    access_payload = {
        "sub": str(get_user.id),
        "email": get_user.email,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
        "iat": datetime.now(timezone.utc),
    }
    
    refresh_payload = {
        "sub": str(get_user.id),
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
        "iat": datetime.now(timezone.utc),
    }
    
    # ------ creating jwt tokens -------
    access_token = create_access_token(access_payload)
    refresh_token = create_refresh_token(refresh_payload)
    
    response.set_cookie(
        key= "refresh_token",
        value= refresh_token,
        httponly= True,
        secure= False,
        samesite= 'lax',
        max_age= 1000,
        path= '/'
    )
    
    return {
        "message" : "Use Login successfully",
        "access" : access_token
    }
    
    
@app.post("/logout")
def logout(response: Response):

    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )

    return {
        "message": "Logout successful"
    }
    
    