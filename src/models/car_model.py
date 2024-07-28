from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session
from .base import BaseModel
from sqlalchemy import Enum
from sqlalchemy.orm import relationship

CarTypeEnum = Enum('small_car', 'large_car', name='car_type_enum')

class CarModel(BaseModel):
    __tablename__ = 'Car'
    
    id = Column(Integer, primary_key=True)
    license_plate = Column(String, nullable=False)
    car_type = Column(CarTypeEnum, nullable=False)
    car_brand = Column(String,nullable=False)
    company_id = Column(Integer, ForeignKey('Company.id'), nullable=True)


    reservations = relationship('ReservationModel', back_populates='car')
    company = relationship('CompanyModel', back_populates='cars')

    @classmethod
    def add_car(cls, session: Session, license_plate: str, car_type: str, car_brand : str, company_id : int = None):
        car = cls(
            license_plate = license_plate,
            car_type = car_type,
            car_brand = car_brand,
            company_id = company_id,
        )
        session.add(car)
        session.commit()
        return car