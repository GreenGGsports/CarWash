import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.user_model import UserModel  
@pytest.fixture
def session():
    # Creating a mock session
    return MagicMock(spec=Session)

@pytest.fixture
def user_data():
    return {
        'id': 1,
        'user_name': 'testuser',
        'password': 'testpassword'
    }

def test_add_user(session, user_data):
    with patch('your_module.generate_password_hash') as mock_generate_password_hash:
        mock_generate_password_hash.return_value = 'hashedpassword'
        
        user = UserModel.add_user(session, user_data['user_name'], user_data['password'])
        
        session.add.assert_called_once_with(user)
        session.commit.assert_called_once()
        assert user.user_name == user_data['user_name']
        assert user.password_hash == 'hashedpassword'

def test_login_success(session, user_data):
    with patch('your_module.check_password_hash') as mock_check_password_hash:
        mock_check_password_hash.return_value = True
        
        user = UserModel(
            id=user_data['id'], 
            user_name=user_data['user_name'], 
            password_hash=generate_password_hash(user_data['password'])
        )
        session.query.return_value.filter.return_value.first.return_value = user
        
        logged_in_user = UserModel.login(session, user_data['user_name'], user_data['password'])
        
        assert logged_in_user == user

def test_login_failure(session, user_data):
    with patch('your_module.check_password_hash') as mock_check_password_hash:
        mock_check_password_hash.return_value = False
        
        user = UserModel(
            id=user_data['id'], 
            user_name=user_data['user_name'], 
            password_hash=generate_password_hash(user_data['password'])
        )
        session.query.return_value.filter.return_value.first.return_value = user
        
        logged_in_user = UserModel.login(session, user_data['user_name'], user_data['password'])
        
        assert logged_in_user == False

def test_check_name_taken(session, user_data):
    session.query.return_value.filter.return_value.first.return_value = UserModel(
        id=user_data['id'], 
        user_name=user_data['user_name'], 
        password_hash=generate_password_hash(user_data['password'])
    )
    
    is_taken = UserModel.check_name_taken(session, user_data['user_name'])
    
    assert is_taken == True

def test_check_name_not_taken(session):
    session.query.return_value.filter.return_value.first.return_value = None
    
    is_taken = UserModel.check_name_taken(session, 'newuser')
    
    assert is_taken == False
