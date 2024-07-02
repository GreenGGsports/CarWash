from flask import Flask
from sqlalchemy import create_engine
from sessions import SessionFactory

from config import DevelopmentConfig, TestingConfig, ProductionConfig
from src.controllers.reservation_controller import reservation_ctrl
from src.controllers.appointment_controller import appointment_ctrl
from database import create_database

def create_app(config_name: str):
    app = Flask(__name__)
    
    if config_name == 'development':
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'testing':
        app.config.from_object(TestingConfig)
    elif config_name == 'production':
        app.config.from_object(ProductionConfig)
    else:
        raise ValueError("Invalid config name. Use 'development', 'testing', or 'production'.")
    
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    app.session_factory = SessionFactory(engine)
    
    with app.app_context():
        create_database(engine)
    
    # Register blueprints
    app = add_blueprints(app)
    
    return app

def add_blueprints(app: Flask):
    app.register_blueprint(reservation_ctrl, url_prefix='/reservation')
    app.register_blueprint(appointment_ctrl,url_prefix='/reservation')
    return app 


if __name__ == '__main__':
    app = create_app('development')
    app.run()