from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from .base import BaseModel  # Adjust the import according to your project structure

class UserModel(BaseModel):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)

    @classmethod
    def add_user(cls, session: Session, username, email, full_name, phone_number=None, address=None):
        user = cls(
            username=username,
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            address=address,
        )
        session.add(user)
        session.commit()
        return user
