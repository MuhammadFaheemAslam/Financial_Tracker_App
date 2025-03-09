class Config:
    SECRET_KEY = '40a210291067df85061ee513d552784d1d0a3040d920c1fccc47f2c087dd485d'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///financial_tracker.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    
    
    

class ProductionConfig(Config):
    SECRET_KEY = '40a210291067df85061ee513d552784d1d0a3040d920c1fccc47f2c087dd485d'
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/prod_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False