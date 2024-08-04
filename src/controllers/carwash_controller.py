from flask import Blueprint, request, jsonify, current_app, session
from flask_login import current_user 
from src.models.carwash_model import CarWashModel

carwash_ctrl = Blueprint('carwash_ctrl', __name__, url_prefix='/carwash')

@carwash_ctrl.route('/list', methods=['GET'])
def get_carwashes():
    try:
        db_session = current_app.session_factory.get_session()
        carwashes = CarWashModel.get_all(session=db_session)
        
        response_data = [{'id': carwash.id, 'location': carwash.location} for carwash in carwashes]
        
        current_app.logger.info("Retrieved carwashes successfully.")
        return jsonify(response_data)
    
    except Exception as e:
        current_app.logger.error(f"Error retrieving carwashes: {e}")
        return jsonify({'error': 'Failed to retrieve carwashes.'}), 500

@carwash_ctrl.route('/select', methods=['POST'])
def select_carwash():
    try:
        db_session = current_app.session_factory.get_session()
        data = request.json
        
        carwash_id = data.get('id')
        if not carwash_id:
            return jsonify({'message': 'Hiányzó azonosító!'}), 400
        
        carwash_id = int(carwash_id) 
        carwash = CarWashModel.get_by_id(session=db_session, obj_id=carwash_id)
        
        if not carwash:
            return jsonify({'message': 'Carwash not found!'}), 404
        
        session['carwash_id'] = carwash.id
        current_app.logger.info(f"Carwash with ID {carwash_id} selected successfully.")
        return jsonify({'message': 'Helyszín kiválasztva!', 'id': carwash_id}), 200

    except ValueError as e:
        current_app.logger.error(f"Value error during carwash selection: {e}")
        return jsonify({'message': 'Invalid carwash ID format.'}), 400

    except Exception as e:
        current_app.logger.error(f"Error selecting carwash: {e}")
        return jsonify({'error': 'Failed to select carwash.'}), 500
