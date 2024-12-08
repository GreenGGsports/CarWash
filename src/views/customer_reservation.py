from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import DataRequired
from src.models.carwash_model import CarWashModel 
from src.models.service_model import ServiceModel
from src.models.extra_model import ExtraModel
from src.models.customer_model import CustomerModel
from flask import Flask, render_template, request, Blueprint, current_app

reservation_test = Blueprint('reservation_test', __name__, template_folder='templates')



@reservation_test.route("/reserve")
def show():
    session = current_app.session_factory.get_session()
    locations = session.query(CarWashModel).all()
    services = session.query(ServiceModel).filter_by(carwash_id=1).all()
    extras = session.query(ExtraModel).filter_by(carwash_id=1).all()
    customer = session.query(CustomerModel).filter_by(user_id=1).first()
    return render(locations, services,extras=extras,customer=customer)

@reservation_test.route("/select_location", methods=["GET", "POST"])
def select_carwash():
    carwash_id = int(request.form.get("location_id"))
    session = current_app.session_factory.get_session()
    locations = session.query(CarWashModel).all()
    services = session.query(ServiceModel).filter_by(carwash_id=carwash_id).all()
    extras =  session.query(ExtraModel).filter_by(carwash_id=carwash_id).all()
    return render(locations, services, extras)

def render(locations, services, extras, customer):
    return render_template('FoglalasV2.html', locations=locations, services=services, extras=extras, customer=customer)


