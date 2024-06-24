from sqlalchemy import  Column, Integer, String, DateTime, Boolean
from .base import BaseModel
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import  List


class SlotModel(BaseModel):
    __tablename__ = 'Slot'
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    live = Column(Boolean, default=True)

    @classmethod
    def add_slot(cls, session: Session, start_time, end_time, ):
        user = cls(
            start_time = start_time,
            end_time = end_time
        )
        session.add(user)
        session.commit()
        return user
    
    @classmethod
    def get_live_slots(cls, session: Session) -> List['SlotModel']:
        try:
            return session.query(cls).filter_by(live=True).all()
        except Exception as e:
            session.rollback()
            raise e
    
    def archive_current_slots(session: Session):
        # Minden aktuális slot történetivé válik (live = False)
        try:
            session.query(SlotModel).filter_by(is_default=True).update({'live': False})
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def create_default_slots(session: Session, start_time, end_time, slot_duration_minutes):
        current_time = start_time

        while current_time < end_time:
            slot_end_time = current_time + timedelta(minutes=slot_duration_minutes)
            SlotModel.add_slot(session, start_time=current_time, end_time=slot_end_time)
            current_time = slot_end_time

    def update_default_slots(session: Session, start_time, end_time, slot_duration_minutes):
        SlotModel.archive_current_slots(session)
        SlotModel.create_default_slots(session, start_time, end_time, slot_duration_minutes)
