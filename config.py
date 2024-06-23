import os 
class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'db', 'car_wash.db')
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'db', 'car_wash.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class TestingConfig(Config):
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    pass
