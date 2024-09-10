from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import Session
from .base import BaseModel
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

class CarTypeEnum(PyEnum):
    small_car = "small_car"
    large_car = "large_car"

class CarModel(BaseModel):
    __tablename__ = 'Car'
    
    id = Column(Integer, primary_key=True)
    license_plate = Column(String(15), nullable=False)
    car_type = Column(SqlEnum(CarTypeEnum), nullable=False)
    car_brand = Column(String(30),nullable=False)
    company_id = Column(Integer, ForeignKey('Company.id'), nullable=True)


    reservations = relationship('ReservationModel', back_populates='car')
    company = relationship('CompanyModel', back_populates='cars')

    @classmethod
    def add_car(cls, session: Session, license_plate: str, car_type: str, car_brand: str, company_id: int = None):
        try:
            car = cls(
                license_plate=license_plate,
                car_type=car_type,
                car_brand=car_brand,
                company_id=company_id,
            )
            
            session.add(car)
            session.commit()
            
            return car
        
        except SQLAlchemyError as e:
            session.rollback()
            raise
        
        except Exception as e:
            session.rollback()
            raise