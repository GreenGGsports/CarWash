from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from src.controllers.reservation_controller import reservation_ctrl


def create_app(config_name : str):
    db = SQLAlchemy()
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
    
    with app.app_context():
        db.create_all()  # Adatbázis táblák létrehozása az alkalmazás inicializálásakor
    
    app = add_blueprints(app)
    return app

def add_blueprints(app: Flask):
    app.register_blueprint(reservation_ctrl, url_prefix='/reservation')
    return app 
    

if __name__ == '__main__':
    app = create_app('development')
    app.run()