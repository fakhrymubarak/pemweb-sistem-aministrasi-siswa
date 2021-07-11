"""Flask Configuration"""

FLASK_ENV = 'development'
TESTING = True
SECRET_KEY = 'mysecretkey'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/sistem_rapor_pweb'
SQLALCHEMY_TRACK_MODIFICATIONS = False