from flask import Flask
from sqlalchemy import create_engine
from sessions import SessionFactory

from config import DevelopmentConfig, TestingConfig, ProductionConfig
from src.controllers.reservation_controller import reservation_ctrl
from src.controllers.user_controller import user_ctrl, init_login_manager
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
    
    init_login_manager(app=app)
    # Register blueprints
    app = add_blueprints(app)
    
    return app

def add_blueprints(app: Flask):
    app.register_blueprint(reservation_ctrl, url_prefix='/reservation')
    app.register_blueprint(user_ctrl,url_prefix='/login_test')
    return app 


if __name__ == '__main__':
    app = create_app('development')
    app.run()