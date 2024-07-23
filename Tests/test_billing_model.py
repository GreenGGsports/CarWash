import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from src.models.base import BaseModel  # Adjust the import path as per your project structure
from src.models.billing_model import BillingModel  # Adjust the import path as per your project structure
# Test cases for BillingModel
def test_add_billing_data(session):
    # Arrange
    name = "John Doe"
    address = "123 Main St"
    email = "john.doe@example.com"
    company_name = "XYZ Inc."
    tax_ID = "123456"

    # Act
    billing_data = BillingModel.add(
        session=session, 
        name = name, 
        address = address, 
        email = email,
        company_name = company_name,
        tax_ID = tax_ID
    )

    # Assert
    assert billing_data.id is not None
    assert billing_data.name == name
    assert billing_data.address == address
    assert billing_data.email == email
    assert billing_data.company_name == company_name
    assert billing_data.tax_ID == tax_ID