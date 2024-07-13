from src.models.service_model import ServiceModel 
from src.models.extra_model import ExtraModel
from flask import Blueprint, request, jsonify, current_app
from flask_login import current_user 

service_ctrl = Blueprint('service_ctrl', __name__, url_prefix='/service')

@service_ctrl.route('/list', methods=['GET'])
def get_service():

    session = current_app.session_factory.get_session()
    carwash_id = current_user.carwash_id
    services = ServiceModel.filter_by_column_value(session,'carwash_id',carwash_id)
    response_data = []
    for service in services:
        response_data.append(
            dict(
                id = service.id,
                name = service.service_name,
                description = service.description
            )
        )
    return jsonify(response_data)

@service_ctrl.route('/select', methods=['POST'])
def select_service():
    data = request.json
    service_id = int(data.get('id'))
    if not service_id:
        return jsonify({'message': 'Hiányzó azonosító!'}), 400
    current_user.service_id = service_id
    return jsonify({'message': 'Csomag kiválasztva!', 'id': service_id}), 200