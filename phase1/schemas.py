from pydantic import BaseModel, EmailStr
from datetime import date


class EmpolyeeRequest(BaseModel):
    id: int
    name: str
    email: str
    age: int
    date: str 

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    date: str