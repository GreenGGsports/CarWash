from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, String, Boolean, Enum as SqlEnum
from sqlalchemy.orm import relationship, Session
from datetime import datetime
from .base import BaseModel
from src.models.reservation_extras import reservation_extra
from enum import Enum as PyEnum
from typing import List, Optional
from src.models.service_model import ServiceModel
from src.models.extra_model import ExtraModel
from src.models.company_model import CompanyModel
from src.models.car_model import CarModel

class PaymentEnum(PyEnum):
    card = "bankkárya"
    cash = "készpénz"
    list = "listás"
    transaction = 'utalás'

    def __str__(self):
        return self.value
    

class ReservationModel(BaseModel):
    __tablename__ = 'Reservation'

    id = Column(Integer, primary_key=True)
    slot_id = Column(Integer, ForeignKey('Slot.id'), nullable=False)
    car_id = Column(Integer, ForeignKey('Car.id'))
    service_id = Column(Integer, ForeignKey('Service.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('Customer.id'), nullable=False)
    carwash_id = Column(Integer, ForeignKey('Carwash.id'), nullable=False)
    
    reservation_date = Column(DateTime, nullable=False)
    parking_spot = Column(String(127))
    
    final_price = Column(Integer)
    payment_method = Column(SqlEnum(PaymentEnum, nullable = False))
    is_completed = Column(Boolean, default=False)
    comment = Column(String(512), nullable=True)

    car = relationship('CarModel', back_populates='reservations')
    slot = relationship("SlotModel")
    service = relationship("ServiceModel")
    customer = relationship('CustomerModel', back_populates='reservations')
    extras = relationship('ExtraModel', secondary=reservation_extra, back_populates='reservations')
    carwash = relationship('CarWashModel')
    billing = relationship('BillingModel', back_populates='reservation', uselist=False)
    
    def __init__(self, slot_id, service_id, customer_id, carwash_id, reservation_date, extras = None,
                 parking_spot=None, car_id=None, final_price=None, payment_method=None, 
                 is_completed=False, comment=None):
        self.slot_id = slot_id
        self.service_id = service_id
        self.customer_id = customer_id
        self.carwash_id = carwash_id
        self.reservation_date = reservation_date
        self.parking_spot = parking_spot
        self.car_id = car_id
        self.final_price = final_price
        self.payment_method = payment_method
        self.is_completed = is_completed
        self.comment = comment
        
    def calculate_final_price(self,session: Session) -> float:
        # Szolgáltatás árának lekérése az autó típusától függően
        car = session.query(CarModel).filter_by(id=self.car_id).first()
        service= session.query(ServiceModel).filter_by(id=self.service_id).first()
        
        if car.car_type.value == 'large_car':
            service_price = service.price_large if service else 0
        elif car.car_type.value == 'medium_car':
            service_price = service.price_medium if service else 0
        else:
            service_price = service.price_small if service else 0

        # Extrák árainak lekérése és összegzése
        
        total_extra_price = 0
        for extra_id in self.extras:
            if extra_id:
                extra = session.query(ExtraModel).filter_by(id=extra_id)
                total_extra_price += extra.price

        # Cég kedvezményének alkalmazása (százalékban)
        company_discount = 0
        if car.company_id:
            company = car.company
            company_discount = company.discount if company else 0

        # Végső ár kiszámítása a kedvezmény alkalmazásával (százalékos kedvezmény)
        discount_multiplier = (100 - company_discount) / 100
        final_price = int((service_price + total_extra_price) * discount_multiplier)

        self.final_price = final_price
        from pdb import set_trace
        set_trace()


    @classmethod
    def add_reservation(cls, session: Session, service_id: int, slot_id: int, carwash_id: int, car_id : int,
                        reservation_date: datetime, customer_id: int, payment_method = str ,extras: Optional[List[int]] = None,
                        parking_spot: Optional[String] = None, final_price=None,is_completed=False, comment=None) -> 'ReservationModel':
        

        if extras is None:
            extras = []

        # Végső ár kiszámítása külön függvény használatával
        if not final_price:
            final_price = ReservationModel.calculate_final_price(session, service_id , car_id, extras)
        from pdb import set_trace
        set_trace() 
        reservation = cls(
            car_id=car_id,
            service_id=service_id,
            slot_id=slot_id,
            customer_id=customer_id,
            carwash_id = carwash_id,
            parking_spot=parking_spot,
            reservation_date=reservation_date,
            final_price=final_price,
            payment_method = payment_method,
            extras=[ExtraModel.get_by_id(session, extra_id) for extra_id in extras],
            is_completed = is_completed,
            comment = comment
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