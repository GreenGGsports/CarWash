from src.models.company_model import CompanyModel
from src.models.reservation_model import ReservationModel
from src.models.service_model import ServiceModel

from src.models.base import Base
from sqlalchemy_utils import database_exists

def create_database(engine):
    # Create database if it doesn't exist
    if not database_exists(engine.url):
        Base.metadata.create_all(engine)
        print("Database created.")