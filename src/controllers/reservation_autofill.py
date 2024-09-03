from flask import Blueprint, request, jsonify, current_app, render_template, session
from flask_login import current_user
from src.models.customer_model import CustomerModel

reservation_autofill_ctrl = Blueprint('reservation_autofill_ctrl', __name__, url_prefix='/reservation_autofill')

@reservation_autofill_ctrl.route("/get_data")
def autofill():
    from pdb import set_trace
    set_trace()
    if current_user.is_authenticated:
        user_id = current_user.id
        try:
            session = current_app.session_factory.get_session()
            customer = session.query(CustomerModel).filter(CustomerModel.user_id == user_id).order_by(CustomerModel.id.desc()).first()
            from pdb import set_trace
            set_trace()
            
        except:
            pass
