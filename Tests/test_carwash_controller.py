import pytest
from flask import Flask
from unittest.mock import MagicMock, patch
from src.controllers.carwash_controller import carwash_ctrl


# Fixture for Flask app
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(carwash_ctrl)
    app.session_factory = MagicMock()
    app.logger = MagicMock()
    app.secret_key = "test_key"
    yield app


# Fixture for test client
@pytest.fixture
def client(app):
    return app.test_client()


# Fixture for mocking database session
@pytest.fixture
def db_session(app):
    session = MagicMock()
    app.session_factory.get_session.return_value = session
    return session


# Test for /carwash/list endpoint - success case
@patch('src.models.carwash_model.CarWashModel.get_all')
def test_get_carwashes_success(mock_get_all, client, db_session):
    # Mock the database response
    mock_carwashes = [
        MagicMock(id=1, location="Test Location 1", image_name="image1.jpg"),
        MagicMock(id=2, location="Test Location 2", image_name="image2.jpg"),
    ]
    mock_get_all.return_value = mock_carwashes

    response = client.get('/carwash/list')

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['id'] == 1
    assert data[0]['location'] == "Test Location 1"
    assert data[0]['image_name'] == "image1.jpg"
    assert data[1]['id'] == 2
    assert data[1]['location'] == "Test Location 2"
    assert data[1]['image_name'] == "image2.jpg"


# Test for /carwash/list endpoint - failure case
@patch('src.models.carwash_model.CarWashModel.get_all')
def test_get_carwashes_failure(mock_get_all, client, db_session):
    # Simulate a database error
    mock_get_all.side_effect = Exception("DB error")

    response = client.get('/carwash/list')

    assert response.status_code == 500
    assert response.is_json
    data = response.get_json()
    assert data['error'] == 'Failed to retrieve carwashes.'


# Test for /carwash/select endpoint - success case
@patch('src.models.carwash_model.CarWashModel.get_by_id')
def test_select_carwash_success(mock_get_by_id, client, db_session):
    # Mock the database response
    mock_carwash = MagicMock(id=1)
    mock_get_by_id.return_value = mock_carwash

    response = client.post('/carwash/select', json={'id': 1})

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'Helyszín kiválasztva!'
    assert data['id'] == 1


# Test for /carwash/select endpoint - carwash not found
@patch('src.models.carwash_model.CarWashModel.get_by_id')
def test_select_carwash_not_found(mock_get_by_id, client, db_session):
    # Simulate carwash not found
    mock_get_by_id.return_value = None

    response = client.post('/carwash/select', json={'id': 999})

    assert response.status_code == 404
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'Carwash not found!'


# Test for /carwash/select endpoint - missing ID
def test_select_carwash_missing_id(client, db_session):
    response = client.post('/carwash/select', json={})  # No ID provided

    assert response.status_code == 400
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'Hiányzó azonosító!'


# Test for /carwash/select endpoint - invalid ID format
@patch('src.models.carwash_model.CarWashModel.get_by_id')
def test_select_carwash_invalid_id(mock_get_by_id, client, db_session):
    response = client.post('/carwash/select', json={'id': 'invalid'})  # Invalid ID format

    assert response.status_code == 400
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'Invalid carwash ID format.'
