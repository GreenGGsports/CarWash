import pytest
from unittest.mock import MagicMock, patch
from flask import Flask, session
from flask_login import LoginManager, UserMixin
from datetime import datetime, timedelta
from src.controllers.booking_controller import booking_ctrl, get_available_slots
from src.models.slot_model import SlotModel
from src.models.slot_lock_model import SlotLockModel
from src.models.reservation_model import ReservationModel


# Mock User class for Flask-Login
class MockUser(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(booking_ctrl)
    app.secret_key = 'test_secret'

    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return MockUser(user_id)  # Mock user loader

    app.session_factory = MagicMock()  # Mockolt session factory
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session():
    return MagicMock()


@pytest.fixture
def mock_user():
    return MockUser(user_id=123)


def test_reserve_slot(client, db_session, mock_user):
    db_session.query.return_value.filter.return_value.first.return_value = None  # No lock exists

    # Mock current_user
    with patch('src.controllers.booking_controller.current_user', mock_user):
        with patch('src.controllers.booking_controller.current_app.session_factory.get_session', return_value=db_session):
            response = client.post('/booking/api/carwash/reserve_slot', json={
                'slot_id': 1,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['message'] == 'A slot tartalékban van, 10 percig foglalva.'


def test_reserve_slot_already_locked(client, db_session, mock_user):
    # Mock an existing slot lock
    mock_slot_lock = MagicMock(user_id=999, locked_until=datetime.now() + timedelta(minutes=5))
    db_session.query.return_value.filter.return_value.first.return_value = mock_slot_lock

    # Mock current_user
    with patch('src.controllers.booking_controller.current_user', mock_user):
        with patch('src.controllers.booking_controller.current_app.session_factory.get_session', return_value=db_session):
            response = client.post('/booking/api/carwash/reserve_slot', json={
                'slot_id': 1,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is False
    assert data['message'] == 'A slot már tartalékban van másik felhasználó által.'
