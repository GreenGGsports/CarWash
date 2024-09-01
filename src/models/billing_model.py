from sqlalchemy import Column, Integer, String, Date , ForeignKey
from sqlalchemy.orm import Session, relationship
from .base import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from src.models.reservation_model import ReservationModel

class BillingModel(BaseModel):
    __tablename__ = 'Billing'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable= False)
    address = Column(String(100),nullable=False)
    email = Column(String(30),nullable=False)
    date = Column(Date)  
    reservation_id = Column(Integer, ForeignKey('Reservation.id'),nullable=False)
    
    company_name = Column(String(30),nullable= True)
    tax_ID = Column(String(30),nullable=True)
    reservation = relationship('ReservationModel', back_populates='billing')
    
    
    @classmethod
    def add_billing_data(cls,session: Session, reservation_id: int,  name: str, address: str, email : str, company_name: str = None, tax_ID: str = None):
        billing_data = cls(
            name = name,
            reservation_id = reservation_id,
            address = address,
            email = email,
            company_name = company_name,
            tax_ID = tax_ID,
        )

        try:
            session.add(billing_data)
            session.commit()
            return billing_data 
        except Exception as e:
            session.rollback()
            raise e 
               
    @classmethod
    def get_last_by_user_id(cls, session: Session, user_id: int):
        try:
            billing_data = session.query(cls).filter(
                cls.user_id == user_id
            ).order_by(cls.id.desc()).first()  # Assuming `id` is an auto-incremented field
            
            if billing_data:
                return billing_data
            return None  # Return None instead of False for more idiomatic Python
        except SQLAlchemyError as e:
            session.rollback()
            return None
        