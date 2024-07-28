from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from src.models.customer_model import CustomerModel
from src.models.car_model import CarModel, CarTypeEnum
from src.models.reservation_model import ReservationModel

class ReservationForm(FlaskForm):
    def __init__(self, session, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.session = session
        self.car.query_factory = lambda: self.session.query(CarModel).all()
        self.customer.query_factory = lambda: self.session.query(CustomerModel).all()

    car = QuerySelectField('Car', allow_blank=True)
    customer = QuerySelectField('Customer', allow_blank=True)
    new_customer_forname = StringField('New Customer Forname')
    new_customer_lastname = StringField('New Customer Lastname')
    new_customer_phone_number = StringField('New Customer Phone Number')
    new_car_license_plate = StringField('New Car License Plate')
    new_car_type = SelectField('New Car Type', choices=[(t.name, t.name) for t in CarTypeEnum])
    new_car_brand = StringField('New Car Brand')

class ReservationAdminView(ModelView):
    form = ReservationForm
    edit_template = 'reservation_admin.html'
    create_template = 'admin/reservation_admin.html'

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
        super(ReservationAdminView, self).__init__(model, self.session_factory.get_session(), *args, **kwargs)

    def create_form(self, obj=None):
        form = super(ReservationAdminView, self).create_form(obj)
        form.session = self.session_factory.get_session()
        self._add_custom_fields(form)
        return form

    def edit_form(self, obj=None):
        form = super(ReservationAdminView, self).edit_form(obj)
        form.session = self.session_factory.get_session()
        self._add_custom_fields(form)
        return form

    def _add_custom_fields(self, form):
        form.new_customer_forname = StringField('New Customer Forname')
        form.new_customer_lastname = StringField('New Customer Lastname')
        form.new_customer_phone_number = StringField('New Customer Phone Number')
        form.new_car_license_plate = StringField('New Car License Plate')
        form.new_car_type = SelectField(
            'New Car Type',
            choices=[(t.name, t.name) for t in CarTypeEnum]
        )
        form.new_car_brand = StringField('New Car Brand')

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

        session.close()  # Session lezárása

        return super(ReservationAdminView, self).on_model_change(form, model, is_created)

def init_admin(app, session_factory):
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
    
    # Admin nézetek hozzáadása
    admin.add_view(ReservationAdminView(ReservationModel, session_factory))
