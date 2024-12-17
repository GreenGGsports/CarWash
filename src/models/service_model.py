from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, relationship
from .base import BaseModel
from src.models.service_extras import service_extra

class ServiceModel(BaseModel):
    __tablename__ = 'Service'

    id = Column(Integer, primary_key=True)
    service_name = Column(String(64), nullable=False)
    price_small = Column(Integer, nullable=False)
    price_medium = Column(Integer,nullable=False)
    price_large = Column(Integer, nullable=False)
    description = Column(String(512),nullable=True )
    carwash_id = Column(Integer, ForeignKey('Carwash.id'), nullable=True)
    
    extras = relationship('ServiceModel', secondary=service_extra, back_populates='extras')
    carwash = relationship("CarWashModel")
    def __repr__(self):
        return self.service_name

    @classmethod
    def add_service(cls, session: Session, service_name: str, price_small: int, price_large: int ,price_medium:str , carwash_id : int, description: str = None):
        service = cls(
            service_name = service_name,
            price_small = price_small,
            price_medium = price_medium,
            price_large = price_large,
            carwash_id = carwash_id,
            description = description
        )
        session.add(service)
        session.commit()
        return service
    