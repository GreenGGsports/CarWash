from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship, Session
from datetime import datetime
from .base import BaseModel
from src.models.reservation_extras import reservation_extra
from sqlalchemy import Enum
from typing import List, Optional
from src.models.service_model import ServiceModel
from src.models.extra_model import ExtraModel
from src.models.company_model import CompanyModel
from src.models.billing_model import BillingModel

CarTypeEnum = Enum('small_car', 'large_car', name='car_type_enum')


class ReservationModel(BaseModel):
    __tablename__ = 'Reservation'

    id = Column(Integer, primary_key=True)
    slot_id = Column(Integer, ForeignKey('Slot.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('Service.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('Company.id'), nullable=True)
    customer_id = Column(Integer, ForeignKey('Customer.id'), nullable=False)
    carwash_id = Column(Integer, ForeignKey('Carwash.id'), nullable=False)
    billing_id = Column(Integer, ForeignKey('Billing.id'), nullable=True)

    reservation_date = Column(DateTime, nullable=False)
    #car_data
    parking_spot = Column(Integer)
    car_type = Column(CarTypeEnum, nullable=False)
    car_brand = Column(String,nullable=False)
    final_price = Column(Float)
    license_plate = Column(String,nullable=False)

    slot = relationship("SlotModel")
    service = relationship("ServiceModel")
    company = relationship("CompanyModel")
    customer = relationship('CustomerModel', back_populates='reservations')
    extras = relationship('ExtraModel', secondary=reservation_extra, back_populates='reservations')
    carwash = relationship('CarWashModel')
    billing = relationship('BillingModel')


    @classmethod
    def calculate_final_price(cls, session: Session, service_id: int, car_type: str, extras: Optional[List[int]] = [], company_id: Optional[int] = None) -> float:
        # Szolgáltatás árának lekérése az autó típusától függően
        service = ServiceModel.get_by_id(session, service_id)
        if car_type == 'large_car':
            service_price = service.price_large if service else 0
        else:
            service_price = service.price_small if service else 0

        # Extrák árainak lekérése és összegzése
        total_extra_price = 0
        for extra_id in extras:
            extra = ExtraModel.get_by_id(session, extra_id)
            if extra:
                total_extra_price += extra.price

        # Cég kedvezményének alkalmazása (százalékban)
        company_discount = 0
        if company_id:
            company = CompanyModel.get_by_id(session, company_id)
            company_discount = company.discount if company else 0

        # Végső ár kiszámítása a kedvezmény alkalmazásával (százalékos kedvezmény)
        discount_multiplier = (100 - company_discount) / 100
        final_price = (service_price + total_extra_price) * discount_multiplier

        return final_price

    @classmethod
    def add_reservation(cls, session: Session, service_id: int, slot_id: int, carwash_id: int, 
                        reservation_date: datetime, customer_id: int, car_type: str, car_brand:str, license_plate:str, extras: Optional[List[int]] = None,
                        parking_spot: Optional[int] = None, billing_id: int = None,company_id: Optional[int] = None) -> 'ReservationModel':
        if extras is None:
            extras = []

        if not cls.is_slot_available(session, slot_id, reservation_date):
            raise Exception("Slot is not available for reservation")

        # Végső ár kiszámítása külön függvény használatával
        final_price = cls.calculate_final_price(session, service_id, car_type, extras, company_id)
        reservation = cls(
            company_id=company_id,
            service_id=service_id,
            slot_id=slot_id,
            customer_id=customer_id,
            carwash_id = carwash_id,
            parking_spot=parking_spot,
            reservation_date=reservation_date,
            car_type=car_type,
            license_plate=license_plate,
            car_brand = car_brand,
            final_price=final_price,
            extras=[ExtraModel.get_by_id(session, extra_id) for extra_id in extras],
            billing_id = billing_id
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
        # Check if there is any reservation for the same slot on the same day
        existing_reservation = session.query(cls).filter(
            cls.slot_id == slot_id,
            #todo use only = date
            cls.reservation_date >= datetime.combine(reservation_date, datetime.min.time()),
            cls.reservation_date <= datetime.combine(reservation_date, datetime.max.time())
        ).first()
        
        if existing_reservation:
            return False
        return True