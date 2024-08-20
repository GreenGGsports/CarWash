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
from src.views.service_admin import ServiceModelView
from src.controllers.admin_index_view import AdminIndexView
from src.controllers.local_admin_index_view import LocalAdminIndexView
from src.views.extra_admin_view import ExtraModelView
from src.controllers.developer_index_view import DeveloperIndexView

def init_admin(app, session_factory):
    admin = Admin(
        app,
        name='Admin Panel',
        template_mode='bootstrap3',
        index_view=AdminIndexView(url='/admin', endpoint='admin')
    )

    session = session_factory.get_session()

    # Admin view registration
    admin.add_view(ReservationAdminView(ReservationModel, session, name='Foglalások', endpoint='reservation_admin'))
    admin.add_view(ServiceModelView(ServiceModel, session, name='Csomagok', endpoint='service_admin'))
    admin.add_view(ExtraModelView(ExtraModel, session, name='Extrák', endpoint='extra_admin'))
    admin.add_view(ModelView(CompanyModel, session, name='Cégek', endpoint='company_admin'))
    admin.add_view(ModelView(CarWashModel, session, name='Autómosók', endpoint='carwash_admin'))

    admin.add_view(ModelView(BillingModel, session, name='Számlák', endpoint='billing_admin'))
    
    admin.add_view(MonthlyInvoiceView(session=session, name='Havi számlázás', endpoint='monthly_invoices'))

    session.close()

def init_local_admin(app, session_factory):
    local_admin = Admin(
        app,
        name='Local Admin Panel',
        template_mode='bootstrap3',
        index_view=LocalAdminIndexView(url='/local-admin', endpoint='local_admin')
    )

    session = session_factory.get_session()

    # Local Admin view registration
    local_admin.add_view(ReservationAdminView(ReservationModel, session, name='Foglalások', endpoint='local_reservation_admin'))
    local_admin.add_view(ServiceModelView(ServiceModel, session, name='Csomagok', endpoint='local_service_admin'))
    local_admin.add_view(ExtraModelView(ExtraModel, session, name='Extrák', endpoint='local_extra_admin'))

    session.close()

def init_developer_admin(app, session_factory):
    session = session_factory.get_session()

    developer_admin = Admin(
        app,
        name = 'Developer Admin Panel',
        template_mode='bootstrap3',
        index_view=DeveloperIndexView(url='/developer', endpoint='developer')
    )
    developer_admin.add_view(ModelView(ReservationModel, session, name='Reservation', endpoint='reservation_developer'))
    developer_admin.add_view(ModelView(UserModel, session, name='User', endpoint='user_developer'))
    developer_admin.add_view(ModelView(SlotModel, session, name='Slot', endpoint='slot_developer'))
    developer_admin.add_view(ModelView(ServiceModel, session, name='Service', endpoint='service_developer'))
    developer_admin.add_view(ModelView(CompanyModel, session, name='Company', endpoint='company_developer'))
    developer_admin.add_view(ModelView(CarWashModel, session, name='Carwash', endpoint='carwash_developer'))
    developer_admin.add_view(ModelView(ExtraModel, session, name='Extras', endpoint='extra_developer'))
    developer_admin.add_view(ModelView(CustomerModel, session, name='Customer', endpoint='customer_developer'))
    developer_admin.add_view(ModelView(BillingModel, session, name='Billing', endpoint='billing_developer'))
    developer_admin.add_view(ModelView(CarModel, session, name='Car', endpoint='car_developer'))
    
    developer_admin.add_view(MonthlyInvoiceView(session=session, name='Monthly Invoices', endpoint='monthly_invoices_developer'))

    session.close()


