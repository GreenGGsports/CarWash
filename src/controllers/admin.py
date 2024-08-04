from flask_admin import Admin
from src.models.reservation_model import ReservationModel
from src.models.customer_model import CustomerModel
from src.models.car_model import CarModel
from src.models.billing_model import BillingModel
from src.models.service_model import ServiceModel
from src.models.company_model import CompanyModel
from src.models.slot_model import SlotModel
from src.models.user_model import UserModel
from src.models.carwash_model import CarWashModel
from src.models.extra_model import ExtraModel
from flask_admin.contrib.sqla import ModelView
from src.views.company_admin import  MonthlyInvoiceView
from src.views.reservation_admin import ReservationAdminView

class ServiceModelView(ModelView):
    column_labels = {
        'carwash.carwash_name': 'Car Wash Name',
        'service_name': 'Service Name',
        'price_small': 'Price (Small)',
        'price_large': 'Price (Large)'
    }

    column_list = ['carwash.carwash_name', 'service_name', 'price_small', 'price_large']




def init_admin(app, session_factory):
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

    session = session_factory.get_session()

    # Admin view registration
    admin.add_view(ReservationAdminView(ReservationModel, session))
    admin.add_view(ModelView(UserModel, session))
    admin.add_view(ModelView(SlotModel, session))
    admin.add_view(ServiceModelView(ServiceModel, session))
    admin.add_view(ModelView(CompanyModel, session))
    admin.add_view(ModelView(CarWashModel, session))
    admin.add_view(ModelView(ExtraModel, session))
    admin.add_view(ModelView(CustomerModel, session))
    admin.add_view(ModelView(BillingModel, session))
    admin.add_view(ModelView(CarModel, session))
    
    admin.add_view(MonthlyInvoiceView(session= session, name='Monthly Invoices', endpoint='monthly_invoices'))

    session.close()