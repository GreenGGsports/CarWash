BLUEPRINT_ROUTE = '/user'
LOGIN = '/login'
ADD = '/add_user'

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
    assert response.status_code == 200
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
    assert response.status_code == 302 #the logout route can't be reached if not logged in

def test_add_user_successful(client):
    # Simulate adding a new user
    response = client.post(BLUEPRINT_ROUTE + ADD, json={
        'user_name': 'newuser',
        'password': 'newpassword'
    })
    assert response.status_code == 200
    assert b'success' in response.data

def test_add_user_failed_existing_username(client):
    # Simulate adding a user with an existing username
    response = client.post(BLUEPRINT_ROUTE + ADD, json={
        'user_name': 'testuser',
        'password': 'newpassword'
    })
    response = client.post(BLUEPRINT_ROUTE + ADD, json={
        'user_name': 'testuser',
        'password': 'newpassword'
    })
    assert response.status_code == 200
    assert b'failed' in response.data
