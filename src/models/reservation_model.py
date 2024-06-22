from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from .base import BaseModel



class ReservationModel(BaseModel):
    __tablename__ = 'Reservation'
    
    id = Column(Integer, primary_key=True)
    appointment = Column(DateTime, default=datetime.datetime.utcnow)
    license_plate = Column(String(10), nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(String(20), nullable=False)
    brand = Column(String, nullable=False)
    type = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('Company.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('Service.id'), nullable=False)
    parking_spot = Column(String, nullable=True)
    
    company = relationship("CompanyModel")
    service = relationship("ServiceModel")
    
    def __repr__(self):
        return f"<Reservation(id={self.id}, appointment={self.appointment}, name='{self.name}', service_id={self.service_id})>"

    @classmethod
    def add_reservation(cls, session, appointment, license_plate, name, phone_number, brand, type, company_id, service_id, parking_spot=None):
        reservation = cls(
            appointment=appointment,
            license_plate=license_plate,
            name=name,
            phone_number=phone_number,
            brand=brand,
            type=type,
            company_id=company_id,
            service_id=service_id,
            parking_spot=parking_spot
        )
        session.add(reservation)
        session.commit()
        return reservation
