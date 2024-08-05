from config import Config 
from database import create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.reservation_model import ReservationModel
from src.models.carwash_model import CarWashModel
from src.models.service_model import ServiceModel
from src.models.extra_model import ExtraModel
from src.models.slot_model import SlotModel
import datetime

db_path = Config.SQLALCHEMY_DATABASE_URI

engine = create_engine(db_path)
def create_session():
    Session = sessionmaker(bind=engine)
    return Session()

def add_carwash_test(session):
    carwash_name_1 = "Sparkle Clean"
    location_1 = "123 Main St"
    carwash_name_2 = "Shiny Wash"
    location_2 = "456 Elm St"
    CarWashModel.add_carwash(session=session,carwash_name=carwash_name_1, location=location_1)
    CarWashModel.add_carwash(session=session,carwash_name=carwash_name_2, location=location_2)
    session.close()

def add_service_test(session):
    service_name_1 = "Test Service 1"
    service_name_2 = "Test Service 2"
    price_1 = 100
    carwash_id_1 =  1 
    desription_1 = 'blablabla mosás, szőr szedés + barátság extrákkal szolgáltatás'
    ServiceModel.add_service(session, service_name_1, price_1, price_1, carwash_id_1 , desription_1)
    ServiceModel.add_service(session, service_name_2, price_1, price_1, carwash_id_1 , desription_1)
    
def add_extra_test(session):
    extras_data = [
        {"extra_name": "Waxing", "price": 50, "extra_type": "Basic", "carwash_id": 1},
        {"extra_name": "Polishing", "price": 80, "extra_type": "Advanced", "carwash_id": 1},
        {"extra_name": "Interior Cleaning", "price": 60, "extra_type": "Basic", "carwash_id": 2},
        {"extra_name": "Underbody Wash", "price": 70, "extra_type": "Advanced", "carwash_id": 2},
    ]
    
    for extra_data in extras_data:
        ExtraModel.add_extra(session=session, **extra_data)
        
def create_hourly_slots(session):
    start_time = datetime.datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    end_time = start_time.replace(hour=17)
    SlotModel.create_default_slots(session = session, start_time=start_time,end_time=end_time, slot_duration_minutes=60)
    session.close()
        
def create_test_db(session):
    session = create_session()
    add_carwash_test(session)
    
    session.close()
# Example usage
if __name__ == '__main__':
    session = create_session()
    #create_database(engine=engine)
    
    create_hourly_slots(session)
    #add_carwash_test(session=session)
    #add_service_test(session)
    #add_service_test(session)