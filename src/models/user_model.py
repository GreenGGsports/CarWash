from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from .base import BaseModel  # Adjust the import according to your project structure

class UserModel(BaseModel):
    __tablename__ = 'User'
    
    
    user_name = Column(String, nullable=False)
    password_hash = Column(String,nullable=False )