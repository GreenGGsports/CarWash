from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import DataRequired
from src.models.carwash_model import CarWashModel 
from src.models.service_model import ServiceModel
from src.models.extra_model import ExtraModel
from src.models.customer_model import CustomerModel
from flask import Flask, render_template, request, Blueprint, current_app, session

reservation_test = Blueprint('reservation_test', __name__, template_folder='templates')



@reservation_test.route("/reserve")
def show():
    db_session = current_app.session_factory.get_session()
    locations = db_session.query(CarWashModel).all()
    services = db_session.query(ServiceModel).filter_by(carwash_id=1).all()
    extras = db_session.query(ExtraModel).filter_by(carwash_id=1).all()
    customer = db_session.query(CustomerModel).filter_by(user_id=1).first()
    return render(locations, services,extras=extras,customer=customer)

@reservation_test.route("/select_location", methods=["GET", "POST"])
def select_carwash():
    carwash_id = int(request.form.get("location_id"))
    session['carwash_id'] = carwash_id
    db_session = current_app.session_factory.get_session()
    locations = db_session.query(CarWashModel).all()
    services = db_session.query(ServiceModel).filter_by(carwash_id=carwash_id).all()
    extras =  db_session.query(ExtraModel).filter_by(carwash_id=carwash_id).all()
    customer = db_session.query(CustomerModel).filter_by(user_id=1).first()
    return render(locations, services, extras, customer, carwash_id)

def render(locations, services, extras, customer, selected_location_id=None):
    return render_template('FoglalasV2.html', locations=locations, services=services, extras=extras, customer=customer, selected_location_id=selected_location_id)



@reservation_test.route("/create_reservation",methods=[ "POST"])
def create_reservation():
    from pdb import set_trace
    set_trace()
    pass