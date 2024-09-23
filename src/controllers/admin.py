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
from src.views.company_admin import  MonthlyInvoiceView
from src.views.reservation_admin import ReservationAdminView
from src.views.service_admin import ServiceModelView
from src.controllers.admin_index_view import BaseAdminIndexView
from src.views.extra_admin_view import ExtraModelView
from src.views.my_modelview import MyModelView
from src.views.carwash_modelview import CarwashAdminView
from src.views.invoice_admin_view import InvoiceModelView
from src.views.dashboard import Dashboard
def init_admin(app, session_factory):
    admin = Admin(
        app,
        name='Admin Panel',
        template_mode='bootstrap3',
        index_view=BaseAdminIndexView(role='admin',url='/admin', endpoint='admin')
    )

    session = session_factory.get_session()

    # Admin view registration
    
    admin.add_view(ReservationAdminView(ReservationModel, session, name='Foglalások', endpoint='reservation_admin'))
    admin.add_view(ServiceModelView(ServiceModel, session, name='Csomagok', endpoint='service_admin'))
    admin.add_view(ExtraModelView(ExtraModel, session, name='Extrák', endpoint='extra_admin'))
    admin.add_view(MyModelView(CompanyModel, session, name='Cégek', endpoint='company_admin'))
    admin.add_view(CarwashAdminView(CarWashModel, session, name='Autómosók', endpoint='carwash_admin'))
    admin.add_view(MonthlyInvoiceView(session=session, name='Havi számlázás', endpoint='monthly_invoices'))
    admin.add_view(InvoiceModelView(BillingModel, session, name='Számlák', endpoint='billing_admin'))
    admin.add_view(Dashboard(ReservationModel, session, name='Dashboard', endpoint='dashboard'))
    
def init_local_admin(app, session_factory):
    local_admin = Admin(
        app,
        name='Local Admin Panel',
        template_mode='bootstrap3',
        index_view=BaseAdminIndexView(role='local_admin',url='/local-admin', endpoint='local_admin')
    )

    session = session_factory.get_session()

    # Local Admin view registration
    local_admin.add_view(ReservationAdminView(ReservationModel, session, name='Foglalások', endpoint='local_reservation_admin'))
    local_admin.add_view(ServiceModelView(ServiceModel, session, name='Csomagok', endpoint='local_service_admin'))
    local_admin.add_view(ExtraModelView(ExtraModel, session, name='Extrák', endpoint='local_extra_admin'))

def init_developer_admin(app, session_factory):
    session = session_factory.get_session()

    developer_admin = Admin(
        app,
        name = 'Developer Admin Panel',
        template_mode='bootstrap3',
        index_view=BaseAdminIndexView(role='developer', url='/developer', endpoint='developer')
    )
    developer_admin.add_view(MyModelView(ReservationModel, session, name='Reservation', endpoint='reservation_developer'))
    developer_admin.add_view(MyModelView(UserModel, session, name='User', endpoint='user_developer'))
    developer_admin.add_view(MyModelView(SlotModel, session, name='Slot', endpoint='slot_developer'))
    developer_admin.add_view(MyModelView(ServiceModel, session, name='Service', endpoint='service_developer'))
    developer_admin.add_view(MyModelView(CompanyModel, session, name='Company', endpoint='company_developer'))
    developer_admin.add_view(MyModelView(CarWashModel, session, name='Carwash', endpoint='carwash_developer'))
    developer_admin.add_view(MyModelView(ExtraModel, session, name='Extras', endpoint='extra_developer'))
    developer_admin.add_view(MyModelView(CustomerModel, session, name='Customer', endpoint='customer_developer'))
    developer_admin.add_view(MyModelView(BillingModel, session, name='Billing', endpoint='billing_developer'))
    developer_admin.add_view(MyModelView(CarModel, session, name='Car', endpoint='car_developer'))
    
    developer_admin.add_view(MonthlyInvoiceView(session=session, name='Monthly Invoices', endpoint='monthly_invoices_developer'))

