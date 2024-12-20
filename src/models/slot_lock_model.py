from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.models.base import BaseModel

class SlotLockModel(BaseModel):
    __tablename__ = 'slot_locks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    slot_id = Column(Integer, ForeignKey('Slot.id', ondelete="CASCADE"), nullable=False)  # Kapcsolat a SlotModel-lel
    user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"), nullable=False)  # Kapcsolat a felhasználóval
    reservation_date = Column(DateTime, nullable=False)  # A dátum, amelyre a slotot zárolták
    locked_until = Column(DateTime, nullable=False)  # A zárolás lejárati ideje

    # Kapcsolatok
    slot = relationship("SlotModel")  # Slot kapcsolata
    user = relationship("UserModel")  # Felhasználó kapcsolata

    def is_active(self) -> bool:
        """ Ellenőrzi, hogy a zárolás még érvényes-e. """
        return self.locked_until > datetime.now()
