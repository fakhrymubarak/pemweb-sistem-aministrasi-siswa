from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    # Create app and basic configs here (DB, etc.)
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    # initialize the database
    
    db.init_app(app)
    
    with app.app_context():
        # Register blueprints
        from .routes.siswa import siswa
        from .routes.jurusan import jurusan
        from .routes.mapel import mapel
        from .routes.periode_ajaran import periode_ajaran
        from .routes.nilai import nilai
        app.register_blueprint(siswa, url_prefix='/api')
        app.register_blueprint(jurusan, url_prefix='/api')
        app.register_blueprint(mapel, url_prefix='/api')
        app.register_blueprint(periode_ajaran, url_prefix='/api')
        app.register_blueprint(nilai, url_prefix='/api')

    return app