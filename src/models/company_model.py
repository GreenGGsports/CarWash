from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from .base import Base

class CompanyModel(Base):
    __tablename__ = 'Company'
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String, nullable=False)



def get_company(db: Session, company_id: int):
    return db.query(CompanyModel).filter(CompanyModel.id == company_id).first()

def get_companies(db: Session, skip: int = 0, limit: int = 10):
    return db.query(CompanyModel).offset(skip).limit(limit).all()

def create_company(db: Session, company_name: str):
    db_company = CompanyModel(company_name=company_name)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_company(db: Session, company_id: int, company_name: str = None):
    db_company = get_company(db, company_id)
    if db_company:
        if company_name is not None:
            db_company.company_name = company_name
        db.commit()
        db.refresh(db_company)
    return db_company

def delete_company(db: Session, company_id: int):
    db_company = get_company(db, company_id)
    if db_company:
        db.delete(db_company)
        db.commit()
    return db_company