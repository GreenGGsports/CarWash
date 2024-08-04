from flask import Blueprint, request, jsonify, current_app, render_template, session
from src.models.user_model import UserModel
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

user_ctrl = Blueprint('user_ctrl', __name__, url_prefix='/user')


#only for testing
@user_ctrl.route('/')
def show_test_form():
    return render_template('User.html')

class User(UserMixin):
    def __init__(self, id=None):
        self.id = id
        

# Function to initialize LoginManager
def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user_ctrl.login'

    @login_manager.user_loader
    def load_user(user_id):
        if user_id is None:
            return None
        
        try:
            user_data = UserModel.get_by_id(user_id)
            if user_data:
                return User(user_id=user_id)
            else:
                return None
        except Exception as e:
            current_app.logger.error(f"Error loading user {user_id}: {e}")
            return None
    
@user_ctrl.route('/login', methods=['POST'])
def login():
    db_session = current_app.session_factory.get_session()
    data = request.json
    user_name = data.get('user_name')
    password = data.get('password')
    user = UserModel.login(session=db_session, user_name=user_name, password=password)
    try:
        user = UserModel.login(session=db_session, user_name=user_name, password=password)
        if user:
            user_obj = User(user.id)
            login_user(user_obj, remember=False)
            session['user_id'] = user.id
            current_app.logger.info(f"User {user_name} logged in successfully.")
            return jsonify({'status': 'logged_in'}), 200
        else:
            current_app.logger.warning(f"Failed login attempt for user {user_name}.")
            return jsonify({'status': 'failed'}), 401
    except Exception as e:
        current_app.logger.error(f"Error during login: {e}")
        return jsonify({'status': 'error', 'message': 'Internal server error.'}), 500


@user_ctrl.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        logout_user()
        current_app.logger.info(f"User {current_user.id} logged out successfully.")
        return jsonify({'status': 'logged_out'}), 200
    except Exception as e:
        current_app.logger.error(f"Error during logout: {e}")
        return jsonify({'status': 'error', 'message': 'Internal server error.'}), 500


@user_ctrl.route('/add_user', methods=['POST'])
def add_user():
    db_session = current_app.session_factory.get_session()
    data = request.json
    user_name = data.get('user_name')
    password = data.get('password')
    
    try:
        if UserModel.check_name_taken(session=db_session, user_name=user_name):
            current_app.logger.warning(f"Attempt to add a user with a taken name: {user_name}.")
            return jsonify({'status': 'failed', 'message': 'Username is already taken.'}), 400

        UserModel.add_user(session=db_session, user_name=user_name, password=password)
        current_app.logger.info(f"User {user_name} added successfully.")
        return jsonify({'status': 'success'}), 201
    except Exception as e:
        current_app.logger.error(f"Error adding user {user_name}: {e}")
        return jsonify({'status': 'error', 'message': 'Internal server error.'}), 500

