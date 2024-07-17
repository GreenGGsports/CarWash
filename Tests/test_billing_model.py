import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from src.models.base import BaseModel  # Adjust the import path as per your project structure
from src.models.billing_model import BillingModel  # Adjust the import path as per your project structure

@pytest.fixture(scope='module')
def engine():
    return create_engine('sqlite:///:memory:')


@pytest.fixture(scope='module')
def tables(engine):
    BaseModel.metadata.create_all(engine)
    yield
    BaseModel.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def session(engine):
    BaseModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    BaseModel.metadata.drop_all(engine)

# Test cases for BillingModel
def test_add_billing_data(session):
    # Arrange
    license_plate = "ABC123"
    name = "John Doe"
    address = "123 Main St"
    email = "john.doe@example.com"
    company_name = "XYZ Inc."
    tax_ID = "123456"

    # Act
    billing_data = BillingModel.add_billing_data(
        session, license_plate, name, address, email, company_name, tax_ID
    )

    # Assert
    assert billing_data.id is not None
    assert billing_data.license_plate == license_plate
    assert billing_data.name == name
    assert billing_data.address == address
    assert billing_data.email == email
    assert billing_data.company_name == company_name
    assert billing_data.tax_ID == tax_ID

def test_get_by_license_plate(session):
    # Arrange
    license_plate = "ABC123"
    name = "John Doe"
    address = "123 Main St"
    email = "john.doe@example.com"
    company_name = "XYZ Inc."
    tax_ID = "123456"

    BillingModel.add_billing_data(
        session, license_plate, name, address, email, company_name, tax_ID
    )

    # Act
    result = BillingModel.get_first_by_license_plate(session, license_plate)

    # Assert
    assert result is not False
    

def test_get_by_license_plate_not_found(session):
    # Arrange
    license_plate = "XYZ789"

    # Act
    result = BillingModel.get_first_by_license_plate(session, license_plate)

    # Assert
    assert result is False
