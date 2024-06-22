from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from src.controllers.reservation_controller import reservation_ctrl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from src.models.base import Base

db = SQLAlchemy()

class SessionFactory:
    def __init__(self, engine) -> None:
        self.Session = sessionmaker(bind=engine)
        
    def get_session(self):
        return self.Session()

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
    
    db.init_app(app)
    

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    app.session_factory = SessionFactory(engine)
    create_database(app,engine)
    # Register blueprints
    app = add_blueprints(app)
    
    return app

def add_blueprints(app: Flask):
    app.register_blueprint(reservation_ctrl, url_prefix='/reservation')
    return app 

# Create database if it doesn't exist
def create_database(app,engine):
    with app.app_context():
        if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
            Base.metadata.create_all(engine)
            db.create_all()
            print("Database created.")
    
if __name__ == '__main__':
    app = create_app('development')
    app.run()

