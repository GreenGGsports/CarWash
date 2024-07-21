from flask import Flask, current_app
from sqlalchemy import create_engine
from sessions import SessionFactory

from config import load_configs
from src.controllers.reservation_controller import reservation_ctrl
from src.controllers.user_controller import user_ctrl, init_login_manager
from src.controllers.carwash_controller import carwash_ctrl
from src.controllers.service_controller import service_ctrl
from database import create_database
from add_record import create_test_db
from src.controllers.admin import init_admin

def create_app(config_name: str):
    app = Flask(__name__)
    
    load_configs(app,config_name)
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    app.session_factory = SessionFactory(engine)
    
    with app.app_context():
        create_database(engine)
        init_admin(app)
    
    init_login_manager(app=app)
    # Register blueprints
    app = add_blueprints(app)
    return app

def add_blueprints(app: Flask):
    app.register_blueprint(reservation_ctrl, url_prefix='/reservation')
    app.register_blueprint(user_ctrl,url_prefix='/user')
    app.register_blueprint(carwash_ctrl,url_prefix='/carwash')
    app.register_blueprint(service_ctrl,url_prefix= '/service')
    return app 

if __name__ == '__main__':
    app = create_app('development')
    app.run()