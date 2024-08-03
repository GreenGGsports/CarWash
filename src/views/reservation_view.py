from flask import Blueprint, render_template, request
import os 

reservation_view = Blueprint('reservation_view', __name__, template_folder='templates')

class ReservationView:  
    @staticmethod
    def show_reservation_form():
        return render_template('reservation.html')
    
    @staticmethod
    def generate_popup_html(hely, elerhetosegek, rendszam, csomag, extra, idopont, vegosszeg):
        """
        Generates a popup HTML.
        """
        return render_template('popup.html',
                            hely=hely,
                            elerhetosegek=elerhetosegek,
                            rendszam=rendszam,
                            csomag=csomag,
                            extra=extra,
                            idopont=idopont,
                            vegosszeg=vegosszeg)