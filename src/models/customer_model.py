from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, relationship
from .base import BaseModel

class CustomerModel(BaseModel):
    __tablename__ = 'Customer'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable= True)
    customer_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

    user = relationship('UserModel')

    @classmethod
    def add_customer(cls, session: Session, customer_name: str, phone_number: str):
        customer = cls(
            customer_name = customer_name,
            phone_number = phone_number,
        )
        session.add(customer)
        session.commit()
        return customer

