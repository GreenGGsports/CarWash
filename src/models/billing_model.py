from sqlalchemy import Column, Integer, String , ForeignKey
from sqlalchemy.orm import Session, relationship
from .base import BaseModel
from sqlalchemy.exc import SQLAlchemyError

class BillingModel(BaseModel):
    __tablename__ = 'Billing'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable= False)
    address = Column(String,nullable=False)
    email = Column(String,nullable=False)
    
    company_name = Column(String,nullable= True)
    tax_ID = Column(String,nullable=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=True)
    
    user = relationship("UserModel")
    
    @classmethod
    def add_billing_data(cls,session: Session,  name: str, address: str, email : str, company_name: str = None, tax_ID: str = None, user_id: int = None):
        billing_data = cls(
            name = name,
            address = address,
            email = email,
            company_name = company_name,
            tax_ID = tax_ID,
            user_id = user_id
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
            # Log the exception here if needed
            return None
        