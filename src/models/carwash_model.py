from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, Session
from .base import BaseModel
from datetime import timedelta, datetime
from typing import List
from src.models.slot_model import SlotModel


class CarWashModel(BaseModel):
    __tablename__ = 'Carwash'
    
    id = Column(Integer, primary_key=True)
    carwash_name = Column(String(30), nullable=False)
    location = Column(String(100), nullable=False)
    image_name = Column(String(30), nullable=True)
    
    close_start = Column(DateTime(),nullable=True)
    close_end = Column(DateTime(),nullable=True)

    slots = relationship('SlotModel', back_populates='carwash')  # Kapcsolat a SlotModel-lel

    @property
    def capacity(self):
        # Számolja ki a kapacitást a kapcsolódó slotokból
        return len([slot for slot in self.slots if slot.live])

    def __repr__(self):
        return self.carwash_name

    def add_slot(self, session: Session, start_time, end_time):
        slot = SlotModel(
            start_time=start_time,
            end_time=end_time,
            carwash_id=self.id  # Hozzáadjuk a carwash_id-t
        )
        session.add(slot)
        session.commit()
        return slot

    def get_live_slots(self, session: Session) -> List['SlotModel']:
        try:
            return session.query(SlotModel).filter_by(carwash_id=self.id, live=True).all()
        except Exception as e:
            session.rollback()
            raise e
        
    def get_live_slot_count(self, session: Session) -> int:
        try:
            return session.query(SlotModel).filter_by(carwash_id=self.id, live=True).count()
        except Exception as e:
            session.rollback()
            raise e

    def archive_current_slots(self, session: Session):
        try:
            session.query(SlotModel).filter_by(carwash_id=self.id, live=True).update({'live': False})
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def create_default_slots(self, session: Session, start_time, end_time, slot_count):
        # Átalakítjuk az időket datetime objektumokká
        today = datetime.today().date()
        start_datetime = datetime.combine(today, start_time)
        end_datetime = datetime.combine(today, end_time)

        # Ellenőrizzük, hogy az end_time nem korábbi mint a start_time
        if end_datetime <= start_datetime:
            raise ValueError("End time must be after start time.")

        total_duration = end_datetime - start_datetime

        # Ellenőrizzük, hogy az időtartam elegendő-e a megadott slot_count számára
        if total_duration.total_seconds() <= 0:
            raise ValueError("Invalid duration between start and end time.")

        slot_duration = total_duration / slot_count

        for i in range(slot_count):
            slot_start = start_datetime + i * slot_duration
            slot_end = slot_start + slot_duration
            # Slot létrehozása
            slot = SlotModel(
                carwash_id=self.id,
                start_time=slot_start,
                end_time=slot_end
            )
            session.add(slot)
        
        session.commit()

    def update_default_slots(self, session: Session, start_time, end_time, slot_count):
        # Előző élő slotok archiválása
        self.archive_current_slots(session)
        # Új slotok létrehozása
        self.create_default_slots(session, start_time, end_time, slot_count)
        
    def is_open(self, session: Session, date: datetime) -> bool:
        if self.close_start and self.close_end:
            if self.close_start <= date <= self.close_end:
                return False
        return True
