
from src.models.customer_model import CustomerModel
from src.models.car_model import CarModel, CarTypeEnum
from src.models.service_model import ServiceModel
from src.models.slot_model import SlotModel
from src.models.carwash_model import CarWashModel
from src.models.extra_model import ExtraModel
from src.models.reservation_model import ReservationModel
from src.models.billing_model import BillingModel
from src.views.my_modelview import MyModelView
from flask_login import current_user
from flask import current_app, request
from src.views.filters import ThisMonthFilter, ThisWeekFilter, TodayFilter
from flask_admin.contrib.sqla.filters import DateBetweenFilter
from src.views.reservation_form import ReservationForm

class ReservationAdminView(MyModelView):
    form = ReservationForm
    create_template = 'admin/reservation_form.html'
    list_template = 'admin/list_template.html'
    column_list = (
        'carwash.carwash_name',
        'reservation_date',
        'car.license_plate',
        'car.car_brand',
        'car.car_model',
        'service.service_name',
        'extras',
        'customer.phone_number',
        'payment_method',
        'final_price',
        'is_completed',
    )

    column_labels = {
        'carwash.carwash_name': 'Hely',
        'reservation_date': 'Dátum',
        'car.license_plate': 'Rendszám',
        'car.car_brand': 'Márka',
        'car.car_model': 'Típus',
        'service.service_name': 'Csomag',
        'extras': 'Extra',
        'final_price': 'Ár',
        'payment_method': 'Fizetési mód',
        'customer.phone_number': 'Tel',
        'is_completed': 'Kész?'
    }

    form_excluded_columns = ['billing']
    
    column_filters = [
        TodayFilter(ReservationModel.reservation_date),
        ThisWeekFilter(ReservationModel.reservation_date),
        ThisMonthFilter(ReservationModel.reservation_date),
        DateBetweenFilter(ReservationModel.reservation_date, "Custom date"),
        'car.license_plate',
        'service.service_name',
        'carwash.carwash_name',
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

        # Csak GET kérés esetén hívjuk meg a load_data-t
        if request.method == 'GET' and obj:
            form.load_data(obj)

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
                        car.car_model = form.new_car_model.data
                    else:
                        # Ha nem létezik, hozzuk létre az újat
                        car = CarModel(
                            license_plate=form.new_car_license_plate.data,
                            car_type=CarTypeEnum[form.new_car_type.data],
                            car_brand=form.new_car_brand.data,
                            car_model = form.new_car_model.data
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
                if form.billing_required.data:
                    BillingModel.add_billing_data(
                        session=session,
                        reservation_id=model.id,
                        name=form.billing_name.data,
                        address=form.address.data,
                        email=form.email.data,
                        company_name=form.company_name.data,
                        tax_ID=form.tax_ID.data
                    )
                    

                session.flush()

        except Exception as  e :
                self.session.rollback()
                current_app.logger.error(e)

        return super(ReservationAdminView, self).on_model_change(form, model, is_created)
    
    def on_model_delete(self, model):
        try:
            # Ellenőrizzük, hogy van-e kapcsolódó számla
            billing = model.billing
            if billing:
                # Töröljük a számlát a foglalás törlése előtt
                self.session.delete(billing)
                self.session.commit()

            # Foglalás törlése
            self.session.delete(model)
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(f"Hiba történt a foglalás vagy a számla törlése közben: {str(e)}")
        
        return super(ReservationAdminView, self).on_model_delete(model)
    
    def render(self, template, **kwargs):
        # Append summary data to kwargs
        kwargs['summary_data'] = [
            {
                'title': 'Összeg (filtered)',
                'final_price': self.get_sum('final_price'),
            },
        ]

        return super(ReservationAdminView, self).render(template, **kwargs)
