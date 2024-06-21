import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import Base
from src.models.company_model import CompanyModel


@pytest.fixture(scope='module')
def engine():
    return create_engine('sqlite:///:memory:')


@pytest.fixture(scope='module')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def session(engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_add_company(session):
    company_name = "Test Company"
    company = CompanyModel.add_company(session, company_name)
    assert company.id is not None
    assert company.company_name == company_name

def test_get_company(session):
    company_name = "Test Company"
    created_company = CompanyModel.add_company(session, company_name)
    fetched_company = CompanyModel.get_company(session, created_company.id)
    assert fetched_company is not None
    assert fetched_company.id == created_company.id
    assert fetched_company.company_name == company_name


def test_get_companies(session):
    company_name_1 = "Test Company 1"
    company_name_2 = "Test Company 2"
    CompanyModel.add_company(session, company_name_1)
    CompanyModel.add_company(session, company_name_2)
    companies = CompanyModel.get_companies(session)
    assert len(companies) == 2
    assert companies[0].company_name in [company_name_1, company_name_2]
    assert companies[1].company_name in [company_name_1, company_name_2]
    

def test_update_company(session):
    company_name = "Test Company"
    new_company_name = "Updated Company"
    created_company = CompanyModel.add_company(session, company_name)
    updated_company = CompanyModel.update_company(session, created_company.id, new_company_name)
    assert updated_company.company_name == new_company_name


def test_delete_company(session):
    company_name = "Test Company"
    created_company = CompanyModel.add_company(session, company_name)
    CompanyModel.delete_company(session, created_company.id)
    deleted_company = CompanyModel.get_company(session, created_company.id)
    assert deleted_company is None
