from sqlalchemy import  Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel
from sqlalchemy.orm import Session


class SlotModel(BaseModel):
    __tablename__ = 'Slot'
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    historic = Column(Boolean, default=False)

    @classmethod
    def add_slot(cls, session: Session, start_time, end_time, ):
        user = cls(
            start_time = start_time,
            end_time = end_time
        )
        session.add(user)
        session.commit()
        return user