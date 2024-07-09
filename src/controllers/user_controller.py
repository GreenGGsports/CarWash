from flask import Blueprint, request, jsonify, current_app, render_template
from src.models.user_model import UserModel
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

user_ctrl = Blueprint('user_ctrl', __name__)


#only for testing
@user_ctrl.route('/')
def show_test_form():
    return render_template('User.html')

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.reservation_id = None


# Function to initialize LoginManager
def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user_ctrl.login'

    @login_manager.user_loader
    def load_user(user_id):
        if user_id:
            return User(user_id)
        return None
    
@user_ctrl.route('/login', methods=['POST'])
def login():
    session = current_app.session_factory.get_session()
    data = request.json
    user_name = data.get('user_name')
    password = data.get('password')
    user = UserModel.login(session=session, user_name=user_name, password=password)
    if user:
        user_obj = User(user.id)
        login_user(user_obj, remember=True)
        return jsonify({'status': 'logged_in'})
    return jsonify({'status': 'failed'})


@user_ctrl.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'status': 'logged_out'})


@user_ctrl.route('/add_user', methods=['POST'])
def add_user():
    session = current_app.session_factory.get_session()
    data = request.json
    user_name = data.get('user_name')
    password = data.get('password')
    if not UserModel.check_name_taken(session=session, user_name=user_name):
        UserModel.add_user(session=session, user_name=user_name, password=password)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'failed'})

# Test output route
@user_ctrl.route('/test', methods=['GET'])
def test_output():
    if current_user.is_authenticated:
        return jsonify({'vicc': 'mi az 3 lábá van de nem szék?'})
    return jsonify({'status': 'not_authenticated'})
