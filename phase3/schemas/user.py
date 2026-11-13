from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    
