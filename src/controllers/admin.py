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
from src.models.customer_model import CustomerModel


class ServiceModelView(ModelView):
    column_labels = {
        'carwash.carwash_name': 'Car Wash Name',  # Itt adod meg az egyedi nevet
        'service_name': 'Service Name',
        'price_small': 'Price (Small)',
        'price_large': 'Price (Large)'
    }

    column_list = ['carwash.carwash_name', 'service_name', 'price_small', 'price_large']

class ReservationModelView(ModelView):


    column_list = (
        'reservation_date',
        'license_plate',
        'carwash.carwash_name',
        'service.service_name',
        'extras',
        'customer.forname',
        'customer.lastname',
        'customer.phone_number',
        'company.company_name',
        'final_price',
    )

    column_labels = {
        'reservation_date': 'Reservation Date',
        'license_plate': 'License Plate',
        'customer.forname': 'Forename',
        'customer.lastname': 'Lastname',
        'customer.phone_number': 'Phone Number',
        'company.company_name': 'Company Name',
        'service.service_name': 'Service Name',
         'extras': 'Extras',
        'carwash.carwash_name': 'Carwash Name',
        'final_price': 'Final Price',
    }

    column_sortable_list = (
        'reservation_date',
        ('customer', 'customer.forname'),
        ('customer', 'customer.lastname'),
        ('customer', 'customer.phone_number'),
        ('company', 'company.company_name'),
        ('service', 'service.service_name'),
        ('carwash', 'carwash.carwash_name'),
        'license_plate',
        'final_price'
    )

    column_searchable_list = (
        'license_plate',
        'customer.forname',
        'customer.lastname',
        'customer.phone_number',
        'company.company_name',
        'service.service_name',
        'carwash.carwash_name',
    )

    def _list_extras(view, context, model, name):
        return ', '.join([extra.service_name for extra in model.extras])

    column_formatters = {
        'extras': _list_extras
    }

    @staticmethod
    def _list_extras(view, context, model, name):
        return ', '.join([extra.service_name for extra in model.extras])

    column_formatters = {
        'extras': _list_extras
    }

    def create_model(self, form):
        model = self.model()
        form.populate_obj(model)
        
        try:
            # Számítjuk ki a végső árat a calculate_final_price segítségével
            final_price = ReservationModel.calculate_final_price(
                self.session,
                model.service.id,  # Használjuk a service objektum id attribútumát
                model.car_type,
                [extra.id for extra in model.extras],
                model.company.id  # Használjuk a company objektum id attribútumát
            )
            model.final_price = final_price

            self.session.add(model)
            self.session.commit()
            return model

        except Exception as ex:
            self.session.rollback()
            raise ex

        finally:
            self.session.close()


def init_admin(app):   
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

    admin.add_view(ModelView(UserModel, app.session_factory.get_session()))
    admin.add_view(ReservationModelView(ReservationModel, app.session_factory.get_session()))
    admin.add_view(ModelView(SlotModel, app.session_factory.get_session()))
    admin.add_view(ServiceModelView(ServiceModel, app.session_factory.get_session()))
    admin.add_view(ModelView(CompanyModel, app.session_factory.get_session()))
    admin.add_view(ModelView(CarWashModel, app.session_factory.get_session()))
    admin.add_view(ModelView(ExtraModel, app.session_factory.get_session()))
    admin.add_view(ModelView(CustomerModel, app.session_factory.get_session()))