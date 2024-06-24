from sqlalchemy import Column, Integer, DateTime, Boolean, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from datetime import datetime

from .base import BaseModel

class ReservationModel(BaseModel):
    __tablename__ = 'reservation'

    appointment_id = Column(Integer, ForeignKey('Appointment.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('Service.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('Company.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    reservation_date = Column(DateTime, nullable=False)
    parking_spot = Column(Integer)
    car_type = Column(String)
    license_plate = Column(String)
    final_price = Column(Float)

    appointment = relationship("AppointmentModel")
    service = relationship("ServiceModel")
    company = relationship("CompanyModel")
    user = relationship("UserModel")

    @classmethod
    def add_reservation(cls, session, license_plate, company_id, service_id,appointment_id,reservation_date,user_id , car_type, final_price ,parking_spot=None):
        reservation = cls( 
            license_plate=license_plate,
            company_id=company_id,
            service_id=service_id,
            appointment_id = appointment_id,
            user_id = user_id,
            parking_spot=parking_spot,
            reservation_date = reservation_date,
            car_type = car_type,
            final_price = final_price
        )
        session.add(reservation)
        session.commit()
        return reservation