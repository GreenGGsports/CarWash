import pytest
from flask import jsonify
from add_record import add_carwash_test

@pytest.fixture(scope='function')
def session(client):
    return client.application.session_factory.get_session()

def test_get_carwashes(client, session):
    session = client.application.session_factory.get_session()
    add_carwash_test(session)
    # Test for /carwash/list endpoint
    response = client.get('/carwash/list')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)  # Assuming it returns a list of dictionaries
    assert len(data) > 0  # Ensure some data is returned

def test_select_carwash(client, session):
    # Test for /carwash/select endpoint
    data = {'id': 1}  # Replace with a valid carwash ID
    response = client.post('/carwash/select', json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Helyszín kiválasztva!'
    assert 'id' in data
    assert data['id'] == 1  # Ensure the ID returned matches the one sent in the request
