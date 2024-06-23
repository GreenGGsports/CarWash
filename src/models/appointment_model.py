from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Type

from .base import BaseModel

class AppointmentModel(BaseModel):
    __tablename__ = 'Appointment'
    
    appointment_time = Column(DateTime, nullable=False)
    car_ready = Column(Boolean, default=False)

    @classmethod
    def add(cls: Type['AppointmentModel'], session: Session, appointment_time: datetime, car_ready: bool = False) -> 'AppointmentModel':
        try:
            new_appointment = cls(appointment_time=appointment_time, car_ready=car_ready)
            session.add(new_appointment)
            session.commit()
            return new_appointment
        except Exception as e:
            session.rollback()
            raise e
