from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from .base import BaseModel

class ServiceModel(BaseModel):
    __tablename__ = 'service'
    
    service_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<ServiceModel(id={self.id}, service_name='{self.service_name}', price={self.price})>"

    @classmethod
    def add_service(cls, session: Session, service_name: str, price: int):
        service = cls(
            service_name = service_name,
            price = price
        )
        session.add(service)
        session.commit()
        return service
