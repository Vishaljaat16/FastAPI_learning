from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from db.database import Base 

class UserTable(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String, unique=True)
    age: Mapped[int] = mapped_column(Integer)
    
