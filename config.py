from urllib.parse import quote_plus

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:%s@localhost/mechanic_api" % quote_plus("fighter4EV@")
    DEBUG = True
    
    
class TestingConfig:
    pass

class ProductionConfig:
    pass