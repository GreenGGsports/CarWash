from src.models.service_model import ServiceModel 
from src.models.extra_model import ExtraModel
from flask import Blueprint, request, jsonify, current_app, session
from flask_login import current_user 

service_ctrl = Blueprint('service_ctrl', __name__, url_prefix='/service')

@service_ctrl.route('/list', methods=['GET'])
def get_service():  
    db_session = current_app.session_factory.get_session()
    if 'carwash_id' not in session:
        current_app.logger.warning('No carwash_id in session. Cannot retrieve services.')
        return jsonify({'status': 'failed', 'message': 'No carwash_id selected'}), 400
    
    carwash_id = session['carwash_id']
    try:
        services = ServiceModel.filter_by_column_value(db_session, 'carwash_id', carwash_id)
        response_data = [{'id': service.id, 'name': service.service_name, 'description': service.description} for service in services]

        current_app.logger.info(f"Retrieved services for carwash_id {carwash_id}.")
        return jsonify(response_data), 200
    
    except Exception as e:
        current_app.logger.error(f"Error retrieving services for carwash_id {carwash_id}: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to retrieve services.'}), 500

@service_ctrl.route('/select', methods=['POST'])
def select_service():
    db_session = current_app.session_factory.get_session()
    data = request.json
    service_id = data.get('id')

    if not service_id:
        current_app.logger.warning('Missing service ID in request.')
        return jsonify({'status': 'failed', 'message': 'Service ID is required!'}), 400
    
    try:
        service = ServiceModel.get_by_id(session=db_session, obj_id=int(service_id))
        if not service:
            current_app.logger.warning(f"Service with ID {service_id} not found.")
            return jsonify({'status': 'failed', 'message': 'Service not found!'}), 404
        
        session['service_id'] = service.id
        session['service_name'] = service.service_name
        
        current_app.logger.info(f"Service {service_id} selected.")
        return jsonify({'status': 'success', 'message': 'Service selected!', 'id': service.id}), 200
    
    except ValueError:
        current_app.logger.error('Invalid service ID format.')
        return jsonify({'status': 'error', 'message': 'Invalid service ID format.'}), 400
    
    except Exception as e:
        current_app.logger.error(f"Error selecting service with ID {service_id}: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to select service.'}), 500


@service_ctrl.route('/list_extra', methods=['GET'])
def get_extra():
    try:
        db_session = current_app.session_factory.get_session()
        if 'carwash_id' not in session:
            current_app.logger.warning('No carwash_id in session. Cannot retrieve extras.')
            return jsonify({'status': 'failed', 'message': 'No carwash_id selected'}), 400
        
        carwash_id = session['carwash_id']
        extras = ExtraModel.filter_by_column_value(db_session, 'carwash_id', carwash_id)
        
        response_data = []
        if extras:
            response_data = [{'id': extra.id, 'name': extra.service_name, 'type': extra.extra_type} for extra in extras]
        
        current_app.logger.info(f"Retrieved extras for carwash_id {carwash_id}.")
        return jsonify(response_data), 200
    
    except Exception as e:
        current_app.logger.error(f"Error retrieving extras: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to retrieve extras.'}), 500

@service_ctrl.route('/select_extras', methods=['POST'])
def select_extras():
    try:
        data = request.json
        extra_ids = [int(i) for i in data.get('extra_ids', [])] 
        session['extra_ids'] = extra_ids
        
        current_app.logger.info(f"Selected extras: {extra_ids}.")
        return jsonify({'message': 'Extrák kiválasztva!', 'ids': extra_ids}), 200
    
    except ValueError as e:
        current_app.logger.error(f"Invalid extra_id format: {e}")
        return jsonify({'status': 'error', 'message': 'Invalid format for extra_ids.'}), 400
    
    except Exception as e:
        current_app.logger.error(f"Error selecting extras: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to select extras.'}), 500