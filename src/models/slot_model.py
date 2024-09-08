from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class SlotModel(BaseModel):
    __tablename__ = 'Slot'
    
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    live = Column(Boolean, default=True)
    carwash_id = Column(Integer, ForeignKey('Carwash.id'), nullable=False)  # Hozzáadott mező

    carwash = relationship('CarWashModel', back_populates='slots')  # Kapcsolat a CarWashModel-lel

    def __repr__(self):
        return f"Slot(id={self.id}, start_time={self.start_time}, end_time={self.end_time}, live={self.live})"
