from flask import Blueprint, render_template, request

reservation_view = Blueprint('reservation_view', __name__, template_folder='templates')

@reservation_view.route('/add', methods=['GET'])
def show_reservation_form():
    return render_template('add_reservation.html')

@reservation_view.route('/add', methods=['POST'])
def submit_form():
    return request.json 
