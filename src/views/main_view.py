from flask import Blueprint, request, jsonify, current_app, render_template, url_for, redirect
from src.models.carwash_model import CarWashModel
from src.models.service_model import ServiceModel
from src.models.extra_model import ExtraModel
main_view = Blueprint('main_view', __name__, url_prefix='/')

@main_view.route("/",methods=["GET"])
def home():
    try:
        db_session = current_app.session_factory.get_session()
        locations = db_session.query(CarWashModel).all()
        return render_template('Landing_page.html', locations=locations)
    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")
        return render_template("500.html", message="An internal error occurred"), 500

@main_view.route("/carwash/<site_name>", methods=["GET"])
def show_carwash_sites(site_name):
    try:
        db_session = current_app.session_factory.get_session()

        carwash = db_session.query(CarWashModel).filter_by(carwash_name=site_name).first()
        if not carwash:
            current_app.logger.warning(f"Car wash site '{site_name}' not found.")
            return redirect(url_for('main_view.home'))
        
        carwash_id = carwash.id
        location = db_session.query(CarWashModel).filter_by(id=carwash_id).first()
        services = db_session.query(ServiceModel).filter_by(carwash_id=carwash_id).all()
        extras = db_session.query(ExtraModel).filter_by(carwash_id=carwash_id).all()
        service_data, extra_names_out, extra_names_in = get_service_data(carwash_id)
        return render_template('Carwash_sites.html', location=location, service_data=service_data, extra_names_out=extra_names_out, extra_names_in=extra_names_in)

    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")
        return render_template("500.html", message="An internal error occurred"), 500

def get_service_data(carwash_id):
    service_data = []
    db_session = current_app.session_factory.get_session()
    services = db_session.query(ServiceModel).filter_by(carwash_id=carwash_id).all()
    extras_out = db_session.query(ExtraModel).filter_by(carwash_id=carwash_id).filter_by(extra_type='exterior').all()
    extras_in = db_session.query(ExtraModel).filter_by(carwash_id=carwash_id).filter_by(extra_type='interior').all()
    

    for service in services:
        service_data.append (
            dict(
            name = service.service_name,
            extras_out = [extra in service.extras for extra in extras_out],
            extras_in = [extra in service.extras for extra in extras_in],
            price_small = service.price_small,
            price_medium = service.price_medium,
            price_large = service.price_large,
            )
        )
    extra_names_out =  [extra.service_name for extra in extras_out]
    extra_names_in =  [extra.service_name for extra in extras_in]
    return service_data, extra_names_out, extra_names_in

@main_view.route("/carwash/", methods=["POST"])
def carwash_sites():
    try:
        db_session = current_app.session_factory.get_session()
        carwash_id = request.form.get("location_id")
        carwash_site_name = db_session.query(CarWashModel).filter_by(id=carwash_id).first().carwash_name
    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")
        return render_template("500.html", message="An internal error occurred"), 500
    return redirect(url_for('main_view.show_carwash_sites', site_name=carwash_site_name))