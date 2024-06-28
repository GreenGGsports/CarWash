from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from .base import BaseModel

class ServiceModel(BaseModel):
    __tablename__ = 'Service'
    
    id = Column(Integer, primary_key=True)
    service_name = Column(String, nullable=False)
    price_small = Column(Integer, nullable=False)
    price_large = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<ServiceModel(id={self.id}, service_name='{self.service_name}', price={self.price})>"

    @classmethod
    def add_service(cls, session: Session, service_name: str, price_small: int, price_large: int):
        service = cls(
            service_name = service_name,
            price_small = price_small,
            price_large = price_large
        )
        session.add(service)
        session.commit()
        return service
