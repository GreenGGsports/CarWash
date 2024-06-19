from sqlalchemy import Column, Integer, String
from .base import Base
from sqlalchemy.orm import Session

class ServiceModel(Base):
    __tablename__ = 'Service'
    
    id = Column(Integer, primary_key=True)
    service_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

def get_service(db: Session, service_id: int):
    return db.query(ServiceModel).filter(ServiceModel.id == service_id).first()

def get_services(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ServiceModel).offset(skip).limit(limit).all()

def create_service(db: Session, service_name: str, price: int):
    db_service = ServiceModel(service_name=service_name, price=price)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def update_service(db: Session, service_id: int, service_name: str = None, price: int = None):
    db_service = get_service(db, service_id)
    if db_service:
        if service_name is not None:
            db_service.service_name = service_name
        if price is not None:
            db_service.price = price
        db.commit()
        db.refresh(db_service)
    return db_service

def delete_service(db: Session, service_id: int):
    db_service = get_service(db, service_id)
    if db_service:
        db.delete(db_service)
        db.commit()
    return db_service