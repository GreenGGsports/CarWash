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

def init_admin(app, session_factory):
    admin = Admin(
        app,
        name='Admin Panel',
        template_mode='bootstrap3',
        index_view=AdminIndexView(url='/admin', endpoint='admin')
    )

    session = session_factory.get_session()

    # Admin view registration
    admin.add_view(ReservationAdminView(ReservationModel, session, name='ReservationModelAdmin', endpoint='reservation_admin'))
    admin.add_view(ModelView(UserModel, session, name='UserModelAdmin', endpoint='user_admin'))
    admin.add_view(ModelView(SlotModel, session, name='SlotModelAdmin', endpoint='slot_admin'))
    admin.add_view(ServiceModelView(ServiceModel, session, name='ServiceModelAdmin', endpoint='service_admin'))
    admin.add_view(ModelView(CompanyModel, session, name='CompanyModelAdmin', endpoint='company_admin'))
    admin.add_view(ModelView(CarWashModel, session, name='CarWashModelAdmin', endpoint='carwash_admin'))
    admin.add_view(ModelView(ExtraModel, session, name='ExtraModelAdmin', endpoint='extra_admin'))
    admin.add_view(ModelView(CustomerModel, session, name='CustomerModelAdmin', endpoint='customer_admin'))
    admin.add_view(ModelView(BillingModel, session, name='BillingModelAdmin', endpoint='billing_admin'))
    admin.add_view(ModelView(CarModel, session, name='CarModelAdmin', endpoint='car_admin'))
    
    admin.add_view(MonthlyInvoiceView(session=session, name='Monthly Invoices', endpoint='monthly_invoices'))

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
    local_admin.add_view(ReservationAdminView(ReservationModel, session, name='LocalReservationModelAdmin', endpoint='local_reservation_admin'))
    local_admin.add_view(ServiceModelView(ServiceModel, session, name='LocalServiceModelAdmin', endpoint='local_service_admin'))
    local_admin.add_view(ModelView(ExtraModel, session, name='LocalExtraModelAdmin', endpoint='local_extra_admin'))

    session.close()
