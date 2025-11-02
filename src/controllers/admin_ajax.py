from flask import Blueprint, request, jsonify, current_app
from src.models.service_model import ServiceModel
from src.models.extra_model import ExtraModel

admin_ajax = Blueprint('admin_ajax', __name__)

# Remove the extra /admin inside the route
@admin_ajax.route("/_get_services")
def get_services():
    carwash_id = request.args.get("carwash_id", type=int)
    session = current_app.session_factory.get_session()
    services = session.query(ServiceModel).filter_by(carwash_id=carwash_id).all()
    return jsonify([{"id": s.id, "name": s.service_name} for s in services])

@admin_ajax.route("/_get_extras")
def get_extras():
    carwash_id = request.args.get("carwash_id", type=int)
    session = current_app.session_factory.get_session()
    extras = session.query(ExtraModel).filter_by(carwash_id=carwash_id).all()
    return jsonify([{"id": e.id, "name": e.service_name} for e in extras])

