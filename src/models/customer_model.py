from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, relationship
from .base import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from typing import Type, Optional

class CustomerModel(BaseModel):
    __tablename__ = 'Customer'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable= True)
    forname = Column(String(30), nullable=False)
    lastname = Column(String(30), nullable=False)
    phone_number = Column(String(30), nullable=False)

    user = relationship('UserModel')
    reservations = relationship('ReservationModel', back_populates='customer')

    @classmethod
    def add_customer(cls, session: Session, forname: str,lastname: str, phone_number: str, user_id: int = None):
        customer = cls(
            forname = forname,
            lastname = lastname,
            phone_number = phone_number,
            user_id = user_id
        )
        session.add(customer)
        session.commit()
        return customer
    
    @classmethod
    def get_last_by_user_id(cls: Type['BaseModel'], session: Session, user_id: int) -> Optional['BaseModel']:
        try:
            # Query to get the latest customer by user_id, ordered by id in descending order
            latest_customer = session.query(cls).filter_by(user_id=user_id).order_by(cls.id.desc()).first()
            return latest_customer
        except SQLAlchemyError as e:
            # Rollback the session in case of an error
            session.rollback()
            print(f"An error occurred: {e}")
            return None


