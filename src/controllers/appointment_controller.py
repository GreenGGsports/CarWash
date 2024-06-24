from flask import Blueprint, request, jsonify
import datetime

appointment_ctrl = Blueprint('appointment_ctrl', __name__, url_prefix='/reservation')

@appointment_ctrl.route('/list_appointments', methods=['POST'])
def list_available_appointments():
    # Example list of appointments; replace with actual data retrieval
    appointments = [
        dict(
            id=1,
            start='9:00',
            end='10:00'
        ),
        dict(
            id=2,
            start='10:00',
            end='11:00'
        ),
        dict(
            id=3,
            start='11:00',
            end='12:00'
        ),
    ]
    return jsonify(appointments)
