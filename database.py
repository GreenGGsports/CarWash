from sqlalchemy import create_engine
from src.models.base import BaseModel
from src.models.billing_model import BillingModel
from src.models.reservation_model import ReservationModel
from src.models.service_model import ServiceModel
from src.models.company_model import CompanyModel
from src.models.slot_model import SlotModel
from src.models.user_model import UserModel
from src.models.carwash_model import CarWashModel
from src.models.extra_model import ExtraModel
from src.models.reservation_extras import reservation_extra
from src.models.customer_model import CustomerModel
from src.models.car_model import CarModel



def create_database(engine):
    BaseModel.metadata.create_all(engine)
    print("Database created successfully.")


if __name__ == '__main__':
    create_database()
    