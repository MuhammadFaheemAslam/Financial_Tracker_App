# class Config:
#     SECRET_KEY = '40a210291067df85061ee513d552784d1d0a3040d920c1fccc47f2c087dd485d'
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///financial_tracker.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     DEBUG = True
    
    
DB_USERNAME = 'admin'
DB_PASSWORD = '!Admin12'
DB_HOST = 'financial-tracker-db.cha6wqois6uj.us-east-1.rds.amazonaws.com'
DB_NAME = 'financialtrackerdb'

class Config():
    SECRET_KEY = '40a210291067df85061ee513d552784d1d0a3040d920c1fccc47f2c087dd485d'
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False