from src.models.service_model import ServiceModel

def test_create_service(session):
    service_name = "Test Service"
    price = 100
    carwash_id =  1 
    service = ServiceModel.add_service(session, service_name, price, price, carwash_id)
    assert service.id is not None
    assert service.service_name == service_name
    assert service.price_small == price

def test_get_service(session):
    service_name = "Test Service"
    price = 100
    carwash_id =  1 
    created_service = ServiceModel.add_service(session, service_name, price, price,carwash_id)
    fetched_service = ServiceModel.get_by_id(session, created_service.id)
    assert fetched_service is not None
    assert fetched_service.id == created_service.id
    assert fetched_service.service_name == service_name
    assert fetched_service.price_small == price

def test_get_services(session):
    service_name_1 = "Test Service 1"
    price_1_small = 100
    price_1_large = 120
    service_name_2 = "Test Service 2"
    price_2_small = 200
    price_2_large = 200
    carwash_id =  1 
    ServiceModel.add_service(session, service_name_1, price_1_small, price_1_large, carwash_id)
    ServiceModel.add_service(session, service_name_2, price_2_small, price_2_large, carwash_id)
    services = ServiceModel.get_all(session)
    assert len(services) == 2
    assert services[0].service_name in [service_name_1, service_name_2]
    assert services[1].service_name in [service_name_1, service_name_2]

def test_update_service(session):
    service_name = "Test Service"
    price = 100
    new_service_name = "Updated Service"
    new_price = 150
    carwash_id = 1
    created_service = ServiceModel.add_service(session, service_name, price, price, carwash_id)
    updated_service = ServiceModel.update_by_id(session, created_service.id, service_name=new_service_name, price_small=new_price)
    assert updated_service.service_name == new_service_name
    assert updated_service.price_small == new_price

def test_delete_service(session):
    service_name = "Test Service"
    price = 100
    carwash_id = 1
    created_service = ServiceModel.add_service(session, service_name, price, price, carwash_id)
    ServiceModel.delete_by_id(session, created_service.id)
    deleted_service = ServiceModel.get_by_id(session, created_service.id)
    assert deleted_service is None
    
def test_get_services_by_carwash_id(session):
    carwash_id = 1

    # Hozzáadunk szolgáltatásokat különböző autómosókhoz
    ServiceModel.add_service(session, "Service 1", 100, 120, carwash_id)
    ServiceModel.add_service(session, "Service 2", 200, 200, carwash_id)
    ServiceModel.add_service(session, "Service 3", 150, 180, carwash_id + 1)  # Másik autómosóhoz tartozó szolgáltatás

    # Lekérdezzük az autómosóhoz tartozó szolgáltatásokat, használva a filter_by_column_value metódust
    services_carwash_1 = ServiceModel.filter_by_column_value(session, 'carwash_id', carwash_id)

    # Ellenőrzünk
    assert len(services_carwash_1) == 2
    assert all(service.carwash_id == carwash_id for service in services_carwash_1)

    # Ellenőrizzük, hogy a másik autómosóhoz tartozó szolgáltatás ne legyen benne
    assert all(service.carwash_id != carwash_id + 1 for service in services_carwash_1)
