class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your_secret_key'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db/test_car_wash.db'

class ProductionConfig(Config):
    pass
