from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship, Session
from datetime import datetime, date
from .base import BaseModel
from sqlalchemy import Enum

CarTypeEnum = Enum('small_car', 'large_car', name='car_type_enum')

class ReservationModel(BaseModel):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True)
    slot_id = Column(Integer, ForeignKey('Slot.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('Service.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('Company.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    reservation_date = Column(DateTime, nullable=False)
    parking_spot = Column(Integer)
    car_type = Column(CarTypeEnum, nullable=False)
    final_price = Column(Float)

    slot = relationship("SlotModel")
    service = relationship("ServiceModel")
    company = relationship("CompanyModel")
    user = relationship("UserModel")

    @classmethod
    def add_reservation(cls, session: Session, company_id: int, service_id: int, slot_id: int, 
                        reservation_date: datetime, user_id: int, car_type, final_price: float, 
                        parking_spot: int = None):
        # Check if the slot is available
        if not cls.is_slot_available(session, slot_id, reservation_date):
            raise Exception("Slot is not available for reservation")

        reservation = cls(
            company_id=company_id,
            service_id=service_id,
            slot_id=slot_id,
            user_id=user_id,
            parking_spot=parking_spot,
            reservation_date=reservation_date,
            car_type=car_type,
            final_price=final_price
        )
        try:
            session.add(reservation)
            session.commit()
            return reservation
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def is_slot_available(cls, session: Session, slot_id: int, reservation_date: datetime) -> bool:
        # Convert reservation_date to date object to ignore time part
        reservation_date_only = reservation_date.date()
        
        # Check if there is any reservation for the same slot on the same day
        existing_reservation = session.query(cls).filter(
            cls.slot_id == slot_id,
            cls.reservation_date >= datetime.combine(reservation_date_only, datetime.min.time()),
            cls.reservation_date <= datetime.combine(reservation_date_only, datetime.max.time())
        ).first()
        
        if existing_reservation:
            return False
        return True
