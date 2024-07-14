from sqlalchemy import Column, Integer, String, Enum, ForeignKey 
from sqlalchemy.orm import Session, relationship
from .base import BaseModel

EtraTypeEnum = Enum('interior', 'exterior', name='EtraTypeEnum ')

class ExtraModel(BaseModel):
    __tablename__ = 'Extra'
    
    id = Column(Integer, primary_key=True)
    extra_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    extra_type = Column(EtraTypeEnum, nullable=False)
    carwash_id = Column(ForeignKey('Carwash.id'), nullable= False)
    carwash = relationship("CarWashModel")
    reservations = relationship('ReservationModel', secondary='reservation_extra', back_populates='extras')

    @classmethod
    def add_extra(cls, session: Session, extra_name: str, price: int, extra_type: str, carwash_id: int):
        extra = cls(
            extra_name=extra_name,
            price=price,
            extra_type=extra_type,
            carwash_id=carwash_id,
        )
        session.add(extra)
        session.commit()
        return extra