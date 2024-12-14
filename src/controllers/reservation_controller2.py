from flask import current_app 
from src.models.service_model import ServiceModel
from src.models.carwash_model import CarWashModel
from src.models.extra_model import ExtraModel
from src.models.customer_model import CustomerModel
from src.models.slot_model import SlotModel
from src.models.car_model import CarModel, CarTypeEnum
from src.models.reservation_model import ReservationModel
from src.models.billing_model import BillingModel

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
            

            if form.new_price.data:
                model.final_price = form.new_price.data
            else:
                model.final_price = ReservationModel.calculate_final_price(session, 
                                                                        service_id=model.service.id,
                                                                        car_id= model.car.id, 
                                                                        extras=[extra.id for extra in model.extras])
            

            

            if form.billing_required.data:
                billing = session.query(BillingModel).filter_by(reservation_id=model.id).first()
                if not billing:
                    # Ha nincs számlázási adat, hozzunk létre újat
                    BillingModel.add_billing_data(
                        session=session,
                        reservation_id=model.id,
                        name=form.billing_name.data,
                        address=form.address.data,
                        email=form.email.data,
                        company_name=form.company_name.data,
                        tax_ID=form.tax_ID.data
                    )
                else:
                    # Ha van számlázási adat, frissítsük
                    billing.name = form.billing_name.data
                    billing.address = form.address.data
                    billing.email = form.email.data
                    billing.company_name = form.company_name.data
                    billing.tax_ID = form.tax_ID.data
                    session.add(billing)

            session.flush()

    except Exception as  e :
            self.session.rollback()
            current_app.logger.error(e)