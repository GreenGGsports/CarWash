from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from .base import BaseModel

class CompanyModel(BaseModel):
    __tablename__ = 'company'
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String, nullable=False)


    
    def __repr__(self):
        return f"<CompanyModel(id={self.id}, company_name='{self.company_name}')>"

    @classmethod
    def add_company(cls, session: Session, company_name: str):
        company = cls(
            company_name = company_name
        )
        session.add(company)
        session.commit()
        return company
