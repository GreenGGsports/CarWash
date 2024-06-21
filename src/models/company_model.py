from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from .base import Base

class CompanyModel(Base):
    __tablename__ = 'Company'
    
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

    @classmethod
    def get_company(cls, session: Session, company_id: int):
        """Fetch a single company by its ID."""
        try:
            return session.query(cls).get(company_id)
        except Exception as e:
            session.rollback()
            raise e
    
    @classmethod
    def get_companies(cls, session: Session, skip: int = 0, limit: int = 10):
        """Fetch a list of companies with optional pagination."""
        try:
            return session.query(cls).offset(skip).limit(limit).all()
        except Exception as e:
            session.rollback()
            raise e
    
    @classmethod
    def update_company(cls, session: Session, company_id: int, company_name: str = None):
        """Update an existing company."""
        try:
            company = session.query(cls).get(company_id)
            if not company:
                return None
            
            if company_name is not None:
                company.company_name = company_name
            
            session.commit()
            return company
        except Exception as e:
            session.rollback()
            raise e
    
    @classmethod
    def delete_company(cls, session: Session, company_id: int):
        """Delete a company by its ID."""
        try:
            company = session.query(cls).get(company_id)
            if company:
                session.delete(company)
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            session.rollback()
            raise e
