from flask import Blueprint, render_template, request
import os 

reservation_view = Blueprint('reservation_view', __name__, template_folder='templates')

class ReservationView:  
    @staticmethod
    def show_reservation_form():
        return render_template('reservation.html')