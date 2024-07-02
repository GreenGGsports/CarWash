from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from .base import BaseModel

class UserModel(BaseModel):
    __tablename__ = 'User'
    
    id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False)
    password_hash = Column(String,nullable=False )


    
    def __repr__(self):
        return f"<UserModel(id={self.id}, user_name='{self.user_name}')>"

    @classmethod
    def add_user(cls, session: Session, user_name: str, password: str ):
        user = cls(
            user_name = user_name,
            password_hash = generate_password_hash(password=password)
        )
        session.add(user)
        session.commit()
        return user
    
    @classmethod
    def login(cls,session : Session, user_name: str, password):
        user = session.query(cls).filter(
            cls.user_name == user_name
            ).first()
        
        if check_password_hash(user.password_hash,password):
            return user
        else:
            return False

    @classmethod
    def check_name_taken(cls,session: Session,user_name: str):
        user_query = session.query(cls).filter(
            cls.user_name == user_name
            ).first()
        if user_query:
            return True
        
        else:
            return False 
        
        
        