from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from .base import BaseModel

class BillingModel(BaseModel):
    __tablename__ = 'Billing'
    
    id = Column(Integer, primary_key=True)
    license_plate = Column(String, nullable=False)
    name = Column(String, nullable= False)
    address = Column(String,nullable=False)
    email = Column(String,nullable=False)
    
    company_name = Column(String,nullable= True)
    tax_ID = Column(String,nullable=True)
    
    @classmethod
    def add_billing_data(cls,session: Session, license_plate: str, name: str, address: str, email : str, company_name: str = None, tax_ID: str = None):
        billing_data = cls(
            license_plate = license_plate,
            name = name,
            address = address,
            email = email,
            company_name = company_name,
            tax_ID = tax_ID
        )

        try:
            session.add(billing_data)
            session.commit()
            return billing_data 
        except Exception as e:
            session.rollback()
            raise e 
               
    @classmethod    
    def get_by_license_plate(cls, session: Session, license_plate):
        billing_data = session.query(cls).filter(
            cls.license_plate == license_plate
        ).first()
        
        if billing_data:
            return billing_data.__dict__
        return False 
        