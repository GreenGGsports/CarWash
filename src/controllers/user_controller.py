from flask import Blueprint, request, jsonify, current_app, render_template, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_principal import Principal, Identity, RoleNeed, UserNeed, identity_changed, identity_loaded
from src.models.user_model import UserModel

user_ctrl = Blueprint('user_ctrl', __name__, url_prefix='/user')

# Only for testing
@user_ctrl.route('/')
def show_test_form():
    return render_template('User.html')

class User(UserMixin):
    def __init__(self, user):
        self.id = user.id
        self.user_name = user.user_name
        self.role = user.role

# Function to initialize LoginManager
def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user_ctrl.login'

    @login_manager.user_loader
    def load_user(user_id):
        db_session = current_app.session_factory.get_session()
        try:
            user = db_session.query(UserModel).get(user_id)
            if user:
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
        user = UserModel.login(session=db_session, user_name=user_name, password=password)
        if user:
            user_obj = User(user)
            login_user(user_obj, remember=False)
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
            return jsonify({'status': 'logged_in'})
        return jsonify({'status': 'failed'})
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
        if not UserModel.check_name_taken(session=db_session, user_name=user_name):
            UserModel.add_user(session=db_session, user_name=user_name, password=password, role=role)
            return jsonify({'status': 'success'})
        return jsonify({'status': 'failed'})
    finally:
        db_session.close()

# Test output route
@user_ctrl.route('/test', methods=['GET'])
def test_output():
    if current_user.is_authenticated:
        return jsonify({'vicc': 'mi az 3 lába van de nem szék?'})
    return jsonify({'status': 'not_authenticated'})

def init_principal(app):
    principals = Principal(app)
    
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))
        if hasattr(current_user, 'role'):
            identity.provides.add(RoleNeed(current_user.role))
