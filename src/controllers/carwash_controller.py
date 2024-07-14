from flask import Blueprint, request, jsonify, current_app, session
from flask_login import current_user 
from src.models.carwash_model import CarWashModel

carwash_ctrl = Blueprint('carwash_ctrl', __name__, url_prefix='/carwash')

@carwash_ctrl.route('/list', methods=['GET'])
def get_carwashes():
    db_session = current_app.session_factory.get_session()
    carwashes = CarWashModel.get_all(session=db_session)
    
    response_data = []
    for carwash in carwashes:
        response_data.append(
            dict(
                id = carwash.id,
                location = carwash.location
            )
        )
    return jsonify(response_data)

@carwash_ctrl.route('/select', methods=['POST'])
def select_carwash():
    data = request.json
    carwash_id = int(data.get('id'))
    if not carwash_id:
        return jsonify({'message': 'Hiányzó azonosító!'}), 400
    
    session['carwash_id'] = carwash_id
    return jsonify({'message': 'Helyszín kiválasztva!', 'id': carwash_id}), 200
