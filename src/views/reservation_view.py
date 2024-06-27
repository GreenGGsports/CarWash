from flask import Blueprint, render_template, request
import os 

reservation_view = Blueprint('reservation_view', __name__, template_folder='templates')

class ReservationView:  
    @staticmethod
    def show_reservation_form():
        # Print the full path where the system is searching for the HTML template
        template_full_path = os.path.join(os.path.dirname(__file__), reservation_view.template_folder, 'add_reservation.html')
        print(f"Searching for template at: {template_full_path}")
        return render_template('add_reservation.html')