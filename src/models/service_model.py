from sqlalchemy import Column, Integer, String
from .base import Base

class Service(Base):
    __tablename__ = 'Service'
    
    id = Column(Integer, primary_key=True)
    service_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
