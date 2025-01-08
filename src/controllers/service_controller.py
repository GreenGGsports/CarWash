from src.models.service_model import ServiceModel 
from src.models.extra_model import ExtraModel
from flask import Blueprint, request, jsonify, current_app, session
from flask_login import current_user 

service_ctrl = Blueprint('service_ctrl', __name__, url_prefix='/service')

@service_ctrl.route('/list_included', methods=['POST'])
def get_content():
    service_id = int(request.json.get('service_id'))
    db_session = current_app.session_factory.get_session()
    service = db_session.query(ServiceModel).filter_by(id=service_id).first()
    
    current_app.logger.info(f"Requested service_id: {service_id}")
    
    if service is None:
        current_app.logger.warning(f"Service with id {service_id} not found.")
        return jsonify({"error": "Service not found"}), 404
    
    extras_included = [extra.id for extra in service.extras]
    current_app.logger.info(f"Service {service_id} includes {len(extras_included)} extras: {extras_included}")
    
    return jsonify(extras_included)

