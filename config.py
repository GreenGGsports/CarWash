class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your_secret_key'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    pass