from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import Session
from .base import BaseModel
import enum

class ServiceType(enum.Enum):
    PACKAGE = "package"
    EXTRA_OUTSIDE = "extra_outside"
    EXTRA_INSIDE = "extra_inside"

class ServiceModel(BaseModel):
    __tablename__ = 'Service'
    
    id = Column(Integer, primary_key=True)
    service_name = Column(String, nullable=False)
    price_small = Column(Integer, nullable=False)
    price_large = Column(Integer, nullable=False)
    service_type = Column(Enum(ServiceType), nullable=False)

    def __repr__(self):
        return f"<ServiceModel(id={self.id}, service_name='{self.service_name}', service_type={self.service_type})>"

    @classmethod
    def add_service(cls, session: Session, service_name: str, price_small: int, price_large: int, service_type: ServiceType):
        service = cls(
            service_name = service_name,
            price_small = price_small,
            price_large = price_large,
            service_type = service_type
        )
        session.add(service)
        session.commit()
        return service
