from flask import current_app
from src.models.user_model import UserModel
from sessions import SessionFactory  

BLUEPRINT_ROUTE = '/user'
LOGIN = '/login'
ADD = '/add_user'

def setup_function():
    """Törli a felhasználót az adatbázisból a teszt előtt, ha már létezik."""
    db_session = current_app.session_factory.get_session()
    # Töröld a felhasználókat, ha már léteznek
    db_session.query(UserModel).filter_by(user_name='newuser1').delete()
    db_session.query(UserModel).filter_by(user_name='testuser').delete()
    db_session.commit()
    db_session.close()

def teardown_function():
    """Rollback a database changes to maintain test isolation."""
    db_session = current_app.session_factory.get_session()
    db_session.rollback()  # Visszavonja a tranzakciókat, hogy tisztán kezdődjenek a tesztek
    db_session.close()

def test_login_successful(client):
    # First, create the user with a POST request
    response = client.post(BLUEPRINT_ROUTE + ADD, json={
        'user_name': 'testuser',
        'password': 'testpassword'
    })
    
    # Now, log in with the created user
    response = client.post(BLUEPRINT_ROUTE + LOGIN, json={
        'user_name': 'testuser',
        'password': 'testpassword'
    })
    
    # Check the response
    assert response.status_code == 200
    assert b'logged_in' in response.data

def test_login_failed(client):
    # Simulate a failed login request
    response = client.post(BLUEPRINT_ROUTE + LOGIN, json={
        'user_name': 'nonexistent_user',
        'password': 'wrong_password'
    })
    assert response.status_code == 401
    assert b'failed' in response.data

def test_logout(client):
    client.post(BLUEPRINT_ROUTE + ADD, json={
        'user_name': 'testuser',
        'password': 'testpassword'
    })
    # Simulate a logout request after successful login
    client.post(BLUEPRINT_ROUTE + LOGIN, json={
        'user_name': 'testuser',
        'password': 'testpassword'
    })
    response = client.post(BLUEPRINT_ROUTE + '/logout')
    assert response.status_code == 200
    assert b'logged_out' in response.data

def test_logout_when_not_logged_in(client):
    # Simulate a logout request when not logged in
    response = client.post(BLUEPRINT_ROUTE + '/logout')
    assert response.status_code == 302 # the logout route can't be reached if not logged in

def test_add_user_successful(client):
    # Simulate adding a new user with role 'user'
    response = client.post(BLUEPRINT_ROUTE + ADD, json={
        'user_name': 'newuser1',
        'password': 'newpassword',
        'role': 'user',  # Ensure role is included if needed
    })
    assert response.status_code == 200
    assert b'success' in response.data

def test_add_user_failed_existing_username(client):
    # Simulate adding a user with an existing username
    db_session = current_app.session_factory.get_session()
    db_session.query(UserModel).filter_by(user_name='testuser').delete()  # Delete if exists
    db_session.commit()
    
    # First time user creation
    response = client.post(BLUEPRINT_ROUTE + ADD, json={
        'user_name': 'testuser',
        'password': 'newpassword'
    })
    
    # Try to add again with the same username (should fail)
    response = client.post(BLUEPRINT_ROUTE + ADD, json={
        'user_name': 'testuser',
        'password': 'newpassword'
    })
    
    # Assert the response should be "failed"
    assert response.status_code == 200
    assert b'failed' in response.data
