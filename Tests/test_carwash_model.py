from src.models.carwash_model import CarWashModel
def test_add_carwash(session):
    carwash_name = "Sparkle Clean"
    location = "123 Main St"
    carwash = CarWashModel.add_carwash(session, carwash_name, location)
    assert carwash.id is not None
    assert carwash.carwash_name == carwash_name
    assert carwash.location == location

def test_get_carwash(session):
    carwash_name = "Sparkle Clean"
    location = "123 Main St"
    created_carwash = CarWashModel.add_carwash(session, carwash_name, location)
    fetched_carwash = CarWashModel.get_by_id(session, created_carwash.id)
    assert fetched_carwash is not None
    assert fetched_carwash.id == created_carwash.id
    assert fetched_carwash.carwash_name == carwash_name
    assert fetched_carwash.location == location

def test_get_carwashes(session):
    carwash_name_1 = "Sparkle Clean"
    location_1 = "123 Main St"
    carwash_name_2 = "Shiny Wash"
    location_2 = "456 Elm St"
    CarWashModel.add_carwash(session, carwash_name_1, location_1)
    CarWashModel.add_carwash(session, carwash_name_2, location_2)
    carwashes = CarWashModel.get_all(session)
    assert len(carwashes) == 2
    assert carwashes[0].carwash_name in [carwash_name_1, carwash_name_2]
    assert carwashes[1].carwash_name in [carwash_name_1, carwash_name_2]

def test_update_carwash(session):
    carwash_name = "Sparkle Clean"
    location = "123 Main St"
    new_carwash_name = "Updated Clean"
    created_carwash = CarWashModel.add_carwash(session, carwash_name, location)
    updated_carwash = CarWashModel.update_by_id(session, created_carwash.id, carwash_name=new_carwash_name)
    assert updated_carwash.carwash_name == new_carwash_name

def test_delete_carwash(session):
    carwash_name = "Sparkle Clean"
    location = "123 Main St"
    created_carwash = CarWashModel.add_carwash(session, carwash_name, location)
    CarWashModel.delete_by_id(session, created_carwash.id)
    deleted_carwash = CarWashModel.get_by_id(session, created_carwash.id)
    assert deleted_carwash is None