
from src.models.customer_model import CustomerModel
from src.models.car_model import CarModel, CarTypeEnum
from src.models.service_model import ServiceModel
from src.models.slot_model import SlotModel
from src.models.carwash_model import CarWashModel
from src.models.extra_model import ExtraModel
from src.models.reservation_model import ReservationModel
from src.views.my_modelview import MyModelView
from flask_login import current_user
from flask import current_app
from src.views.filters import ThisMonthFilter, ThisWeekFilter, TodayFilter
from flask_admin.contrib.sqla.filters import DateBetweenFilter
from src.views.reservation_form import ReservationForm

class ReservationAdminView(MyModelView):
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
        'billing.id',
        'is_completed'
    )

    column_labels = {
        'reservation_date': 'Időpont',
        'car.license_plate': 'Rendszám',
        'customer.forname': 'Kersztnév',
        'customer.lastname': 'Vezetéknév',
        'customer.phone_number': 'Telefonszám',
        'service.service_name': 'Csomag',
        'extras': 'Extrák',
        'carwash.carwash_name': 'Autómosó',
        'final_price': 'Ár',
        'is_completed': 'Kész?'
    }

    form_excluded_columns = ['billing']
    
    column_filters = [
        TodayFilter(ReservationModel.reservation_date),
        ThisWeekFilter(ReservationModel.reservation_date),
        ThisMonthFilter(ReservationModel.reservation_date),
        DateBetweenFilter(ReservationModel.reservation_date, "Custom date")
    ]

    def __init__(self, model, session, *args, **kwargs):
        self.session = session
        super(ReservationAdminView, self).__init__(model, session, *args, **kwargs)
        
    def get_list(self, *args, **kwargs):
    # Fetch the count and query from the base ModelView method
        count, query = super().get_list(*args, **kwargs)
        # Apply additional filter if current_user has carwash_id
        if current_user is current_user.is_authenticated:
            if  hasattr(current_user, 'carwash_id'): 
                query = [item for item in query if item.carwash_id == current_user.carwash_id]
            if current_user.role == 'admin':
                query = [item for item in query]
        return count, query

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

        except Exception as  e :
                self.session.rollback()
                current_app.logger.error(e)

        return super(ReservationAdminView, self).on_model_change(form, model, is_created)
