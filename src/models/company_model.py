from sqlalchemy import Column, Integer, String
from .base import Base

class Company(Base):
    __tablename__ = 'Company'
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String, nullable=False)
