from sqlalchemy import Column, Integer, String, Date
from database import Base


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    age = Column(Integer)
    date = Column(Date)
    