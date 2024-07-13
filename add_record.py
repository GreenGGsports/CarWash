from config import Config 
from database import create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.reservation_model import ReservationModel
from src.models.carwash_model import CarWashModel
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

def create_test_db(session):
    session = create_session()
    add_carwash_test(session)
    
    session.close()
# Example usage
if __name__ == '__main__':
    session = create_session()
    create_database(engine=engine)
    
    add_carwash_test(session=session)
