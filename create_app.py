from flask import Flask 
from src.controllers import (
    reservation_controller
)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig, TestingConfig, ProductionConfig

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    
    if config_name == 'development':
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(ProductionConfig)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()  # Adatbázis táblák létrehozása az alkalmazás inicializálásakor
    
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run()