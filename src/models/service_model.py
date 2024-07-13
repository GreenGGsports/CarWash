from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, relationship
from .base import BaseModel

class ServiceModel(BaseModel):
    __tablename__ = 'Service'

    id = Column(Integer, primary_key=True)
    service_name = Column(String, nullable=False)
    price_small = Column(Integer, nullable=False)
    price_large = Column(Integer, nullable=False)
    description = Column(String,nullable=True )
    carwash_id = Column(Integer, ForeignKey('Carwash.id'), nullable=True)
    
    carwash = relationship("CarWashModel")
    def __repr__(self):
        return f"<ServiceModel(id={self.id}, service_name='{self.service_name}', service_type={self.service_type})>"

    @classmethod
    def add_service(cls, session: Session, service_name: str, price_small: int, price_large: int, carwash_id : int, description: str = None):
        service = cls(
            service_name = service_name,
            price_small = price_small,
            price_large = price_large,
            carwash_id = carwash_id,
            description = description
        )
        session.add(service)
        session.commit()
        return service
