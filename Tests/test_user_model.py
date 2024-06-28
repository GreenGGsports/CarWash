import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import BaseModel  # Adjust the import path as per your project structure
from src.models.user_model import UserModel  # Adjust the import path as per your project structure

@pytest.fixture(scope='module')
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture(scope='module')
def tables(engine):
    BaseModel.metadata.create_all(engine)
    yield
    BaseModel.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

# Test cases for UserModel
def test_add_user(session):
    # Arrange
    user_name = "test_user"
    password = "test_password"

    # Act
    user = UserModel.add_user(session, user_name, password)

    # Assert
    assert user.id is not None
    assert user.user_name == user_name
    assert user.password_hash != password  # Ensure password is hashed

def test_login_success(session):
    # Arrange
    user_name = "test_user"
    password = "test_password"
    UserModel.add_user(session, user_name, password)

    # Act
    user = UserModel.login(session, user_name, password)

    # Assert
    assert user is not False
    assert user.user_name == user_name

def test_login_failure(session):
    # Arrange
    user_name = "test_user"
    password = "test_password"
    wrong_password = "wrong_password"
    UserModel.add_user(session, user_name, password)

    # Act
    result = UserModel.login(session, user_name, wrong_password)

    # Assert
    assert result is False

def test_check_name_taken_true(session):
    # Arrange
    user_name = "test_user"
    password = "test_password"
    UserModel.add_user(session, user_name, password)

    # Act
    is_taken = UserModel.check_name_taken(session, user_name)

    # Assert
    assert is_taken is True

def test_check_name_taken_false(session):
    # Arrange
    user_name = "non_existent_user"

    # Act
    is_taken = UserModel.check_name_taken(session, user_name)

    # Assert
    assert is_taken is False
