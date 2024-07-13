from flask import current_app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from src.models.user_model import UserModel  # Importáld a szükséges modelleket
from src.models.reservation_model import ReservationModel
from src.models.slot_model import SlotModel
from src.models.service_model import ServiceModel
from src.models.company_model import CompanyModel
from src.models.extra_model import ExtraModel
from src.models.carwash_model import CarWashModel

def init_admin(app):   
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

    admin.add_view(ModelView(UserModel, app.session_factory.get_session()))
    admin.add_view(ModelView(ReservationModel, app.session_factory.get_session()))
    admin.add_view(ModelView(SlotModel, app.session_factory.get_session()))
    admin.add_view(ModelView(ServiceModel, app.session_factory.get_session()))
    admin.add_view(ModelView(CompanyModel, app.session_factory.get_session()))
    admin.add_view(ModelView(ExtraModel, app.session_factory.get_session()))