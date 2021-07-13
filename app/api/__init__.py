from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    # Create app and basic configs here (DB, etc.)
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config.from_envvar('ENV_FILE_LOCATION')

    # initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    with app.app_context():
        # Register blueprints
        from .routes.siswa import siswa
        from .routes.jurusan import jurusan
        from .routes.mapel import mapel
        from .routes.periode_ajaran import periode_ajaran
        from .routes.nilai import nilai
        from .routes.kelas import kelas
        app.register_blueprint(siswa, url_prefix='/api')
        app.register_blueprint(jurusan, url_prefix='/api')
        app.register_blueprint(mapel, url_prefix='/api')
        app.register_blueprint(periode_ajaran, url_prefix='/api')
        app.register_blueprint(nilai, url_prefix='/api')
        app.register_blueprint(kelas, url_prefix='/api')

        from .auth.super_admin import super_admin
        from .auth.guru import guru
        app.register_blueprint(super_admin, url_prefix='/auth')
        app.register_blueprint(guru, url_prefix='/auth')
    return app