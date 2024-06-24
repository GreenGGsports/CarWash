from sqlalchemy import Column, Integer, DateTime, Boolean, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from datetime import datetime

from .base import BaseModel

class ReservationModel(BaseModel):
    __tablename__ = 'reservation'

    slot_id = Column(Integer, ForeignKey('Slot.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('Service.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('Company.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    reservation_date = Column(DateTime, nullable=False)
    parking_spot = Column(Integer)
    car_type = Column(String)
    final_price = Column(Float)

    slot = relationship("SlotModel")
    service = relationship("ServiceModel")
    company = relationship("CompanyModel")
    user = relationship("UserModel")

    @classmethod
    def add_reservation(cls, session, company_id, service_id, slot_id,reservation_date,user_id , car_type, final_price ,parking_spot=None):
        reservation = cls( 
            company_id=company_id,
            service_id=service_id,
            slot_id = slot_id,
            user_id = user_id,
            parking_spot=parking_spot,
            reservation_date = reservation_date,
            car_type = car_type,
            final_price = final_price
        )
        session.add(reservation)
        session.commit()
        return reservation