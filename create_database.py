from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import Base
from src.models.reservation_model import Reservation
from src.models.service_model import Service
from src.models.company_model import Company

def create_database():
    db_path = 'sqlite:///db/car_wash.db'
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    print("Database created successfully.")

if __name__ == '__main__':
    create_database()
