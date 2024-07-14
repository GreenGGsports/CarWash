from src.models.service_model import ServiceModel 
from src.models.extra_model import ExtraModel
from flask import Blueprint, request, jsonify, current_app, session
from flask_login import current_user 

service_ctrl = Blueprint('service_ctrl', __name__, url_prefix='/service')

@service_ctrl.route('/list', methods=['GET'])
def get_service():  
    db_session = current_app.session_factory.get_session()
    if 'carwash_id' not in session:
        return jsonify(({'status': 'failed no carwash_id selected'}))
    else:
        carwash_id = session['carwash_id']
    
    
    services = ServiceModel.filter_by_column_value(db_session,'id',carwash_id)
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
    session['sevice_id'] = service_id
    return jsonify({'message': 'Csomag kiválasztva!', 'id': service_id}), 200


@service_ctrl.route('/list_extra', methods=['GET'])
def get_extra():
    db_session = current_app.session_factory.get_session()
    if 'carwash_id' in session:
        return jsonify(({'status': 'failed no carwash_id selected'}))
    else:
        carwash_id = 1
    extras = ExtraModel.filter_by_column_value(db_session,'carwash_id',carwash_id)
    response_data = []
    for extra in extras:
        response_data.append(
            dict(
                id = extra.id,
                name = extra.extra_name,
                type = extra.extra_type
            )
        )     
    return jsonify(response_data)