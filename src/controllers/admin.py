from flask_admin import Admin
from src.models.reservation_model import ReservationModel
from src.models.customer_model import CustomerModel
from src.models.car_model import CarModel, CarTypeEnum
from src.models.billing_model import BillingModel
from src.models.service_model import ServiceModel
from src.models.company_model import CompanyModel
from src.models.slot_model import SlotModel
from src.models.user_model import UserModel
from src.models.carwash_model import CarWashModel
from src.models.extra_model import ExtraModel
from src.models.reservation_extras import reservation_extra
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, FloatField, DateTimeField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

class ServiceModelView(ModelView):
    column_labels = {
        'carwash.carwash_name': 'Car Wash Name',  # Itt adod meg az egyedi nevet
        'service_name': 'Service Name',
        'price_small': 'Price (Small)',
        'price_large': 'Price (Large)'
    }

    column_list = ['carwash.carwash_name', 'service_name', 'price_small', 'price_large']

class ReservationForm(FlaskForm):
    def __init__(self, session, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.session = session
        self.car.query_factory = lambda: self.session.query(CarModel).all()
        self.customer.query_factory = lambda: self.session.query(CustomerModel).all()
        self.service.query_factory = lambda: self.session.query(ServiceModel).all()
        self.carwash.query_factory = lambda: self.session.query(CarWashModel).all()
        self.slot.query_factory = lambda: self.session.query(SlotModel).all()
        self.extras.query_factory = lambda: self.session.query(ExtraModel).all()

    new_car_license_plate = StringField('New Car License Plate')
    new_car_type = SelectField('New Car Type', choices=[(t.name, t.name) for t in CarTypeEnum])
    new_car_brand = StringField('New Car Brand')
    car = QuerySelectField('Car', allow_blank=True, query_factory=lambda: [])

    new_customer_forname = StringField('New Customer Forname')
    new_customer_lastname = StringField('New Customer Lastname')
    new_customer_phone_number = StringField('New Customer Phone Number')
    customer = QuerySelectField('Customer', allow_blank=True, query_factory=lambda: [])

    service = QuerySelectField('Service', allow_blank=False, query_factory=lambda: [])
    extras = QuerySelectMultipleField('Extras', get_label='service_name')


    reservation_date = DateTimeField('Reservation Date', format='%Y-%m-%d %H:%M:%S')
    parking_spot = IntegerField('Parking Spot')
    final_price = FloatField('Final Price')
    carwash = QuerySelectField('Carwash', allow_blank=False, query_factory=lambda: [])
    slot = QuerySelectField('Slot', allow_blank=False, query_factory=lambda: [])

class ReservationAdminView(ModelView):
    form = ReservationForm
    # edit_template = 'admin/reservation_admin.html'
    # create_template = 'admin/reservation_admin.html'

    column_list = (
        'reservation_date',
        'car.license_plate',
        'carwash.carwash_name',
        'service.service_name',
        'extras',
        'customer.forname',
        'customer.lastname',
        'customer.phone_number',
        'final_price',
        'billing.id'
    )

    column_labels = {
        'reservation_date': 'Reservation Date',
        'car.license_plate': 'License Plate',
        'customer.forname': 'Forename',
        'customer.lastname': 'Lastname',
        'customer.phone_number': 'Phone Number',
        'service.service_name': 'Service Name',
        'extras': 'Extras',
        'carwash.carwash_name': 'Carwash Name',
        'final_price': 'Final Price',
    }

    form_excluded_columns = ['billing']

    def __init__(self, model, session_factory, *args, **kwargs):
        self.session_factory = session_factory
        super(ReservationAdminView, self).__init__(model, session_factory.get_session(), *args, **kwargs)

    def create_form(self, obj=None):
        form = super(ReservationAdminView, self).create_form(obj)
        form.session = self.session_factory.get_session()
        return form

    def edit_form(self, obj=None):
        form = super(ReservationAdminView, self).edit_form(obj)
        form.session = self.session_factory.get_session()
        return form

    def on_model_change(self, form, model, is_created):
        session = self.session_factory.get_session()
        
        # Handle new customer
        if form.new_customer_forname.data and form.new_customer_lastname.data and form.new_customer_phone_number.data:
            customer = session.query(CustomerModel).filter_by(
                forname=form.new_customer_forname.data,
                lastname=form.new_customer_lastname.data,
                phone_number=form.new_customer_phone_number.data
            ).first()
            if not customer:
                customer = CustomerModel(
                    forname=form.new_customer_forname.data,
                    lastname=form.new_customer_lastname.data,
                    phone_number=form.new_customer_phone_number.data
                )
                session.add(customer)
                session.commit()
            model.customer_id = customer.id

        # Handle new car
        if form.new_car_license_plate.data and form.new_car_type.data and form.new_car_brand.data:
            car = session.query(CarModel).filter_by(
                license_plate=form.new_car_license_plate.data,
                car_type=CarTypeEnum[form.new_car_type.data],
                car_brand=form.new_car_brand.data
            ).first()
            if not car:
                car = CarModel(
                    license_plate=form.new_car_license_plate.data,
                    car_type=CarTypeEnum[form.new_car_type.data],
                    car_brand=form.new_car_brand.data
                )
                session.add(car)
                session.commit()
            model.car_id = car.id

        session.close()  # Close the session

        return super(ReservationAdminView, self).on_model_change(form, model, is_created)
    
def init_admin(app, session_factory):
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

    # Admin view registration
    admin.add_view(ReservationAdminView(ReservationModel, session_factory))
    # admin.add_view(ModelView(UserModel, app.session_factory.get_session()))
    # admin.add_view(ModelView(SlotModel, app.session_factory.get_session()))
    # admin.add_view(ServiceModelView(ServiceModel, app.session_factory.get_session()))
    # admin.add_view(ModelView(CompanyModel, app.session_factory.get_session()))
    # admin.add_view(ModelView(CarWashModel, app.session_factory.get_session()))
    # admin.add_view(ModelView(ExtraModel, app.session_factory.get_session()))
    # admin.add_view(ModelView(CustomerModel, app.session_factory.get_session()))
    # admin.add_view(ModelView(BillingModel, app.session_factory.get_session()))