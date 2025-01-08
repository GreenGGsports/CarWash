from flask import Blueprint, request, jsonify, current_app, render_template, session, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_principal import Principal, Identity, RoleNeed, UserNeed, identity_changed, identity_loaded
from src.models.user_model import UserModel

user_ctrl = Blueprint('user_ctrl', __name__, url_prefix='/user')

# Only for testing
@user_ctrl.route('/')
def show_login_form():
    return render_template('User.html')

@user_ctrl.route('/redirect')
def redirect_form():
    """Redirect to the test form page."""
    return redirect(url_for('user_ctrl.show_login_form'))

class User(UserMixin):
    def __init__(self, user):
        self.id = user.id
        self.user_name = user.user_name
        self.role = user.role
        self.carwash_id = user.carwash_id
        self.carwash = user.carwash

# Function to initialize LoginManager
def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = '/'

    @login_manager.user_loader
    def load_user(user_id):
        db_session = current_app.session_factory.get_session()
        try:
            user = db_session.query(UserModel).get(user_id)
            if user:
                current_app.logger.info('authentication succesfull')
                return User(user)
            return None
        finally:
            db_session.close()

@user_ctrl.route('/login', methods=['POST'])
def login():
    db_session = current_app.session_factory.get_session()
    try:
        data = request.json
        user_name = data.get('user_name')
        password = data.get('password')
        
        # Felhasználó ellenőrzése a UserModel segítségével
        user = UserModel.login(session=db_session, user_name=user_name, password=password)
        
        if user:
            user_obj = User(user)
            login_user(user_obj, remember=False)
            
            # Küldjünk identity_changed jelet a Flask-Principal-nek
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
            
            # Szerepkör alapú átirányítás
            if user.role == 'admin':
                redirect_url = '/admin'  # Admin felület
            elif user.role == 'local_admin':
                redirect_url = '/local-admin'  # Carwash felület
            elif user.role == 'developer':
                redirect_url = '/developer'
            else:
                redirect_url = '/reservation_test/reserve'  # Általános felhasználói felület
            
            current_app.logger.info('Log in successful')
            return jsonify({'status': 'logged_in', 'redirect_url': redirect_url})
        
        # Hibás hitelesítés esetén
        return jsonify({'status': 'failed', 'message': 'Invalid username or password'}), 401
    
    except Exception as e:
        db_session.rollback()
        current_app.logger.error(f"Error during login: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred during login'}), 500
    
    finally:
        db_session.close()


@user_ctrl.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'status': 'logged_out'})

@user_ctrl.route('/add_user', methods=['POST'])
def add_user():
    db_session = current_app.session_factory.get_session()
    try:
        data = request.json
        user_name = data.get('user_name')
        password = data.get('password')
        role = data.get('role', 'user')
        carwash_id = data.get('carwash_id') if role == 'local_admin' else None
        if not UserModel.check_name_taken(session=db_session, user_name=user_name):
            UserModel.add_user(session=db_session, user_name=user_name, password=password, role=role, carwash_id=carwash_id)
            return jsonify({'status': 'success'})
        return jsonify({'status': 'failed'})
    except Exception as e:
        db_session.rollback()
        current_app.logger.error(e)
    finally:
        db_session.close()

@user_ctrl.route('/test-auth', methods=['POST'])
def test_authentication():
    if current_user.is_authenticated:
        return jsonify({'status': 'authenticated', 'message': 'User is authenticated'})
    return jsonify({'status': 'not_authenticated', 'message': 'User is not authenticated'})

def init_principal(app):
    principals = Principal(app)
    
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))
        if hasattr(current_user, 'role'):
            identity.provides.add(RoleNeed(current_user.role))
