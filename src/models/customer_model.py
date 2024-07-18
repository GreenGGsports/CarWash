from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, relationship
from .base import BaseModel

class CustomerModel(BaseModel):
    __tablename__ = 'Customer'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable= True)
    forname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

    user = relationship('UserModel')

    @classmethod
    def add_customer(cls, session: Session, forname: str,lastname: str, phone_number: str):
        customer = cls(
            forname = forname,
            lastname = lastname,
            phone_number = phone_number,
        )
        session.add(customer)
        session.commit()
        return customer

