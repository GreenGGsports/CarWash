from src.models.service_model import ServiceModel

def test_create_service(session):
    service_name = "Test Service"
    price = 100
    price_medium = 110  # Állítsd be az árakat egész számokra
    carwash_id = 1
    service = ServiceModel.add_service(session, service_name, price, price, price_medium, carwash_id)
    assert service.id is not None
    assert service.service_name == service_name
    assert service.price_small == price
    assert service.price_medium == price_medium

def test_get_service(session):
    service_name = "Test Service"
    price = 100
    price_medium = 110  # Használj egész számot
    carwash_id = 1
    created_service = ServiceModel.add_service(session, service_name, price, price, price_medium, carwash_id)
    fetched_service = ServiceModel.get_by_id(session, created_service.id)
    assert fetched_service is not None
    assert fetched_service.id == created_service.id
    assert fetched_service.service_name == service_name
    assert fetched_service.price_small == price
    assert fetched_service.price_medium == price_medium

def test_get_services(session):
    service_name_1 = "Test Service 1"
    price_1_small = 100
    price_1_large = 120
    price_1_medium = 110
    service_name_2 = "Test Service 2"
    price_2_small = 200
    price_2_large = 200
    price_2_medium = 210
    carwash_id = 1
    ServiceModel.add_service(session, service_name_1, price_1_small, price_1_large, price_1_medium, carwash_id)
    ServiceModel.add_service(session, service_name_2, price_2_small, price_2_large, price_2_medium, carwash_id)
    services = ServiceModel.get_all(session)
    assert len(services) == 2
    assert services[0].service_name in [service_name_1, service_name_2]
    assert services[1].service_name in [service_name_1, service_name_2]
