from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, FloatField, DateTimeField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from src.models.customer_model import CustomerModel
from src.models.car_model import CarModel, CarTypeEnum
from src.models.service_model import ServiceModel
from src.models.slot_model import SlotModel
from src.models.carwash_model import CarWashModel
from src.models.extra_model import ExtraModel
from src.models.reservation_model import ReservationModel
from flask_admin.contrib.sqla import ModelView, filters
from datetime import datetime, timedelta
from flask_login import current_user

class DateRangeFilter(filters.BaseSQLAFilter):
    def __init__(self, column, label, start_date, end_date):
        super().__init__(column, label)
        self.start_date = start_date
        self.end_date = end_date

    def apply(self, query, value):
        return query.filter(self.column.between(self.start_date, self.end_date))

    def operation(self):
        return f"Date between {self.start_date.strftime('%Y-%m-%d')} and {self.end_date.strftime('%Y-%m-%d')}"

class DayFilter(DateRangeFilter):
    def __init__(self, column, label, date):
        start_date = datetime(date.year, date.month, date.day)
        end_date = start_date + timedelta(days=1)
        super().__init__(column, label, start_date, end_date)

    def operation(self):
        return f"Date is {self.start_date.strftime('%Y-%m-%d')}"

class WeekFilter(DateRangeFilter):
    def __init__(self, column, label, date):
        start_date = date - timedelta(days=date.weekday())
        end_date = start_date + timedelta(days=7)
        super().__init__(column, label, start_date, end_date)

    def operation(self):
        return f"Week starting from {self.start_date.strftime('%Y-%m-%d')}"

class MonthFilter(DateRangeFilter):
    def __init__(self, column, label, date):
        start_date = datetime(date.year, date.month, 1)
        end_date = datetime(date.year, date.month + 1, 1) if date.month < 12 else datetime(date.year + 1, 1, 1)
        super().__init__(column, label, start_date, end_date)

    def operation(self):
        return f"Month of {self.start_date.strftime('%Y-%m')}"

class ReservationForm(FlaskForm):
    def __init__(self, session, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.session = session

        # Filtering options based on the current user
        if current_user.role == 'local_admin':
            self.carwash.query_factory = lambda: self.session.query(CarWashModel).filter_by(id=current_user.carwash.id).all()
            self.service.query_factory = lambda: self.session.query(ServiceModel).filter_by(id=current_user.carwash.id).all()
            self.extras.query_factory = lambda: self.session.query(ExtraModel).filter_by(id=current_user.carwash.id).all()

        else:
            self.carwash.query_factory = lambda: self.session.query(CarWashModel).all()
            self.service.query_factory = lambda: self.session.query(ServiceModel).all()
            
            self.extras.query_factory = lambda: self.session.query(ExtraModel).all()

        self.slot.query_factory = lambda: self.session.query(SlotModel).all()
        self.car.query_factory = lambda: self.session.query(CarModel).all()
        self.customer.query_factory = lambda: self.session.query(CustomerModel).all()
        
    # Form fields
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
    carwash = QuerySelectField('Carwash', allow_blank=False, query_factory=lambda: [])
    slot = QuerySelectField('Slot', allow_blank=False, query_factory=lambda: [])


class ReservationAdminView(ModelView):
    form = ReservationForm
    create_template = 'admin/reservation_form.html'
    
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

    column_filters = [
        DayFilter('reservation_date', 'Reservation Date (Day)', datetime.now()),
        WeekFilter('reservation_date', 'Reservation Date (Week)', datetime.now()),
        MonthFilter('reservation_date', 'Reservation Date (Month)', datetime.now())
    ]

    form_excluded_columns = ['billing']

    def __init__(self, model, session, *args, **kwargs):
        self.session = session
        super(ReservationAdminView, self).__init__(model, session, *args, **kwargs)

    def create_form(self, obj=None):
        form = super(ReservationAdminView, self).create_form(obj)
        form.session = self.session
        form.user_role = current_user.role if current_user.is_authenticated else None  # Pass user role to form
        return form

    def edit_form(self, obj=None):
        form = super(ReservationAdminView, self).edit_form(obj)
        form.session = self.session
        form.user_role = current_user.role if current_user.is_authenticated else None  # Pass user role to form
        return form
    
    def on_model_change(self, form, model, is_created):
        session = form.session

        
        try:
            # Use no_autoflush to prevent automatic flushes
            with session.no_autoflush:
                # Ensure that all related models are attached to the session
                if form.service.data:
                    model.service = session.merge(ServiceModel(id=form.service.data.id))
                if form.carwash.data:
                    model.carwash = session.merge(CarWashModel(id=form.carwash.data.id))
                if form.slot.data:
                    model.slot = session.merge(SlotModel(id=form.slot.data.id))
                if form.extras.data:
                    model.extras = [session.merge(ExtraModel(id=extra.id)) for extra in form.extras.data]



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
                    
                    model.customer_id = customer.id
                    model.customer = customer
                
                # Handle new car
                if form.new_car_license_plate.data:
                    car = session.query(CarModel).filter_by(
                        license_plate=form.new_car_license_plate.data
                    ).first()

                    if car:
                        # Ha az autó már létezik, frissítsük a típusát és márkáját
                        car.car_type = CarTypeEnum[form.new_car_type.data]
                        car.car_brand = form.new_car_brand.data
                    else:
                        # Ha nem létezik, hozzuk létre az újat
                        car = CarModel(
                            license_plate=form.new_car_license_plate.data,
                            car_type=CarTypeEnum[form.new_car_type.data],
                            car_brand=form.new_car_brand.data
                        )
                        session.add(car)
                    
                    # Commit után a model-hez rendeljük a car_id-t és car objektumot
                    session.commit()
                    model.car_id = car.id
                    model.car = car
                
                model.final_price = ReservationModel.calculate_final_price(session, 
                                                                           service_id=model.service.id,
                                                                           car_id= model.car.id, 
                                                                           extras=[extra.id for extra in model.extras])

                # Flush changes manually
                session.flush()

        except Exception as e:
            print(f"Exception occurred: {e}")
            raise

        return super(ReservationAdminView, self).on_model_change(form, model, is_created)
