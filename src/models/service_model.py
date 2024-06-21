from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from .base import Base

class ServiceModel(Base):
    __tablename__ = 'Service'
    
    id = Column(Integer, primary_key=True)
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

    @classmethod
    def get_service(cls, session: Session, service_id: int):
        """Fetch a single service by its ID."""
        try:
            return session.query(cls).get(service_id)
        except Exception as e:
            session.rollback()
            raise e
    
    @classmethod
    def get_services(cls, session: Session, skip: int = 0, limit: int = 10):
        """Fetch a list of services with optional pagination."""
        try:
            return session.query(cls).offset(skip).limit(limit).all()
        except Exception as e:
            session.rollback()
            raise e
    
    @classmethod
    def update_service(cls, session: Session, service_id: int, **kwargs):
        """Update an existing service."""
        try:
            service = session.query(cls).get(service_id)
            if not service:
                return None
            
            for key, value in kwargs.items():
                if hasattr(service, key):
                    setattr(service, key, value)
            
            session.commit()
            return service
        except Exception as e:
            session.rollback()
            raise e
    
    @classmethod
    def delete_service(cls, session: Session, service_id: int):
        """Delete a service by its ID."""
        try:
            service = session.query(cls).get(service_id)
            if service:
                session.delete(service)
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            session.rollback()
            raise e
