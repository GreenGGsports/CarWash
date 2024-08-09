from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from .base import BaseModel

class UserModel(BaseModel):
    __tablename__ = 'User'
    
    id = Column(Integer, primary_key=True)
    user_name = Column(String(30), nullable=False)
    password_hash = Column(String(512), nullable=False)
    role = Column(String(20), nullable=False, default='user')  # Added role field
    carwash_id = Column(Integer, ForeignKey('Carwash.id'), nullable=True)  # Nullable for general admins

    carwash = relationship("CarWashModel")

    
    def __repr__(self):
        return f"<UserModel(id={self.id}, user_name='{self.user_name}')>"

    @classmethod
    def add_user(cls, session: Session, user_name: str, password: str, role: str = 'user', carwash_id=None):
        user = cls(
            user_name=user_name,
            password_hash=generate_password_hash(password=password),
            role=role,
            carwash_id = carwash_id
        )
        session.add(user)
        session.commit()
        return user
    
    @classmethod
    def login(cls, session: Session, user_name: str, password: str):
        user = session.query(cls).filter(
            cls.user_name == user_name
        ).first()
        if not user:
            return False
        if check_password_hash(user.password_hash, password):
            return user
        else:
            return False

    @classmethod
    def check_name_taken(cls, session: Session, user_name: str):
        user_query = session.query(cls).filter(
            cls.user_name == user_name
        ).first()
        return user_query is not None
