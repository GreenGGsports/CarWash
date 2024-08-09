from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from .base import BaseModel


class CarWashModel(BaseModel):
    __tablename__ = 'Carwash'
    
    id = Column(Integer, primary_key=True)
    carwash_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    image_name = Column(String, nullable = True)
    
    
    def __repr__(self):
        return self.carwash_name

    @classmethod
    def add_carwash(cls, session: Session, carwash_name: str, location: str):
        company = cls(
            carwash_name = carwash_name,
            location = location
        )
        session.add(company)
        session.commit()
        return company
