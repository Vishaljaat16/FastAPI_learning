from pydantic import EmailStr, BaseModel

#*------- User Registration Request Schema -------
class UserRegistraion(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    
#* ---------- User Login Request Schema ---------- 
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     username: str | None = None