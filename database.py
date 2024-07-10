from src.models.slot_model import SlotModel
from src.models.reservation_model import ReservationModel
from src.models.service_model import ServiceModel
from src.models.company_model import CompanyModel
from src.models.user_model import UserModel
from src.models.carwash_model import CarWashModel
from src.models.extra_model import ExtraModel
from src.models.reservation_extras import reservation_extra

from src.models.base import BaseModel
from sqlalchemy_utils import database_exists

def create_database(engine):
    # Create database if it doesn't exist
    if not database_exists(engine.url):
        BaseModel.metadata.create_all(engine)
        print("Database created.")