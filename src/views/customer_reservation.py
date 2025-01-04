from src.models.carwash_model import CarWashModel
from src.models.car_model import CarModel 
from src.models.service_model import ServiceModel
from src.models.extra_model import ExtraModel
from src.models.customer_model import CustomerModel
from src.models.reservation_model import ReservationModel
from src.models.billing_model import BillingModel
from flask import  render_template, request, Blueprint, current_app, session
from src.views.form_data import ReservationData, BillingData, CarData
from src.controllers.reservation_controller2 import create_reservation, create_billing
from src.models.slot_model import SlotModel
from flask_login import current_user
from src.controllers.reservation_controller2 import create_reservation, create_billing, add_car, add_customer
from src.views.form_data import ReservationData, BillingData, CarData, CustomerData

reservation_test = Blueprint('reservation_test', __name__, template_folder='templates')


def frontend_query(carwash_id=1):
    db_session = current_app.session_factory.get_session()
    locations = db_session.query(CarWashModel).all()
    services = db_session.query(ServiceModel).filter_by(carwash_id=carwash_id).all()
    services = db_session.query(ServiceModel).filter_by(carwash_id=carwash_id).all()
    extras = db_session.query(ExtraModel).filter_by(carwash_id=carwash_id).all()

    if not current_user.is_authenticated:
        return dict(
            locations=locations, 
            services=services, 
            extras=extras, 
            customer=None, 
            selected_location_id=carwash_id,
            car = None,
        )
    if not db_session.query(CustomerModel).filter_by(user_id=current_user.id).first():
        return dict(
            locations=locations, 
            services=services, 
            extras=extras, 
            customer=None, 
            selected_location_id=carwash_id,
            car = None,
            billing  = None,
        ) 
    else:
        customer = db_session.query(CustomerModel).filter_by(user_id=current_user.id).first()
        last_reservation = (
            db_session.query(ReservationModel)
            .filter_by(customer_id=customer.id)
            .order_by(ReservationModel.id.desc())
            .first()
        )
        if not last_reservation:
            return dict(
                locations=locations, 
                services=services, 
                extras=extras, 
                customer=None, 
                selected_location_id=carwash_id,
                car = None,
                billing  = None,
            ) 
        else:
            car = db_session.query(CarModel).filter_by(id = last_reservation.car_id)
            billing = db_session.query(BillingModel).filter_by(reservation_id=last_reservation.id).first()
            return dict(
                locations=locations, 
                services=services, 
                extras=extras, 
                customer=customer, 
                selected_location_id=carwash_id,
                car = car,
                billing  = billing,
            )
    
@reservation_test.route("/reserve")
def show():
    kwargs = frontend_query()
    session['carwash_id'] =  kwargs["locations"][0].id
    return render(**kwargs)

@reservation_test.route("/select_location", methods=["GET", "POST"])
def select_carwash():
    carwash_id = int(request.form.get("location_id"))
    session['carwash_id'] = carwash_id
    kwargs = frontend_query(carwash_id=carwash_id)
    return render(**kwargs)

def render(locations, services, extras, customer=None, car =None, billing=None, selected_location_id=None):
    return render_template(
        'FoglalasV2.html', 
        locations=locations, 
        services=services, 
        extras=extras, 
        customer=customer, 
        car=car, 
        billing=billing, 
        selected_location_id=selected_location_id)



@reservation_test.route("/create_reservation",methods=["POST"])
def reservation():
    form_data = request.form.to_dict()
    db_session = current_app.session_factory.get_session()
    selected_extras = request.form.getlist('extras') 
    carwash =  db_session.query(CarWashModel).filter_by(id=session['carwash_id']).first()
    service =  db_session.query(ServiceModel).filter_by(id=int(form_data['service'])).first()
    extras = db_session.query(ExtraModel).filter(ExtraModel.id.in_(selected_extras)).all()

    slot = db_session.query(SlotModel).filter_by(id=int(form_data['timeSlot'])).first()
    car_data = CarData.parseForm(form_data)
    car = add_car(db_session,car_data)
        
    customer_data = CustomerData.parseForm(form_data)
    customer = add_customer(db_session, customer_data, admin=False)
    
    reservation_data = ReservationData.parseForm(form_data)
    reservation = create_reservation(
        session=db_session,
        carwash=carwash, 
        service=service, 
        extras=extras, 
        slot=slot,
        car=car,
        customer=customer,
        reservation_data=reservation_data,
        admin=False
        )

    if form_data.get('billing_required', False):
        billing_data = BillingData.parseForm(form_data)
        billing = create_billing(db_session,reservation, billing_data)
    return "success"