from sqlalchemy import create_engine
from src.models.base import BaseModel
from src.models.reservation_model import ReservationModel
from src.models.service_model import ServiceModel
from src.models.company_model import CompanyModel
from src.models.slot_model import SlotModel
from src.models.user_model import UserModel
from src.models.carwash_model import CarWashModel


def create_database(engine,db_path):
    BaseModel.metadata.create_all(engine)
    print("Database created successfully.")

if __name__ == '__main__':
    create_database()