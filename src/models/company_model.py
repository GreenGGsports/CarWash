from sqlalchemy import Column, Integer, String, Double 
from sqlalchemy.orm import Session
from .base import BaseModel

class CompanyModel(BaseModel):
    __tablename__ = 'Company'
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String, nullable=False)
    discount = Column(Double, nullable=False, default=0)
    
    def __repr__(self):
        return f"<CompanyModel(id={self.id}, company_name='{self.company_name}')>"

    @classmethod
    def add_company(cls, session: Session, company_name: str, discount: float = None):
        company = cls(
            company_name = company_name,
            discount = discount
        )
        session.add(company)
        session.commit()
        return company
