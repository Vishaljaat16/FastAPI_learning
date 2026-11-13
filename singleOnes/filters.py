from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter 

from pydantic import BaseModel

class Address(BaseModel):
    street:str 
    road: str
    colony: str
    
class AddressFilter(Filter):
    street: Optional[str]
    country: Optional[str]
    city__in: Optional[list[str]]
    
    class Constants(Filter.Constants):
        model = Address 
        
        
# @app.get("/users", response_model = list[])