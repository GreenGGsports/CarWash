from flask import current_app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import joinedload
from src.models.user_model import UserModel  # Importáld a szükséges modelleket
from src.models.reservation_model import ReservationModel
from src.models.slot_model import SlotModel
from src.models.service_model import ServiceModel
from src.models.company_model import CompanyModel
from src.models.extra_model import ExtraModel
from src.models.carwash_model import CarWashModel

class ServiceModelView(ModelView):
    column_labels = {
        'carwash.carwash_name': 'Car Wash Name',  # Itt adod meg az egyedi nevet
        'service_name': 'Service Name',
        'price_small': 'Price (Small)',
        'price_large': 'Price (Large)'
    }

    column_list = ['carwash.carwash_name', 'service_name', 'price_small', 'price_large']

class ReservationModelView(ModelView):
    column_labels = {
        'carwash.carwash_name': 'Car Wash Name',
        'reservation_date': 'Reservation Date',
        'service.service_name': 'Service Name',
        'car_type': 'Car Type',
        'parking_spot': 'Parking Spot',
        'final_price': 'Final Price',
        'extras': 'Extras'
    }
    column_list = [
        'carwash.carwash_name', 
        'reservation_date', 
        'service.service_name', 
        'car_type', 
        'parking_spot', 
        'final_price',
        'extras'
    ]

    def _list_extras(view, context, model, name):
        return ', '.join([extra.service_name for extra in model.extras])

    column_formatters = {
        'extras': _list_extras
    }

    # def create_model(self, form):
    #     model = self.model()
    #     form.populate_obj(model)
    #     session = current_app.session_factory.get_session()

    #     # Calculate final price
    #     final_price = ReservationModel.calculate_final_price(
    #         session,
    #         model.service_id,
    #         model.car_type,
    #         [extra.id for extra in model.extras],
    #         model.company_id
    #     )

    #     model.final_price = final_price

    #     try:
    #         session.add(model)
    #         session.commit()
    #     except Exception as ex:
    #         session.rollback()
    #         raise ex
    #     finally:
    #         session.close()
    
def init_admin(app):   
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

    admin.add_view(ModelView(UserModel, app.session_factory.get_session()))
    admin.add_view(ReservationModelView(ReservationModel, app.session_factory.get_session()))
    admin.add_view(ModelView(SlotModel, app.session_factory.get_session()))
    admin.add_view(ServiceModelView(ServiceModel, app.session_factory.get_session()))
    admin.add_view(ModelView(CompanyModel, app.session_factory.get_session()))
    admin.add_view(ModelView(CarWashModel, app.session_factory.get_session()))
    admin.add_view(ModelView(ExtraModel, app.session_factory.get_session()))