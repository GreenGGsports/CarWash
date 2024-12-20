import pytest
from unittest.mock import MagicMock
from datetime import datetime, time, timedelta
from src.models.carwash_model import CarWashModel
from src.models.slot_model import SlotModel


@pytest.fixture
def db_session():
    return MagicMock()


@pytest.fixture
def carwash():
    return CarWashModel(
        id=1,
        carwash_name="Test Carwash",
        location="Test Location",
        contact="123456789",
        start_time=time(8, 0),
        end_time=time(20, 0),
        capacity=10
    )


def test_add_slot(db_session, carwash):
    start_time = datetime(2024, 12, 19, 9, 0)
    end_time = datetime(2024, 12, 19, 10, 0)
    carwash.add_slot(db_session, start_time, end_time)
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()


def test_get_live_slots(db_session, carwash):
    # Mock query és annak metódusai
    mock_query = MagicMock()
    mock_slots = [SlotModel(id=1), SlotModel(id=2)]
    mock_query.filter_by.return_value.all.return_value = mock_slots
    db_session.query.return_value = mock_query

    live_slots = carwash.get_live_slots(db_session)

    assert live_slots == mock_slots
    mock_query.filter_by.assert_called_once_with(carwash_id=carwash.id, live=True)


def test_get_live_slot_count(db_session, carwash):
    # Mock query és annak metódusai
    mock_query = MagicMock()
    mock_query.filter_by.return_value.count.return_value = 5
    db_session.query.return_value = mock_query

    slot_count = carwash.get_live_slot_count(db_session)

    assert slot_count == 5
    mock_query.filter_by.assert_called_once_with(carwash_id=carwash.id, live=True)


def test_archive_current_slots(db_session, carwash):
    carwash.archive_current_slots(db_session)
    db_session.query().filter_by.assert_called_once_with(carwash_id=carwash.id, live=True)
    db_session.query().filter_by().update.assert_called_once_with({'live': False})
    db_session.commit.assert_called_once()


def test_create_default_slots(db_session, carwash):
    start_time = time(8, 0)
    end_time = time(12, 0)
    slot_count = 4

    carwash.create_default_slots(db_session, start_time, end_time, slot_count)

    # Ellenőrizzük, hogy a helyes számú slot lett-e hozzáadva
    assert db_session.add.call_count == slot_count
    db_session.commit.assert_called_once()


def test_create_default_slots_invalid_time(db_session, carwash):
    start_time = time(12, 0)
    end_time = time(8, 0)
    slot_count = 4

    with pytest.raises(ValueError, match="End time must be after start time."):
        carwash.create_default_slots(db_session, start_time, end_time, slot_count)


def test_update_default_slots(db_session, carwash):
    start_time = time(8, 0)
    end_time = time(12, 0)
    slot_count = 4

    # Mock az archiváláshoz
    carwash.archive_current_slots = MagicMock()
    carwash.create_default_slots = MagicMock()

    carwash.update_default_slots(db_session, start_time, end_time, slot_count)

    # Ellenőrizzük, hogy az archiválás és az új slotok létrehozása meghívódott
    carwash.archive_current_slots.assert_called_once_with(db_session)
    carwash.create_default_slots.assert_called_once_with(db_session, start_time, end_time, slot_count)


def test_is_open_within_closed_period(db_session, carwash):
    carwash.close_start = datetime(2024, 12, 24)
    carwash.close_end = datetime(2024, 12, 26)

    date = datetime(2024, 12, 25)

    assert not carwash.is_open(db_session, date)


def test_is_open_outside_closed_period(db_session, carwash):
    carwash.close_start = datetime(2024, 12, 24)
    carwash.close_end = datetime(2024, 12, 26)

    date = datetime(2024, 12, 27)

    assert carwash.is_open(db_session, date)


def test_is_open_no_closure_dates(db_session, carwash):
    carwash.close_start = None
    carwash.close_end = None

    date = datetime(2024, 12, 25)

    assert carwash.is_open(db_session, date)
