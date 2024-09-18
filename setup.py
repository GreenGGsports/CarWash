from flask import Flask, request, render_template ,  current_app
from sqlalchemy import create_engine
from sessions import SessionFactory
from config import load_configs
from src.controllers.reservation_controller import reservation_ctrl
from src.controllers.user_controller import user_ctrl, init_login_manager, init_principal
from src.controllers.carwash_controller import carwash_ctrl
from src.controllers.service_controller import service_ctrl
from src.controllers.autocomplete import car_ctrl
from src.controllers.admin_controller import admin_ctrl
from src.controllers.local_admin_controller import local_admin_ctrl
from src.controllers.billing_controller import billing_ctrl
from src.controllers.booking_controller import booking_ctrl
from src.controllers.developer_controller import developer_ctrl
from src.controllers.reservation_autofill import reservation_autofill_ctrl
from database import create_database, get_db, close_db
from src.controllers.admin import init_admin, init_local_admin, init_developer_admin
from src.models.user_model import UserModel



from logger import setup_logging
from database import check_database_connection

def create_app(config_name: str):
    app = Flask(__name__)
    
    load_configs(app, config_name)
    
    setup_logging(app)
    if config_name == 'development' or config_name == 'testing':
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    
    else:
        with app.app_context():
            engine = get_db()

    if check_database_connection(engine, app):
        app.logger.info("Database connection initialized successfully.")
    else:
        app.logger.error("Failed to initialize database connection.")
        
    app.teardown_appcontext(close_db)
    
    session_factory = SessionFactory(engine)
    app.session_factory = session_factory
        
    @app.teardown_request
    def teardown_request(exception=None):
        current_app.session_factory.remove(exception)
        if exception:
            current_app.logger.error(exception)
        
    with app.app_context():
        create_database(engine)
        init_admin(app, session_factory)
        init_local_admin(app, session_factory)
        init_developer_admin(app, session_factory)
        
    init_login_manager(app)
    init_principal(app)  # Ensure this is called

    # Register blueprints
    app = add_blueprints(app)
    app.logger.info(f"Application started with configuration: {config_name}")
    return app

def add_blueprints(app: Flask):
    @app.route('/')
    def home():
        return render_template('Landing_page.html')
    
    @app.route('/carwash_sites/<site_name>')
    def carwash_site(site_name):
        try:
            # This will look for the corresponding HTML file inside templates/carwash_sites
            return render_template(f'carwash_sites/{site_name}.html')
        except :
            # Return a 404 error if the file does not exist
            return "Car wash site not found", 404
    
    app.register_blueprint(billing_ctrl, url_prefix ='/billing')
    app.register_blueprint(reservation_ctrl, url_prefix='/reservation')
    app.register_blueprint(user_ctrl, url_prefix='/user')
    app.register_blueprint(carwash_ctrl, url_prefix='/carwash')
    app.register_blueprint(service_ctrl, url_prefix='/service')
    app.register_blueprint(booking_ctrl, url_prefix = '/booking')
    app.register_blueprint(reservation_autofill_ctrl, url_prefix = '/reservation_autofill')


    app.register_blueprint(car_ctrl, url_prefix='/api/car')
    app.register_blueprint(admin_ctrl, url_prefix='/admin', name='admin_blueprint')
    app.register_blueprint(local_admin_ctrl, url_prefix='/local-admin', name='local_admin_blueprint')
    app.register_blueprint(developer_ctrl, url_prefix='/developer', name='developer_admin_blueprint')
    return app 

if __name__ == '__main__':
    app = create_app('development')
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=8080)
