from flask import Blueprint, request, jsonify, current_app, render_template
from src.models.reservation_model import ReservationModel
import datetime

reservation_ctrl = Blueprint('reservation_ctrl', __name__, url_prefix='/reservation')

@reservation_ctrl.route('/')
def show_reservation_form():
    return render_template('reservation.html')

